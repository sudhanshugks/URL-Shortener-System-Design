# URL Shortener – System Design Experiment

## Objective
Design, implement, and evaluate a URL redirection system that converts long URLs into short URLs and measure system performance under varying request loads.

## System Design

The system consists of three components:
1. **Client** – Sends requests to shorten or resolve URLs.
2. **Web Server (Flask)** – Handles API requests.
3. **Database (SQLite)** – Stores short code ↔ long URL mappings.

**API Endpoints:**
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/shorten` | Accepts a long URL, returns a short URL |
| GET | `/<short_code>` | Redirects (HTTP 302) to the original URL |

## Flowchart

```mermaid
graph TD
    A[Client] -->|POST /shorten| B(Web Server)
    B --> C{Generate Short Code}
    C --> D[Store in Database]
    D --> E[Return Short URL]

    F[Client] -->|GET /short_code| G(Web Server)
    G --> H[Lookup in Database]
    H --> I{Found?}
    I -- Yes --> J[HTTP 302 Redirect]
    I -- No --> K[HTTP 404 Not Found]
```

## Load Test Results

| Metric | Value |
|--------|-------|
| Concurrency | 20 threads |
| Total Requests | 500 |
| Successful Requests | 500 (100%) |
| Requests Per Second | 4.82 |
| Avg Shorten Latency | 2113.09 ms |
| Avg Resolve Latency | 2025.38 ms |

## How to Run
Run in 1st Terminal:
```bash
pip install -r requirements.txt
python app.py
```
Run in separate 2nd Terminal:
```bash
python load_test.py
```
