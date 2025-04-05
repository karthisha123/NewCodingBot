import argparse
from get_papers.fetch import fetch_pubmed_papers
from get_papers.filter import filter_papers
from get_papers.utils import write_to_csv

def main():
    parser = argparse.ArgumentParser(description="Fetch PubMed papers based on a query.")
    parser.add_argument("query", type=str, help="PubMed query string")
    parser.add_argument("-f", "--file", help="Filename to save CSV results", default=None)
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug output")
    
    args = parser.parse_args()

    try:
        if args.debug:
            print("Fetching papers from PubMed...")
        papers = fetch_pubmed_papers(args.query, debug=args.debug)

        if args.debug:
            print("Filtering papers for non-academic authors with company affiliations...")
        filtered_papers = filter_papers(papers)

        if args.file:
            write_to_csv(filtered_papers, args.file)
            print(f"Saved results to {args.file}")
        else:
            for paper in filtered_papers:
                print(paper)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()