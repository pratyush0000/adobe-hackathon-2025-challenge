import os, json
import pdfplumber
from collections import defaultdict
from statistics import median

def extract_outline(pdf_path):
    outline = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            lines = defaultdict(list)
            sizes = defaultdict(list)
            fonts = defaultdict(list)

            for c in page.chars:
                y = round(c['top'], 1)
                lines[y].append(c)
                sizes[y].append(c['size'])
                fonts[y].append(c.get('fontname', ''))

            for y in sorted(lines):
                chars = sorted(lines[y], key=lambda c: c['x0'])
                text = ''.join(c['text'] for c in chars).strip()
                if not text:
                    continue

                avg_size = median(sizes[y])
                common_font = max(set(fonts[y]), key=fonts[y].count)

                # Heading detection heuristics
                if avg_size >= 14 or text.isupper() or 'bold' in common_font.lower():
                    level = "H1" if avg_size >= 18 else "H2"
                    outline.append({
                        "level": level,
                        "text": text,
                        "page": i + 1
                    })
    return outline

def main(input_dir, output_dir):
    if not os.path.exists(input_dir):
        print(f"❌ Input directory does not exist: {input_dir}")
        return

    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if not filename.lower().endswith(".pdf"):
            continue

        pdf_path = os.path.join(input_dir, filename)
        print(f"📄 Processing {filename}")
        outline = extract_outline(pdf_path)
        output = {
            "title": os.path.splitext(filename)[0],
            "outline": outline
        }

        out_path = os.path.join(output_dir, f"{output['title']}.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        print(f"✅ Saved to {out_path} ({len(outline)} headings)\n")

if __name__ == "__main__":
    # Use your folder structure under sample_dataset
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(base_dir, "sample_dataset", "pdfs")
    output_dir = os.path.join(base_dir, "sample_dataset", "outputs")

    main(input_dir, output_dir)
