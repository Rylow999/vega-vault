#!/usr/bin/env python3
"""
Bidirectional Sync: Obsidian ↔ Ontology
- Reads Obsidian notes with frontmatter ontology_id
- Creates/updates entities in Ontology
- Writes ontology_id back to Obsidian frontmatter for new entities
- Maintains consistency between both stores
"""
import yaml, json, os, sys, re
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Set

OBSIDIAN_DIR = Path("/home/delorien/vaults/nexus-dscn/ontology/notes")
GRAPH_PATH = Path("~/.openclaw/workspace/memory/ontology/graph.jsonl").expanduser()
SCHEMA_PATH = Path("~/.openclaw/workspace/memory/ontology/schema.yaml").expanduser()

sys.path.insert(0, str(Path("~/.openclaw/workspace/skills/ontology/scripts").expanduser()))
from ontology import create_entity, create_relation, append_op, load_graph, generate_id

# Type mapping from note content
TYPE_KEYWORDS = {
    "Theorem": ["teorema", "theorem"],
    "Definition": ["definición", "definition"],
    "Conjecture": ["conjetura", "conjecture"],
    "Prediction": ["predicción", "prediction"],
    "Equation": ["ecuación", "equation", "ec."],
    "Parameter": ["parámetro", "parameter"],
    "Paper": ["paper"],
    "Gap": ["gap", "derivation"],
    "Concept": [],  # default
}

def detect_type_from_content(title: str, content: str) -> str:
    """Detect entity type from title and content"""
    text = (title + " " + content[:1000]).lower()
    for etype, keywords in TYPE_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            return etype
    return "Concept"

def extract_frontmatter(content: str) -> tuple[dict, str]:
    """Extract YAML frontmatter if present"""
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            try:
                fm = yaml.safe_load(parts[1]) or {}
                return fm, parts[2].strip()
            except:
                pass
    return {}, content

def write_frontmatter(content: str, fm: dict) -> str:
    """Write frontmatter to content"""
    yaml_str = yaml.dump(fm, allow_unicode=True, sort_keys=False)
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            return f"---\n{yaml_str}---{parts[2]}"
    return f"---\n{yaml_str}---\n{content}"

def parse_note(filepath: Path) -> dict:
    """Parse an Obsidian note"""
    content = filepath.read_text(encoding='utf-8')
    fm, body = extract_frontmatter(content)
    
    title = fm.get('title', filepath.stem)
    ontology_id = fm.get('ontology_id')
    etype = fm.get('type', detect_type_from_content(title, body))
    
    props = {
        "title": title,
        "content": body[:5000],
        "source_file": str(filepath.relative_to(OBSIDIAN_DIR)),
        "tags": fm.get('tags', []),
        "ontology_id": ontology_id,
    }
    
    return {
        "id": ontology_id or generate_id(etype.lower()),
        "type": etype,
        "properties": props,
        "filepath": filepath,
        "frontmatter": fm,
        "body": body
    }

def sync_obsidian_to_ontology():
    """Push Obsidian notes to Ontology"""
    print("Loading existing graph...")
    entities, _ = load_graph(str(GRAPH_PATH))
    print(f"Existing entities: {len(entities)}")
    
    print("\nScanning Obsidian notes...")
    note_files = list(OBSIDIAN_DIR.glob("*.md"))
    print(f"Found {len(note_files)} notes")
    
    created = 0
    updated = 0
    linked = 0
    
    for note_file in note_files:
        try:
            note_data = parse_note(note_file)
            eid = note_data["id"]
            etype = note_data["type"]
            props = note_data["properties"]
            filepath = note_data["filepath"]
            fm = note_data["frontmatter"]
            
            # Check if already exists in ontology
            if eid in entities:
                # Update existing
                entities[eid]["properties"] = props
                # Could append update op here if needed
                updated += 1
            else:
                # Create new entity
                create_entity(etype, props, str(GRAPH_PATH), eid)
                entities[eid] = {"id": eid, "type": etype, "properties": props}
                created += 1
                
                # Write ontology_id back to Obsidian frontmatter if missing
                if not fm.get('ontology_id'):
                    fm['ontology_id'] = eid
                    if not fm.get('type'):
                        fm['type'] = etype
                    new_content = write_frontmatter(note_data["body"], fm)
                    filepath.write_text(new_content, encoding='utf-8')
                    linked += 1
                    print(f"  Linked: {note_file.name} -> {eid}")
                    
        except Exception as e:
            print(f"  Error processing {note_file.name}: {e}")
    
    print(f"\nSync Obsidian → Ontology complete:")
    print(f"  Created: {created}")
    print(f"  Updated: {updated}")
    print(f"  Linked (wrote ontology_id): {linked}")
    
    return entities

def sync_ontology_to_obsidian(entities: Dict):
    """Create Obsidian notes for Ontology entities that don't have notes"""
    print("\nSyncing Ontology → Obsidian...")
    
    # Find entities without Obsidian notes
    existing_files = {f.stem for f in OBSIDIAN_DIR.glob("*.md")}
    created = 0
    
    for eid, ent in entities.items():
        title = ent["properties"].get("title", eid)
        safe_title = re.sub(r'[<>:"/\\|?*]', '_', title)
        
        # Skip if already has note
        if safe_title in existing_files or eid in existing_files:
            continue
        
        # Create note for key theoretical entities
        if ent["type"] in ["Theorem", "Equation", "Prediction", "Conjecture", "Definition", "Paper"]:
            fm = {
                "ontology_id": eid,
                "type": ent["type"],
                "title": title,
                "tags": ent["properties"].get("tags", []),
            }
            
            content = f"# {title}\n\n"
            content += f"**Ontology ID**: `{eid}`\n"
            content += f"**Type**: {ent['type']}\n\n"
            
            # Add properties
            for k, v in ent["properties"].items():
                if k not in ["title", "content", "source_file", "ontology_id"]:
                    content += f"**{k}**: {v}\n"
            
            if "content" in ent["properties"]:
                content += f"\n---\n\n{ent['properties']['content']}"
            
            new_content = write_frontmatter(content, fm)
            filepath = OBSIDIAN_DIR / f"{safe_title}.md"
            filepath.write_text(new_content, encoding='utf-8')
            created += 1
            print(f"  Created note: {filepath.name}")
    
    print(f"  Created {created} new Obsidian notes")

def main():
    print("=" * 60)
    print("Bidirectional Sync: Obsidian ↔ Ontology")
    print("=" * 60)
    
    # Sync Obsidian → Ontology
    entities = sync_obsidian_to_ontology()
    
    # Sync Ontology → Obsidian (create missing notes)
    sync_ontology_to_obsidian(entities)
    
    print("\n" + "=" * 60)
    print("Sync complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
