import os
import json
import pdfplumber

INPUT_DIR = "input"
OUTPUT_DIR = "output"

# Customize these if needed
STOPWORDS = {"name", "date", "page", "table", "figure", "signature", "amount", "total"}
HEADING_KEYWORDS = {
    "introduction", "objective", "overview", "abstract", "proposal", "request", "application",
    "instructions", "acknowledgement", "terms", "conditions", "summary", "scope", "background",
    "history", "agenda", "contents", "references", "methodology", "conclusion", "appendix"
}

def is_probable_heading(text):
    text_clean = text.strip().lower()
    word_count = len(text.split())

    # Basic filters
    if word_count < 2:
        return False
    if any(stop == text_clean for stop in STOPWORDS):
        return False
    if any(char.isdigit() for char in text_clean.split()[0]):
        return False
    if text.endswith(":") or text.endswith("."):
        return False

    # Positive signals
    if any(kw in text_clean for kw in HEADING_KEYWORDS):
        return True
    if text.isupper() or text.istitle():
        return True
    if word_count >= 3 and text[0].isupper():
        return True

    return False

def extract_outline_from_pdf(pdf_path):
    outline = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                words = page.extract_words(use_text_flow=True, keep_blank_chars=False)
                lines = {}

                for word in words:
                    top = round(word['top'], 1)
                    if top not in lines:
                        lines[top] = []
                    lines[top].append(word)

                for top, line_words in sorted(lines.items()):
                    line_text = " ".join(w['text'] for w in sorted(line_words, key=lambda x: x['x0']))
                    font_size = sum(float(w.get("size", 0)) for w in line_words) / len(line_words)

                    if is_probable_heading(line_text):
                        outline.append({
                            "level": "H1" if font_size > 10 else "H2",
                            "text": line_text.strip(),
                            "page": i + 1
                        })
                    else:
                        print(f"❌ Skipped line: '{line_text}'")

    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")

    return outline

def process_all_pdfs():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith(".pdf"):
            file_path = os.path.join(INPUT_DIR, filename)
            print(f"📄 Processing: {filename}")
            outline = extract_outline_from_pdf(file_path)
            output = {
                "title": os.path.splitext(filename)[0],
                "outline": outline
            }

            output_file = os.path.join(OUTPUT_DIR, f"{output['title']}.json")
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(output, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    process_all_pdfs()
