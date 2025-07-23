import os
import json
from pathlib import Path
import pdfplumber


def extract_headings_from_pdf(pdf_path):
    headings = []
    seen = set()

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            words = page.extract_words(use_text_flow=True, keep_blank_chars=False)

            for word in words:
                text = word["text"].strip()

                if len(text) < 4:
                    continue
                if text.lower() in seen:
                    continue
                seen.add(text.lower())

                font_size = float(word.get("size", 0))
                x0, x1 = word["x0"], word["x1"]
                page_width = page.width
                center_x = (x0 + x1) / 2

                # Heuristics for heading level
                if font_size >= 18 and abs(center_x - page_width / 2) < 100:
                    level = "H1"
                elif font_size >= 16:
                    level = "H2"
                elif font_size >= 14:
                    level = "H3"
                else:
                    continue

                headings.append({
                    "level": level,
                    "text": text,
                    "page": page_num
                })

    return {
        "title": Path(pdf_path).stem,
        "outline": headings
    }


def process_pdfs():
    input_dir = Path("/app/input")
    output_dir = Path("/app/output")
    output_dir.mkdir(parents=True, exist_ok=True)

    for pdf_file in input_dir.glob("*.pdf"):
        result = extract_headings_from_pdf(pdf_file)
        output_file = output_dir / f"{pdf_file.stem}.json"

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(f"[✓] Processed {pdf_file.name} -> {output_file.name}")


if __name__ == "__main__":
    print("📄 Starting PDF outline extraction...")
    process_pdfs()
    print("✅ Completed all files.")
