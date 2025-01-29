import requests
from typing import Optional
from bs4 import BeautifulSoup
from utils.utils import retry, sanitize_price
from cache import Cache
from storage import Storage
from scraper.product import Product


class Scraper:
    def __init__(self, limit: int, proxy: Optional[str], storage: Storage, cache: Cache):
        self.limit = limit
        self.proxy = proxy
        self.storage = storage
        self.cache = cache

    def fetch_page(self, url: str) -> str:
        """
        Fetch a page with retry logic.
        """
        def request():
            proxies = None
            if self.proxy:
                proxies = {"http": self.proxy, "https": self.proxy}
            try:
                response = requests.get(url, proxies=proxies, timeout=20)  # Ensure headers are passed
                response.raise_for_status()
                return response.text
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 404:
                    raise  # Properly handle 404
                else:
                    print(f"Retrying {url} due to HTTP error: {e}")
                    return retry(requests, retries=3, delay=2)  

        try:
            return request()
        except Exception as e:
            print(f"Failed to fetch {url}: {e}")
            return ""


    def parse_products(self, html: str):
        """
        Parse product details from HTML.
        """
        soup = BeautifulSoup(html, "html.parser")
        products = []

        for product_card in soup.find_all("div", class_="product-inner"):
            # Extract product title
            title_element = product_card.find("h2", class_="woo-loop-product__title")
            title = title_element.text.strip()

            # Extract product link (href)
            product_link = title_element.find("a")["href"]

            # Extract and sanitize product price
            price = product_card.find("span", class_="woocommerce-Price-amount amount").text.strip()
            sanitized_price = sanitize_price(price)

            # Image URL extraction
            img_tag = product_card.find("img", class_="attachment-woocommerce_thumbnail")
            image_url = (
                img_tag.get("data-lazy-src") or  
                img_tag.get("data-src") or       
                img_tag.get("src")
            )

            # Create a Product object with extracted data
            products.append(Product.from_scraped_data({
                "title": title,
                "price": sanitized_price,
                "image_url": image_url or None,
                "product_link": product_link
            }))

        return products
    

    def scrape_catalogue(self):
        """
        Scrape product details and save them in the required format.
        """
        base_url = "https://dentalstall.com/shop/"
        total_products = 0
        updated_products = 0

        for page in range(1, self.limit + 1):
            url = f"{base_url}page/{page}/" if page > 1 else base_url
            try:
                print(f"Scraping {url}...")
                html = self.fetch_page(url)
                if not html.strip():
                    print(f"Skipping page {page} due to empty response.")
                    break
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 404:
                    print(f"Page {page} not found. Stopping pagination.")
                    break
                else:
                    raise

            products = self.parse_products(html)
            if not products:
                print(f"No products found on page {page}. Stopping pagination.")
                break

            for product in products:
                cache_key = self.cache.generate_key(product.product_link)  # Use product_link as the unique key
                cached_price = self.cache.get(cache_key)

                if cached_price != str(product.product_price):  # if the price changed
                    self.storage.save_products([product])
                    self.cache.set(cache_key, product.product_price)
                    updated_products += 1

            total_products += len(products)

        print(f"Scraping completed: {total_products} products scraped, {updated_products} updated in DB.")
        return total_products, updated_products