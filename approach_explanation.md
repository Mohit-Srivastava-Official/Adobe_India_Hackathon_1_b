# Approach Explanation – Round 1B

## Methodology
This solution extracts and ranks relevant sections from a collection of PDFs based on a given persona and job-to-be-done. It uses a fast, offline-friendly keyword overlap method:
- Extracts headings (H1, H2, H3) from each PDF using PyMuPDF.
- Scores each section by keyword overlap with persona and job description.
- Ranks and outputs the most relevant sections and a snippet from each page as sub-section analysis.

## Why This Approach?
- Fully offline, no internet or large models required.
- Fast and lightweight, suitable for hackathon constraints.
- Modular and easy to extend with more advanced NLP if needed.

## Libraries Used
- PyMuPDF for PDF parsing and text extraction.

## How to Run
- Place PDFs in `input/`, edit `persona.json`, and run the Docker container as described in the README.
- Output will be in `output/output.json`.
