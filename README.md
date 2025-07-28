# Round 1B – Persona-Driven Document Intelligence

## Overview
This solution processes a collection of PDFs, a persona definition, and a job-to-be-done, then extracts and ranks the most relevant sections and sub-sections for that persona and job. Output is a structured JSON as per the hackathon requirements.

## How to Use
- Place your PDFs in the `input/` directory.
- Provide a `persona.json` file describing the persona and job-to-be-done.
- Build and run the Docker container as described in the main README.
- Output will be in the `output/` directory.

## Approach
- Uses text extraction and semantic similarity to rank sections.
- Modular and ready for further improvements.

---
