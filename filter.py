from typing import List, Dict

def is_non_academic(affiliation: str) -> bool:
    academic_keywords = ["university", "institute", "college", "school", "department", "lab"]
    return not any(kw.lower() in affiliation.lower() for kw in academic_keywords)

def is_pharma_or_biotech(affiliation: str) -> bool:
    return any(term in affiliation.lower() for term in ["pharma", "biotech", "therapeutics", "biosciences", "inc", "corp", "ltd"])

def filter_papers(papers: List[Dict]) -> List[Dict]:
    filtered = []
    for paper in papers:
        non_academic_authors = []
        companies = set()
        email = ""

        for author in paper["authors"]:
            affil = author["affiliation"]
            if affil and is_pharma_or_biotech(affil):
                companies.add(affil)
            if affil and is_non_academic(affil):
                non_academic_authors.append(author["name"])
                if not email and "@" in author["email"]:
                    email = author["email"]

        if companies:
            filtered.append({
                "PubMedID": paper["pmid"],
                "Title": paper["title"],
                "Publication Date": paper["date"],
                "Non-academic Author(s)": ", ".join(non_academic_authors),
                "Company Affiliation(s)": ", ".join(companies),
                "Corresponding Author Email": email
            })
    return filtered