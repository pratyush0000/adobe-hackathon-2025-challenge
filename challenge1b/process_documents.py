import os
import json
from pathlib import Path
from datetime import datetime
import pdfplumber
import re

INPUT_DIR = Path("/app/input")
PDF_DIR = INPUT_DIR / "pdfs"
OUTPUT_DIR = Path("/app/output")

# Utility: Normalize text for matching
normalize = lambda s: re.sub(r"[^a-z0-9]", "", s.lower()) if s else ""

def extract_headings(pdf_path):
    headings = []
    font_sizes = set()
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            try:
                for block in page.extract_words(extra_attrs=["size", "fontname"]):
                    text = block["text"].strip()
                    size = block["size"]
                    font_sizes.add(size)
                    if len(text) < 3:
                        continue  # skip short words
                    headings.append({
                        "text": text,
                        "size": size,
                        "page": page_num
                    })
            except Exception:
                continue
    # Determine heading levels by font size
    if not font_sizes:
        return []
    sorted_sizes = sorted(font_sizes, reverse=True)
    size_to_level = {}
    if len(sorted_sizes) > 0:
        size_to_level[sorted_sizes[0]] = "Title"
    if len(sorted_sizes) > 1:
        size_to_level[sorted_sizes[1]] = "H1"
    if len(sorted_sizes) > 2:
        size_to_level[sorted_sizes[2]] = "H2"
    if len(sorted_sizes) > 3:
        size_to_level[sorted_sizes[3]] = "H3"
    # Assign levels
    structured = []
    for h in headings:
        level = size_to_level.get(h["size"], "Body")
        if level != "Body":
            structured.append({
                "level": level,
                "text": h["text"],
                "page": h["page"]
            })
    return structured

def rank_headings(headings, persona, job):
    # Gather keywords from persona and job
    persona_keywords = []
    if isinstance(persona, dict):
        persona_keywords += [str(v) for v in persona.values() if isinstance(v, str)]
        for v in persona.values():
            if isinstance(v, list):
                persona_keywords += [str(x) for x in v]
    job_keywords = []
    if isinstance(job, dict):
        job_keywords += [str(v) for v in job.values() if isinstance(v, str)]
        for v in job.values():
            if isinstance(v, list):
                job_keywords += [str(x) for x in v]
    all_keywords = [normalize(k) for k in persona_keywords + job_keywords]
    # Rank: +2 if heading matches any keyword, else 1
    ranked = []
    for h in headings:
        norm_text = normalize(h["text"])
        rank = 1
        for kw in all_keywords:
            if kw and kw in norm_text:
                rank = 3
                break
        ranked.append({
            "level": h["level"],
            "text": h["text"],
            "page": h["page"],
            "importance_rank": rank,
            "refined_text": h["text"]
        })
    return ranked

def main():
    persona_path = INPUT_DIR / "persona.json"
    job_path = INPUT_DIR / "job.json"
    persona = json.load(open(persona_path, encoding="utf-8")) if persona_path.exists() else {}
    job = json.load(open(job_path, encoding="utf-8")) if job_path.exists() else {}
    pdf_files = list(PDF_DIR.glob("*.pdf")) if PDF_DIR.exists() else []
    all_sections = []
    for pdf_file in pdf_files:
        headings = extract_headings(pdf_file)
        ranked = rank_headings(headings, persona, job)
        for r in ranked:
            r["document"] = pdf_file.name
        all_sections.extend(ranked)
    output = {
        "metadata": {
            "input_documents": [str(f.name) for f in pdf_files],
            "persona": persona,
            "job_to_be_done": job,
            "processing_timestamp": datetime.utcnow().isoformat() + "Z"
        },
        "extracted_sections": all_sections
    }
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_DIR / "output.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"✅ Extracted {len(all_sections)} headings from {len(pdf_files)} PDFs. Output written to /app/output/output.json")

if __name__ == "__main__":
    main() 