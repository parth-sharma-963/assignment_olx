# OLX Scraper

A lightweight Python script to scrape product listings from OLX India.

## Features

- **Flexible search**: Search for any product on OLX
- **Multiple formats**: Save results as JSON, CSV, or both
- **Customizable**: Control the number of pages to scrape
- **Command-line interface**: Easy to use with command-line arguments

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/olx-scraper.git
cd olx-scraper

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Basic usage

```bash
python olx_scraper.py "car cover"
```

### Advanced options

```bash
# Specify number of pages to scrape
python olx_scraper.py "car cover" --pages 5

# Choose output format (json, csv, or both)
python olx_scraper.py "car cover" --format json

# Get help
python olx_scraper.py --help
```

## Output

Results are saved in the `olx_results` directory:
- `car_cover_listings.json`
- `car_cover_listings.csv`

## Disclaimer

Web scraping may be against the Terms of Service of websites. Use responsibly and at your own risk. This script is for educational purposes only.

## License

MIT