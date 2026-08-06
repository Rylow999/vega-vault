#!/usr/bin/env python3
"""
Import ALL Obsidian notes and papers into Ontology
"""
import json, yaml, re, os, sys, uuid
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional

# Paths
OBSIDIAN_NOTES = Path("/home/delorien/vaults/nexus-dscn/ontology/notes")
PAPERS_DIR = Path("/home/delorien/vaults/nexus-dscn/papers")
GRAPH_PATH = Path("~/.openclaw/workspace/memory/ontology/graph.jsonl").expanduser()
SCHEMA_PATH = Path("~/.openclaw/workspace/memory/ontology/schema.yaml").expanduser()

sys.path.insert(0, str(Path("~/.openclaw/workspace/skills/ontology/scripts").expanduser()))
from ontology import (
    create_entity, create_relation, append_op, load_graph, generate_id,
    resolve_safe_path
)

# Type mapping based on note content patterns
TYPE_PATTERNS = {
    "Theorem": [r"Theorem\s+\d+", r"Teorema\s+\d+", r"^Theorem ", r"^Teorema "],
    "Lemma": [r"Lemma\s+\d+", r"Lema\s+\d+"],
    "Definition": [r"Definition\s+\d+", r"Definici[oó]n\s+\d+"],
    "Conjecture": [r"Conjecture\s+[A-Z]?\d+", r"Conjetura\s+[A-Z]?\d+"],
    "Prediction": [r"Prediction\s+[a-zA-Z]\d*", r"Predicci[oó]n\s+[a-zA-Z]\d*"],
    "Equation": [r"Ecuaci[oó]n\s+\d+", r"Equation\s+\d+", r"Ec\.\s*\d+"],
    "Parameter": [r"Par[áa]metro\s+\w+", r"Parameter\s+\w+"],
    "Paper": [r"Paper\b", r"paper\b"],
    "Framework": [r"Framework\b", r"framework\b"],
    "Concept": [r"Concept\b", r"concept\b"],
}

def detect_type(title: str, content: str) -> str:
    """Detect entity type from title and content"""
    text = (title + " " + content[:500]).lower()
    
    if any(re.search(p, text, re.IGNORECASE) for p in TYPE_PATTERNS["Theorem"]):
        return "Theorem"
    if any(re.search(p, text, re.IGNORECASE) for p in TYPE_PATTERNS["Lemma"]):
        return "Theorem"  # Treat lemmas as theorems
    if any(re.search(p, text, re.IGNORECASE) for p in TYPE_PATTERNS["Definition"]):
        return "Definition"
    if any(re.search(p, text, re.IGNORECASE) for p in TYPE_PATTERNS["Conjecture"]):
        return "Conjecture"
    if any(re.search(p, text, re.IGNORECASE) for p in TYPE_PATTERNS["Prediction"]):
        return "Prediction"
    if any(re.search(p, text, re.IGNORECASE) for p in TYPE_PATTERNS["Equation"]):
        return "Equation"
    if any(re.search(p, text, re.IGNORECASE) for p in TYPE_PATTERNS["Parameter"]):
        return "Parameter"
    if any(re.search(p, text, re.IGNORECASE) for p in TYPE_PATTERNS["Paper"]):
        return "Paper"
    if any(re.search(p, text, re.IGNORECASE) for p in TYPE_PATTERNS["Framework"]):
        return "Paper"  # Frameworks as papers
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

def parse_note(filepath: Path) -> dict:
    """Parse an Obsidian note"""
    content = filepath.read_text(encoding='utf-8')
    fm, body = extract_frontmatter(content)
    
    title = fm.get('title', filepath.stem)
    ontology_id = fm.get('ontology_id', generate_id('concept'))
    
    # Detect type
    etype = fm.get('type', detect_type(title, body))
    
    # Build properties
    props = {
        "title": title,
        "content": body[:5000],  # Limit content size
        "source_file": str(filepath.relative_to(OBSIDIAN_NOTES)),
        "tags": fm.get('tags', []),
    }
    
    # Add ontology_id to properties for linking
    props["ontology_id"] = ontology_id
    
    return {
        "id": ontology_id,
        "type": etype,
        "properties": props
    }

def parse_paper(filepath: Path) -> dict:
    """Parse a paper markdown file"""
    content = filepath.read_text(encoding='utf-8')
    fm, body = extract_frontmatter(content)
    
    title = fm.get('title', filepath.stem)
    ontology_id = fm.get('ontology_id', generate_id('paper'))
    
    # Extract authors, year, etc from content or frontmatter
    authors = fm.get('authors', ["Luciano Benjamín Nieto"])
    year = fm.get('year', 2026)
    venue = fm.get('venue', "Technical Report")
    
    props = {
        "title": title,
        "authors": authors,
        "year": year,
        "venue": venue,
        "doi": fm.get('doi', ''),
        "url": fm.get('url', ''),
        "summary": fm.get('summary', body[:1000]),
        "tags": fm.get('tags', []),
        "source_file": str(filepath.relative_to(PAPERS_DIR)),
        "content": body[:10000],
    }
    
    return {
        "id": ontology_id,
        "type": "Paper",
        "properties": props
    }

def main():
    print("Loading existing graph...")
    entities, relations = load_graph(str(GRAPH_PATH))
    print(f"Existing entities: {len(entities)}")
    
    # Process Obsidian notes
    print("\nProcessing Obsidian notes...")
    note_count = 0
    for note_file in OBSIDIAN_NOTES.glob("*.md"):
        try:
            entity_data = parse_note(note_file)
            eid = entity_data["id"]
            
            if eid not in entities:
                # Create entity
                record = {
                    "op": "create",
                    "entity": entity_data,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
                append_op(str(GRAPH_PATH), record)
                entities[eid] = entity_data
                note_count += 1
                if note_count % 10 == 0:
                    print(f"  Created {note_count} notes...")
        except Exception as e:
            print(f"  Error processing {note_file.name}: {e}")
    
    print(f"Total notes processed: {note_count}")
    
    # Process papers
    print("\nProcessing papers...")
    paper_count = 0
    for paper_dir in PAPERS_DIR.iterdir():
        if not paper_dir.is_dir():
            continue
        for paper_file in paper_dir.glob("*.md"):
            try:
                entity_data = parse_paper(paper_file)
                eid = entity_data["id"]
                
                if eid not in entities:
                    record = {
                        "op": "create",
                        "entity": entity_data,
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }
                    append_op(str(GRAPH_PATH), record)
                    entities[eid] = entity_data
                    paper_count += 1
            except Exception as e:
                print(f"  Error processing {paper_file}: {e}")
    
    print(f"Total papers processed: {paper_count}")
    print(f"Total entities in graph: {len(entities)}")
    
    # Now create relations based on content analysis
    print("\nCreating cross-references...")
    create_cross_references(entities)
    
    print("\nDone!")

def create_cross_references(entities: Dict):
    """Create relations between entities based on content"""
    # Build lookup by title/keywords
    title_to_id = {}
    for eid, ent in entities.items():
        title = ent["properties"].get("title", "").lower()
        if title:
            title_to_id[title] = eid
    
    # Link papers to concepts they reference
    for eid, ent in entities.items():
        if ent["type"] == "Paper":
            content = ent["properties"].get("content", "").lower()
            # Find mentioned concepts
            for title, cid in title_to_id.items():
                if title in content and cid != eid:
                    # Create relation
                    record = {
                        "op": "relate",
                        "from": eid,
                        "rel": "references_paper",
                        "to": cid,
                        "properties": {},
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }
                    append_op(str(GRAPH_PATH), record)

if __name__ == "__main__":
    main()
