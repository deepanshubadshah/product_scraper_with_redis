import os
import json
import requests
from pathlib import Path
from typing import List, Optional
from scraper.product import Product

class Storage:
    """
    Abstract base class for storage implementations.
    """
    def save_products(self, products: List[dict]):
        pass

    def get_all_products(self) -> List[dict]:
        pass

class LocalStorage(Storage):
    def __init__(self, file_path: str = "products.json", image_folder: str = "images"):
        self.file_path = file_path
        self.image_folder = Path(image_folder)
        self.image_folder.mkdir(exist_ok=True)

    def save_products(self, products: List[Product]):
        """
        Save products to the local JSON database. If the price of an existing product has changed, update it.
        """
        existing_products = self.get_all_products()
        product_map = {prod["product_link"]: prod for prod in existing_products}  # Map by product_link

        for product in products:
            if product.product_link in product_map:
                # Check if price has changed
                existing_product = product_map[product.product_link]
                if existing_product["product_price"] != product.product_price:
                    print(f"Updating price for {product.product_link}: {existing_product['product_price']} -> {product.product_price}")
                    # Update only the changed fields
                    existing_product["product_price"] = product.product_price
                    existing_product["path_to_image"] = self._save_image(product.image_url)
            else:
                # Add a new product
                print(f"Adding new product: {product.product_link}")
                product.path_to_image = self._save_image(product.image_url)
                existing_products.append(product.to_dict())  # Append new product as a dict

        # Save the updated list back to the file
        with open(self.file_path, "w") as f:
            json.dump(existing_products, f, indent=4)
            

    def get_all_products(self) -> List[dict]:
        if not os.path.exists(self.file_path):
            return []

        with open(self.file_path, "r") as f:
            data = json.load(f)
        return [Product(**product).to_dict() for product in data]  # Return as list of dicts


    def _save_image(self, image_url: Optional[str]) -> Optional[str]:
        if not image_url:
            return None

        image_name = image_url.split("/")[-1]
        absolute_path = os.path.join(os.getcwd(), "images", image_name)
        os.makedirs(os.path.dirname(absolute_path), exist_ok=True)

        # Download and save the image
        try:
            response = requests.get(image_url, stream=True)
            if response.status_code == 200:
                with open(absolute_path, "wb") as img_file:
                    img_file.write(response.content)
            else:
                print(f"Failed to download image: {image_url}")
                return None
        except Exception as e:
            print(f"Error while saving image: {e}")
            return None

        return absolute_path  # Absolute path to the saved image