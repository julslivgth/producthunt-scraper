import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

def scrape_producthunt():
    # Format today's UTC date as YYYY/MM/DD
    today_date = datetime.utcnow().strftime("%Y/%m/%d")
    url = f"https://www.producthunt.com/leaderboard/daily/{today_date}"
    
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {"error": "Failed to fetch the page", "status": response.status_code}
    
    soup = BeautifulSoup(response.text, "html.parser")
    products = []
    
    # Update the CSS selectors based on the current structure of the page
    for product in soup.find_all("li", class_="styles_item__5muID"):
        try:
            name_tag = product.find("h3")
            desc_tag = product.find("p")
            link_tag = product.find("a")
            if not (name_tag and desc_tag and link_tag):
                continue
            name = name_tag.text.strip()
            description = desc_tag.text.strip()
            link = link_tag.get("href")
            full_link = f"https://www.producthunt.com{link}" if link.startswith("/") else link
            
            products.append({
                "name": name,
                "description": description,
                "link": full_link
            })
        except Exception as e:
            continue  # Skip products that cause errors
    
    return products

if __name__ == "__main__":
    data = scrape_producthunt()
    # Print the JSON output for testing
    print(json.dumps(data, indent=2, ensure_ascii=False))
