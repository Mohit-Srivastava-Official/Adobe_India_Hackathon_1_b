import os
import json
import fitz  # PyMuPDF
from datetime import datetime
from collections import Counter

def extract_sections(pdf_path):
    doc = fitz.open(pdf_path)
    sections = []
    for page_num, page in enumerate(doc, 1):
        blocks = page.get_text("dict")['blocks']
        for block in blocks:
            if block['type'] == 0:
                for line in block['lines']:
                    text = ''.join([span['text'] for span in line['spans']]).strip()
                    if not text or len(text) < 5:
                        continue
                    font_sizes = [span['size'] for span in line['spans']]
                    max_size = max(font_sizes)
                    if max_size > 14:
                        level = 'H1'
                    elif max_size > 12:
                        level = 'H2'
                    elif max_size > 10:
                        level = 'H3'
                    else:
                        continue
                    sections.append({
                        'title': text,
                        'page': page_num,
                        'level': level
                    })
    return sections

def score_section(section, persona, job):
    # Simple keyword overlap scoring
    section_text = section['title'].lower()
    persona_words = set(persona.lower().split())
    job_words = set(job.lower().split())
    score = len(persona_words & set(section_text.split())) + len(job_words & set(section_text.split()))
    return score

def main():
    input_dir = '../input'
    output_dir = '../output'
    persona_path = '../persona.json'
    os.makedirs(output_dir, exist_ok=True)
    with open(persona_path, 'r', encoding='utf-8') as f:
        persona_data = json.load(f)
    persona = persona_data['persona']
    job = persona_data['job_to_be_done']
    all_sections = []
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(input_dir, filename)
            sections = extract_sections(pdf_path)
            for section in sections:
                section['document'] = filename
                section['score'] = score_section(section, persona, job)
                all_sections.append(section)
    # Rank sections
    ranked_sections = sorted([s for s in all_sections if s['score'] > 0], key=lambda x: -x['score'])
    extracted_sections = []
    subsection_analysis = []
    for rank, section in enumerate(ranked_sections[:10], 1):
        extracted_sections.append({
            'document': section['document'],
            'page_number': section['page'],
            'section_title': section['title'],
            'importance_rank': rank
        })
        # Subsection: extract a snippet from the page
        doc = fitz.open(os.path.join(input_dir, section['document']))
        page = doc[section['page']-1]
        text = page.get_text().strip().replace('\n', ' ')
        snippet = text[:400]  # First 400 chars as a refined text
        subsection_analysis.append({
            'document': section['document'],
            'refined_text': snippet,
            'page_number': section['page']
        })
    output = {
        'metadata': {
            'input_documents': [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')],
            'persona': persona,
            'job_to_be_done': job,
            'processing_timestamp': datetime.utcnow().isoformat() + 'Z'
        },
        'extracted_sections': extracted_sections,
        'subsection_analysis': subsection_analysis
    }
    with open(os.path.join(output_dir, 'output.json'), 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
