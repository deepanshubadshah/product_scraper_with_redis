from typing import Optional

class Product:
    def __init__(self, product_title: str, product_price: float, product_link: str, path_to_image: Optional[str] = "", image_url: Optional[str] = None):
        self.product_title = self._validate_title(product_title)
        self.product_price = self._validate_price(product_price)
        self.product_link = product_link
        self.path_to_image = path_to_image
        self.image_url = image_url

    def to_dict(self):
        """
        Convert the Product instance to a dictionary in the required format.
        """
        return {
            "product_title": self.product_title,
            "product_price": self.product_price,
            "product_link": self.product_link,
            "path_to_image": self.path_to_image,
        }

    @classmethod
    def from_scraped_data(cls, data):
        """
        Create a Product instance from scraped data.
        The 'data' dictionary may include optional 'image_url'.
        """
        return cls(
            product_title=data.get("title"), 
            product_price=data.get("price"), 
            product_link=data.get("product_link"),
            image_url=data.get("image_url", "")
        )

    @staticmethod
    def _validate_title(title: str) -> str:
        """
        Validate product title.
        """
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Invalid product title. It must be a non-empty string.")
        return title.strip()

    @staticmethod
    def _validate_price(price: float) -> float:
        """
        Validate product price.
        """
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Invalid product price. It must be a positive number.")
        return round(float(price), 2)
