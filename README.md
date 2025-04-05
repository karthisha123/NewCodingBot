# get-papers-list

Fetches PubMed papers based on a search query, filters for pharma/biotech affiliated authors, and outputs a CSV.

## Installation

```bash
poetry install
```

## Usage

```bash
poetry run get-papers-list "cancer immunotherapy" -f results.csv
```

## Options

- `-f, --file`: Save results to CSV
- `-d, --debug`: Show debug output

## Project Structure

- `fetch.py`: Fetches papers from PubMed
- `filter.py`: Filters authors with non-academic, pharma/biotech affiliations
- `utils.py`: CSV writing utility