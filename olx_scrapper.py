import requests
from bs4 import BeautifulSoup
import json
import csv
import time
import random
import argparse
import sys
from pathlib import Path

def scrape_olx(search_query, pages=3, output_format='both'):
    """
    Scrape OLX listings based on search query
    
    Args:
        search_query: Search term to look for
        pages: Number of pages to scrape
        output_format: 'json', 'csv', or 'both'
    """
    base_url = f"https://www.olx.in/items/q-{search_query.replace(' ', '-')}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    all_listings = []
    for page in range(1, pages + 1):
        print(f"Scraping page {page}/{pages}...")
        
        try:
            time.sleep(random.uniform(1, 2))
            response = requests.get(f"{base_url}?page={page}", headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            items = soup.select('li[data-aut-id="itemBox"]')
            
            if not items:
                print(f"No items found on page {page}. Stopping.")
                break
            for item in items:
                listing = {}
                selectors = {
                    'title': '[data-aut-id="itemTitle"]',
                    'price': '[data-aut-id="itemPrice"]',
                    'location': '[data-aut-id="item-location"]'
                }
                for key, selector in selectors.items():
                    element = item.select_one(selector)
                    listing[key] = element.text.strip() if element else "N/A"
                link = item.select_one('a')
                listing['url'] = "https://www.olx.in" + link['href'] if link and 'href' in link.attrs else "N/A"
                img = item.select_one('img')
                listing['image_url'] = img['src'] if img and 'src' in img.attrs else "N/A"
                
                all_listings.append(listing)
            
            print(f"Found {len(items)} listings on page {page}")
            
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            break
    
    # Save results
    if not all_listings:
        print("No listings found.")
        return
        
    output_dir = Path("olx_results")
    output_dir.mkdir(exist_ok=True)
    
    if output_format in ['json', 'both']:
        output_file = output_dir / f"{search_query.replace(' ', '_')}_listings.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_listings, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(all_listings)} listings to {output_file}")
    
    if output_format in ['csv', 'both']:
        output_file = output_dir / f"{search_query.replace(' ', '_')}_listings.csv"
        if all_listings:
            with open(output_file, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=all_listings[0].keys())
                writer.writeheader()
                writer.writerows(all_listings)
            print(f"Saved {len(all_listings)} listings to {output_file}")
    
    return all_listings

def main():
    parser = argparse.ArgumentParser(description='Scrape OLX listings')
    parser.add_argument('search_query', nargs='?', default='car cover', help='Search term to look for')
    parser.add_argument('-p', '--pages', type=int, default=3, help='Number of pages to scrape')
    parser.add_argument('-f', '--format', choices=['json', 'csv', 'both'], default='both', help='Output format')
    args = parser.parse_args()
    
    print(f"Starting OLX scraper for '{args.search_query}'")
    scrape_olx(args.search_query, args.pages, args.format)
    print("Scraping complete!")

if __name__ == "__main__":
    main()