import os
from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import HttpUrl, ValidationError
from scraper.scraper import Scraper
from cache import Cache
from storage import LocalStorage
from dotenv import load_dotenv


app = FastAPI()

load_dotenv()
TOKEN = os.getenv("AUTH_TOKEN")
REDIS_URL = os.getenv("REDIS_URL")

def authenticate(auth_token: str = Header(...)):
    """
    Authenticate the user using a token in the Authorization header.
    """
    if auth_token != TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True


def validate_proxy(proxy: str):
    """
    Validate the proxy string using Pydantic's HttpUrl model.
    """
    if proxy:
        try:
            validated_proxy = HttpUrl(proxy)
            return str(validated_proxy)
        except ValidationError:
            raise HTTPException(status_code=400, detail="Invalid proxy URL format.")
    return None

@app.get("/scrape")
def scrape(limit: int = 5, proxy: str = None, auth: bool = Depends(authenticate)):

    proxy = validate_proxy(proxy)
    storage = LocalStorage()
    cache = Cache(redis_url=REDIS_URL)
    scraper = Scraper(limit, proxy, storage, cache)
    scraper.scrape_catalogue()
    return {"message": f"Scraping completed for {limit} pages."}


@app.get("/health")
async def check_health():
    return "Working"