# PDF Processing Solution

## Overview
This repository contains solutions for **Challenge 1a and Challenge 1b** of the Adobe India Hackathon 2025. Both challenges require implementing PDF processing solutions that extract structured data from PDF documents and output JSON files. The solutions must be containerized using Docker and meet specific performance and resource constraints.

---

# Challenge 1a: PDF to JSON Processing

## Overview
Challenge 1a requires implementing a PDF processing solution that extracts structured data from PDF documents and outputs JSON files. The solution must be containerized using Docker and meet specific performance and resource constraints.

## Official Challenge Guidelines

### Submission Requirements
- **GitHub Project**: Complete code repository with working solution
- **Dockerfile**: Must be present in the root directory and functional
- **README.md**:  Documentation explaining the solution, models, and libraries used

### Build Command
```bash
docker build --platform linux/amd64 -t <reponame.someidentifier> .
```

### Run Command
```bash
docker run --rm -v $(pwd)/input:/app/input:ro -v $(pwd)/output/repoidentifier/:/app/output --network none <reponame.someidentifier>
```

### Critical Constraints
- **Execution Time**: ≤ 10 seconds for a 50-page PDF
- **Model Size**: ≤ 200MB (if using ML models)
- **Network**: No internet access allowed during runtime execution
- **Runtime**: Must run on CPU (amd64) with 8 CPUs and 16 GB RAM
- **Architecture**: Must work on AMD64, not ARM-specific

### Key Requirements
- **Automatic Processing**: Process all PDFs from `/app/input` directory
- **Output Format**: Generate `filename.json` for each `filename.pdf`
- **Input Directory**: Read-only access only
- **Open Source**: All libraries, models, and tools must be open source
- **Cross-Platform**: Test on both simple and complex PDFs

## Sample Solution Structure
```
Challenge_1a/
├── sample_dataset/
│   ├── outputs/         # JSON files provided as outputs.
│   ├── pdfs/            # Input PDF files
│   └── schema/          # Output schema definition
│       └── output_schema.json
├── Dockerfile           # Docker container configuration
├── process_pdfs.py      # Sample processing script
└── README.md           # This file
```

## Sample Implementation

### Current Sample Solution
The provided `process_pdfs.py` is a **basic sample** that demonstrates:
- PDF file scanning from input directory
- Dummy JSON data generation
- Output file creation in the specified format

**Note**: This is a placeholder implementation using dummy data. A real solution would need to:
- Implement actual PDF text extraction
- Parse document structure and hierarchy
- Generate meaningful JSON output based on content analysis

### Sample Processing Script (`process_pdfs.py`)
```python
# Current sample implementation
def process_pdfs():
    input_dir = Path("/app/input")
    output_dir = Path("/app/output")
    
    # Process all PDF files
    for pdf_file in input_dir.glob("*.pdf"):
        # Generate structured JSON output
        # (Current implementation uses dummy data)
        output_file = output_dir / f"{pdf_file.stem}.json"
        # Save JSON output
```

### Sample Docker Configuration
```dockerfile
FROM --platform=linux/amd64 python:3.10
WORKDIR /app
COPY process_pdfs.py .
CMD ["python", "process_pdfs.py"]
```

## Expected Output Format

### Required JSON Structure
Each PDF should generate a corresponding JSON file that **must conform to the schema** defined in `sample_dataset/schema/output_schema.json`.

## Implementation Guidelines

### Performance Considerations
- **Memory Management**: Efficient handling of large PDFs
- **Processing Speed**: Optimize for sub-10-second execution
- **Resource Usage**: Stay within 16GB RAM constraint
- **CPU Utilization**: Efficient use of 8 CPU cores

### Testing Strategy
- **Simple PDFs**: Test with basic PDF documents
- **Complex PDFs**: Test with multi-column layouts, images, tables
- **Large PDFs**: Verify 50-page processing within time limit

## Testing Your Solution

### Local Testing
```bash
# Build the Docker image
docker build --platform linux/amd64 -t pdf-processor .

# Test with sample data
docker run --rm -v $(pwd)/sample_dataset/pdfs:/app/input:ro -v $(pwd)/sample_dataset/outputs:/app/output --network none pdf-processor
```

### Validation Checklist
- [ ] All PDFs in input directory are processed
- [ ] JSON output files are generated for each PDF
- [ ] Output format matches required structure
- [ ] **Output conforms to schema** in `sample_dataset/schema/output_schema.json`
- [ ] Processing completes within 10 seconds for 50-page PDFs
- [ ] Solution works without internet access
- [ ] Memory usage stays within 16GB limit
- [ ] Compatible with AMD64 architecture

---

# Challenge 1b: Advanced PDF Processing

## Overview
Challenge 1b builds upon Challenge 1a and requires implementing an advanced PDF processing solution with enhanced capabilities for extracting structured data from complex PDF documents. The solution must handle more sophisticated document structures and provide more detailed JSON outputs.

