import requests
from typing import List, Dict

API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
DETAILS_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

def fetch_pubmed_papers(query: str, debug: bool = False) -> List[Dict]:
    search_params = {
        "db": "pubmed",
        "term": query,
        "retmax": 50,
        "retmode": "json"
    }
    search_res = requests.get(API_URL, params=search_params)
    search_res.raise_for_status()
    ids = search_res.json()["esearchresult"]["idlist"]

    fetch_params = {
        "db": "pubmed",
        "id": ",".join(ids),
        "retmode": "xml"
    }
    fetch_res = requests.get(DETAILS_URL, params=fetch_params)
    fetch_res.raise_for_status()

    from xml.etree import ElementTree as ET
    root = ET.fromstring(fetch_res.content)
    papers = []

    for article in root.findall(".//PubmedArticle"):
        try:
            pmid = article.findtext(".//PMID")
            title = article.findtext(".//ArticleTitle")
            date = article.findtext(".//PubDate/Year") or "Unknown"
            authors = article.findall(".//Author")
            author_data = []

            for a in authors:
                name = a.findtext("LastName", "") + " " + a.findtext("ForeName", "")
                affil = a.findtext(".//AffiliationInfo/Affiliation")
                email = a.findtext(".//AffiliationInfo/Affiliation")
                author_data.append({"name": name, "affiliation": affil or "", "email": email or ""})

            papers.append({
                "pmid": pmid,
                "title": title,
                "date": date,
                "authors": author_data
            })
        except Exception:
            continue

    return papers