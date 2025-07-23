import fitz  # PyMuPDF
import json
from pathlib import Path

def extract_headings_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    outline = []

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                spans = line["spans"]
                if not spans:
                    continue

                text = " ".join(span["text"] for span in spans).strip()
                if not text or len(text) < 4:
                    continue

                size = spans[0]["size"]
                font = spans[0]["font"]

                # Use font size to heuristically determine level
                if size > 16:
                    level = "H1"
                elif size > 14:
                    level = "H2"
                elif size > 12:
                    level = "H3"
                else:
                    continue

                outline.append({
                    "level": level,
                    "text": text,
                    "page": page_num
                })

    title = pdf_path.stem
    return {
        "title": title,
        "outline": outline
    }

def process_pdfs():
    input_dir = Path("/app/input")
    output_dir = Path("/app/output")
    output_dir.mkdir(parents=True, exist_ok=True)

    for pdf_file in input_dir.glob("*.pdf"):
        print(f"[INFO] Processing {pdf_file.name}")
        result = extract_headings_from_pdf(pdf_file)

        output_file = output_dir / f"{pdf_file.stem}.json"
        with open(output_file, "w") as f:
            json.dump(result, f, indent=2)

        print(f"[INFO] Saved to {output_file.name}")

if __name__ == "__main__":
    process_pdfs()