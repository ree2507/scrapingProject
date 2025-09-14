import requests
import pandas as pd
from bs4 import BeautifulSoup

# response = requests.get("https://sandbox.oxylabs.io/products/category/pc/page_num=1")


baseUrl = "https://sandbox.oxylabs.io/products/category/pc"
page_num = 1

def classify_price(price_str):
    # mata uang dollar atau euro
    try:
        price_str = price_str.replace('$', '').replace('€', '').replace(',', '.').strip()
        price = float(price_str)
        if price < 80:
            return 'Murah'
        elif price <= 89 and price >= 80 :
            return 'Sedang'
        else:
            return 'Mahal'
    except Exception:
        return 'Unknown'

result = []
for page_num in range(1, 4):
    url = f"{baseUrl}?page_num={page_num}"
    print(f"Scraping page: {url}")

    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve the page or no more pages available.")
        break

    soup = BeautifulSoup(response.text, 'html.parser')
    produk = soup.find_all("div", class_="product-card css-e8at8d eag3qlw10")

    if not produk:
        print("No more data found, ending the scraping process.")
        break

    for item in produk:
        nameGames = item.find("h4", class_="title css-7u5e79 eag3qlw7").get_text(strip=True)
        tags = item.find('p', class_="category css-8fdgzc eag3qlw9")
        if tags:
            tags = " | ".join([tag.get_text() for tag in tags])
        price = item.find("div", class_="price-wrapper css-li4v8k eag3qlw4").get_text(strip=True)
        price_class = classify_price(price)
        result.append((nameGames, tags, price, price_class))

df = pd.DataFrame(result, columns=['Name', 'Tags', 'Price', 'Price_Class'])
with pd.ExcelWriter('tes.xlsx') as writer:
    df.to_excel(writer, sheet_name='sheet1', index=False)