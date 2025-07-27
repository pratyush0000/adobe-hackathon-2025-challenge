# Challenge 1B: Persona-Driven Document Intelligence

This solution processes a collection of PDFs and, given a persona and job-to-be-done, extracts and ranks relevant sections. The output is a JSON file with metadata and dummy extracted sections (for now).

## Build the Docker Image

```
docker build --platform linux/amd64 -t mysolutionname:somerandomidentifier .
```

## Run the Solution

```
docker run --rm -v "${PWD}\sample_input:/app/input:ro" -v "${PWD}\sample_output:/app/output" --network none mysolutionname:somerandomidentifier
```

- Place your PDFs in `sample_input/pdfs/`
- Place `persona.json` and `job.json` in `sample_input/`
- Output will be written to `sample_output/output.json`

## Files
- `process_documents.py`: Main script
- `requirements.txt`: Python dependencies
- `Dockerfile`: Container configuration
- `approach_explanation.md`: Describe your approach here

## Notes
- This is a minimal working template. Replace the dummy extraction logic with your actual implementation. 