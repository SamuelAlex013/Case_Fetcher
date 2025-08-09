# Delhi High Court Case Fetcher

A Flask web application to fetch and parse Delhi High Court case details, including parties, filing/disposal dates, status, and order/judgment PDF links, with automated CAPTCHA handling and a modern UI.

Video Demo : https://www.loom.com/share/520807a61ee840febb7e9a2303c86f4b?sid=04f88412-d92d-498e-a378-feca8e887bc8
---

## Features
- Search Delhi High Court cases by type, number, and year
- Automated CAPTCHA bypass (reads value from DOM)
- Parses parties, filing/disposal dates, status, and PDF links
- Loading spinner for long-running searches
- Lazy-loads 190+ case types for fast UI
- Stores all queries in SQLite database
- View all previous queries at `/queries`
- Docker and Docker Compose support
- Unit test example and CI workflow

---

## Court Chosen
- **Delhi High Court** ([https://dhcmisc.nic.in/pcase/guiCaseWise.php](https://dhcmisc.nic.in/pcase/guiCaseWise.php))

---

## Setup Steps

### Local (Recommended for Dev)
1. Clone the repo
2. `cd Court_Case_fetcher`
3. Create a virtual environment and activate it:
   ```
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Run the app:
   ```
   python run.py
   ```
6. Open [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser

### Docker
1. Build the image:
   ```
   docker build -t court-case-fetcher .
   ```
2. Run the container:
   ```
   docker run -p 5000:5000 court-case-fetcher
   ```
3. Or use Docker Compose:
   ```
   docker-compose up --build
   ```

---

## CAPTCHA Strategy
- The CAPTCHA is not an image; its value is present in the DOM and is read directly using Selenium.

---

## Environment Variables
- No special env vars required for basic use.
- (Optional) Set `FLASK_ENV=development` for debug mode.

---


## License
MIT License (see LICENSE file)

---


## Project Structure

```
Court_Case_fetcher/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── scraper.py
├── templates/
│   ├── index.html
│   ├── results.html
│   ├── queries.html
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── LICENSE
├── README.md
```

---

## How it Works
- User fills the form and submits a case search
- Loading spinner appears while Selenium automates the search and CAPTCHA
- Results page shows parsed details and PDF links (if available)
- All queries are logged and viewable at `/queries`

---
