def extract_sections(text):
    sections = {
        "skills": "",
        "education": "",
        "experience": "",
        "languages": "",
        "interests": ""
    }

    lower_text = text.lower()

    section_map = {
        "skills": ["compétences", "competences"],
        "education": ["formation"],
        "experience": ["expériences professionnelles", "experiences professionnelles", "expérience professionnelle", "experience professionnelle"],
        "languages": ["langues"],
        "interests": ["centres d’intérêt", "centres d'interet", "centres d interet"]
    }

    for section_name, keywords in section_map.items():
        for keyword in keywords:
            if keyword in lower_text:
                start = lower_text.find(keyword)
                snippet = lower_text[start:start + 400]
                sections[section_name] = snippet
                break

    return sections