## Official Challenge Guidelines

### Submission Requirements
- **GitHub Project**: Complete code repository with working solution
- **Dockerfile**: Must be present in the root directory and functional
- **README.md**: Documentation explaining the solution, models, and libraries used

### Build Command
```bash
docker build --platform linux/amd64 -t <reponame.someidentifier> .
```

### Run Command
```bash
docker run --rm -v $(pwd)/input:/app/input:ro -v $(pwd)/output/repoidentifier/:/app/output --network none <reponame.someidentifier>
```

### Critical Constraints
- **Execution Time**: ≤ 15 seconds for a 50-page PDF
- **Model Size**: ≤ 300MB (if using ML models)
- **Network**: No internet access allowed during runtime execution
- **Runtime**: Must run on CPU (amd64) with 8 CPUs and 16 GB RAM
- **Architecture**: Must work on AMD64, not ARM-specific

### Key Requirements
- **Advanced Processing**: Handle complex PDF layouts, tables, and multi-column documents
- **Enhanced Output**: Generate detailed JSON with hierarchical structure
- **Automatic Processing**: Process all PDFs from `/app/input` directory
- **Output Format**: Generate `filename.json` for each `filename.pdf`
- **Input Directory**: Read-only access only
- **Open Source**: All libraries, models, and tools must be open source
- **Cross-Platform**: Test on both simple and complex PDFs

## Sample Solution Structure
```
Challenge_1b/
├── sample_dataset/
│   ├── outputs/         # JSON files provided as outputs.
│   ├── pdfs/            # Input PDF files
│   └── schema/          # Output schema definition
│       └── output_schema.json
├── Dockerfile           # Docker container configuration
├── process_pdfs.py      # Advanced processing script
└── README.md           # This file
```

## Advanced Implementation

### Enhanced Processing Capabilities
The Challenge 1b solution should demonstrate:
- **Table Extraction**: Accurate parsing of complex table structures
- **Multi-column Layout**: Handling documents with multiple columns
- **Image Processing**: Basic image analysis and text extraction from images
- **Hierarchical Structure**: Maintaining document hierarchy and relationships
- **Metadata Extraction**: Extracting document metadata and properties

### Advanced Processing Script (`process_pdfs.py`)
```python
# Advanced implementation for Challenge 1b
def process_pdfs():
    input_dir = Path("/app/input")
    output_dir = Path("/app/output")
    
    # Process all PDF files with enhanced capabilities
    for pdf_file in input_dir.glob("*.pdf"):
        # Extract complex document structure
        # Handle tables, multi-column layouts, images
        # Generate detailed hierarchical JSON output
        output_file = output_dir / f"{pdf_file.stem}.json"
        # Save enhanced JSON output
```

### Advanced Docker Configuration
```dockerfile
FROM --platform=linux/amd64 python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY process_pdfs.py .
CMD ["python", "process_pdfs.py"]
```

## Expected Output Format

### Enhanced JSON Structure
Each PDF should generate a corresponding JSON file that **must conform to the advanced schema** defined in `sample_dataset/schema/output_schema.json`. The output should include:
- **Document Structure**: Hierarchical representation of document sections
- **Table Data**: Structured table information with headers and data
- **Image Information**: Basic image analysis and extracted text
- **Metadata**: Document properties and processing information

## Implementation Guidelines

### Performance Considerations
- **Memory Management**: Efficient handling of large PDFs with complex structures
- **Processing Speed**: Optimize for sub-15-second execution
- **Resource Usage**: Stay within 16GB RAM constraint
- **CPU Utilization**: Efficient use of 8 CPU cores for complex processing

### Testing Strategy
- **Simple PDFs**: Test with basic PDF documents
- **Complex PDFs**: Test with multi-column layouts, tables, images
- **Large PDFs**: Verify 50-page processing within time limit
- **Edge Cases**: Test with unusual document formats and structures

## Testing Your Solution

### Local Testing
```bash
# Build the Docker image
docker build --platform linux/amd64 -t pdf-processor-advanced .

# Test with sample data
docker run --rm -v $(pwd)/sample_dataset/pdfs:/app/input:ro -v $(pwd)/sample_dataset/outputs:/app/output --network none pdf-processor-advanced
```

### Validation Checklist
- [ ] All PDFs in input directory are processed
- [ ] Enhanced JSON output files are generated for each PDF
- [ ] Output format matches advanced structure requirements
- [ ] **Output conforms to advanced schema** in `sample_dataset/schema/output_schema.json`
- [ ] Processing completes within 15 seconds for 50-page PDFs
- [ ] Solution works without internet access
- [ ] Memory usage stays within 16GB limit
- [ ] Compatible with AMD64 architecture
- [ ] Handles complex document structures (tables, multi-column layouts)
- [ ] Extracts and processes images appropriately

---

**Important**: These are sample implementations. Participants should develop their own solutions that meet all the official challenge requirements and constraints for both Challenge 1a and Challenge 1b. 