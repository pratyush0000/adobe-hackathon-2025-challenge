# Adobe India Hackathon 2025 – Challenge 1A

## 🧠 Goal
Extract title and hierarchical headings (H1, H2, H3) from PDF documents and output structured JSON.

## 🚀 How to Build and Run

### 1. Build Docker Image
```bash
docker build --platform linux/amd64 -t pdf-outline-extractor .
```
### 2. Run
```bash
docker run --rm `
  -v "$PWD\sample_dataset\pdfs:/app/input:ro" `
  -v "$PWD\sample_dataset\outputs:/app/output" `
  --network none pdf-outline-extractor

