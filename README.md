# product_scraper_with_redis
 Product Scrapper with Redis, Proxy and Retry mechanism

# Quick Setup for Running the App
## 1. Requirements
### System:
Python 3.8+

Pip

Redis (local or remote instance)

(Optional) Virtual Environment

## 2. Setup
### Step 1: Clone the Repo
```git clone <repo-url>```

```cd <repo-name>```

### Step 2: Virtual Environment (Optional)
#### macOS/Linux:
```python3 -m venv venv```

```source venv/bin/activate```

#### Windows:
```python -m venv venv```

```venv\Scripts\activate```
### Step 3: Install Requirements
```pip install -r requirements.txt```
### Step 4: Redis Configuration
Start Redis server with Port: ```6379```

## 3. Run the App
### Step 1: Start the App
```uvicorn main:app --reload```

### Step 2: Access APIs
Swagger UI:  ```http://127.0.0.1:8000/docs```

ReDoc:  ```http://127.0.0.1:8000/redoc```

## 4. Test the Scrape API
### Using Swagger UI:

auth-token (string): ```31655c42d72f8cf4454111b3f7806128```

### Using curl:

curl -X 'GET' \
  'http://127.0.0.1:8000/scrape?limit=1' \
  -H 'accept: application/json' \
  -H 'auth-token: 31655c42d72f8cf4454111b3f7806128'



