# Real Estate Data Crawler and API

## Overview
This project is a comprehensive real estate data crawler and API service designed to scrape property data from the [Bayut](https://www.bayut.com) website. It uses Selenium for dynamic web scraping, Celery for task scheduling, FastAPI for serving data through a RESTful API, and PostgreSQL for robust data storage. The system is containerized with Docker and orchestrated using Docker Compose.

## Key Features
- **Dynamic Web Scraping**: Selenium with ChromeDriver enables scraping JavaScript-rendered content.
- **Background Task Queue**: Celery manages asynchronous tasks for processing and storing scraped data.
- **Data Storage**: PostgreSQL serves as the database for reliable and structured data storage.
- **RESTful API**: FastAPI provides endpoints for accessing and aggregating data.
- **Dockerized Setup**: Docker Compose ensures seamless development and deployment.
- **Robust Handling**: The scraper intelligently skips irrelevant sections and ensures no duplication in the database.

---

## Technology Stack
- **Python**: Core programming language.
- **Selenium**: Web scraping with headless Chromium.
- **Celery**: Task queue for distributed processing.
- **PostgreSQL**: Relational database for data persistence.
- **FastAPI**: Framework for building the API.
- **Docker/Docker Compose**: Containerization and orchestration.
- **Redis**: Message broker for Celery.
- **SQLAlchemy**: ORM for database interactions.

---

## Project Structure
```plaintext
real_estate_project/
├── crawler/
│   ├── __init__.py
│   ├── actual_crawler.py      # Main script for crawling and queuing tasks
│   ├── tasks.py               # Celery tasks for background processing
│   ├── database.py            # Database models and functions
│   ├── utils.py               # Utility functions for scraping
├── api/
│   ├── __init__.py
│   ├── main.py                # FastAPI application
├── docker-compose.yml         # Docker Compose configuration
├── Dockerfile                 # Dockerfile for building containers
├── requirements.txt           # Python dependencies
├── README.md                  # Documentation
```

---

## How It Works

### Crawling Workflow
1. **Fetch Listing URLs**: The crawler uses Selenium to navigate the website and scrape property URLs dynamically.
2. **Process Each Listing**: For each URL, Celery asynchronously processes the page, extracting detailed property information.
3. **Store in Database**: The scraped data is stored in a PostgreSQL database, avoiding duplicates.

### FastAPI Endpoints
- `/`: Root endpoint with a welcome message.
- `/listings/`: Fetch listings with optional filtering by region and TruCheck status.
- `/listings/region_counts/`: Aggregate listing counts by region.
- `/listings/trucheck_counts/`: Aggregate TruCheck-verified listings by region.

---

## Installation and Setup

### Prerequisites
- Docker and Docker Compose installed on your machine.
- Python 3.12+ (for manual script testing).

### Step-by-Step Guide
1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd real_estate_project
   ```

2. **Build and Run the Docker Containers**
   ```bash
   docker compose build
   docker compose up -d
   ```

3. **Verify the Setup**
   - Check the running containers:
     ```bash
     sudo docker ps
     ```
   - Access the FastAPI Swagger UI:
     Navigate to `http://localhost:8000/docs` in your browser.

4. **Start the Crawler**
   ```bash
   sudo docker exec -it <crawler_container_name> python crawler/actual_crawler.py
   ```

5. **Access Data via API**
   - Example: Fetch all listings:
     ```bash
     curl http://localhost:8000/listings/
     ```
   - Example: Get region counts:
     ```bash
     curl http://localhost:8000/listings/region_counts/
     ```

---

## Usage Guide

### Adding New Features
1. **Add New Fields**: Update `crawler/database.py` to modify the `Listing` model.
2. **Extend Scraping Logic**: Update `crawler/utils.py` to scrape additional property details.
3. **Expose New API Endpoints**: Add routes in `api/main.py` for custom queries or new data endpoints.

### Debugging
- Use logs from Celery:
  ```bash
  sudo docker logs <celery_worker_container>
  ```
- Access the PostgreSQL database:
  ```bash
  sudo docker exec -it <postgres_container_name> psql -U user -d real_estate
  ```

### Resetting the Database
To clear all data and reset the database:
```bash
docker compose down -v
docker compose up -d
```

---

## Future Enhancements
- **Pagination**: Add pagination support for API endpoints.
- **Authentication**: Secure API with user authentication.
- **Advanced Analytics**: Provide richer aggregated statistics and insights.
- **Cloud Deployment**: Deploy the service to AWS, GCP, or Azure for broader accessibility.
- **Improved Error Handling**: Enhance resilience against scraping errors and timeouts.

---

## Credits
Special thanks to the open-source libraries and tools that made this project possible: Selenium, Celery, SQLAlchemy, FastAPI, Docker, and PostgreSQL.

---

## License
This project is licensed under the MIT License. See `LICENSE` for details.

---

## Support
For any issues, please create an issue in the GitHub repository or contact the maintainers.

---

Enjoy building and exploring with the Real Estate Data Crawler and API! 🚀


