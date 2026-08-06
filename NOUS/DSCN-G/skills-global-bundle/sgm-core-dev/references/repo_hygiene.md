# SGM repo hygiene pattern (reusable)

Run this whenever Luciano asks to "clean up" / "fix the repo" / "leave README perfect".

## 1. experiment_registry.json
- Rebuild entries by reading every results_*.json under phases/ + results/ (real data, not memory).
- Dedup by experiment_id. Sort by numeric suffix via regex re.search(r"(\d+)", eid.split("_")[-1])
  (handles exp_SGM_0003_stress). Add missing experiments that have a result JSON. Validate json.load.

## 2. READMEs — ONE canonical
- README.md (raiz) = canonical. README_SGM.md = navigation index only. Delete duplicates
  (docs/SGM_README.md was an LE-mixed duplicate with a false "Primer sistema cognitivo funcional" title).
- Drop titles that contradict the honest-limits table.

## 3. lit/papers/
- Misnamed paper? Check the index first, then confirm via md5 (byte-identical -> safe delete)
  and/or PyPDF2 text extraction (no pdftotext/mutool on device).
  - kanerva_hdc_1988_0903.4547.pdf was really Kanerva 2009 -> renamed kanerva_hdc_2009_0903.4547.pdf;
    byte-identical wrong_id/kanerva_hdc_2009.pdf deleted (md5 3867be7e0c625087c9e3f71cc23b63d5).
  - hipporag_v2_2025.pdf was SNAP (McGill 2024) per PyPDF2 text -> renamed snap_2024.pdf, moved out of wrong_id/.
- Keep PDFs in VAULT, EXCLUDE from GitHub via .gitignore (lit/papers/). Repo keeps only
  SGM_literature_index.md with arXiv/NASA links. Update index lines for renamed files.

## 4. git hygiene
- .gitignore: __pycache__/, *.pyc, lit/papers/. DELETE committed .pyc on GitHub via API. Add LICENSE (MIT).
- After local deletes, DELETE same GitHub paths via API (push script only upserts).

## 5. Verify before claiming done
- Push log: 200/201 for expected, no .pyc, no stray PDF. GET key paths 200/404 as expected.
- registry.json loads with no duplicates.
