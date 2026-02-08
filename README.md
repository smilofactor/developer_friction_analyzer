# Developer Friction Analyzer (Sent.dm Case Study)

**A Market Intelligence & Automated Campaign Tool**

> **Note:** This project was created for **evaluation purposes only**. It demonstrates full-stack capability: data scraping, SQL persistence, interactive visualization, and programmatic asset generation.

## 🚀 The Mission
To identify where developers struggle with competitor APIs (Twilio, MessageBird, etc.) and automatically generate marketing assets that target those specific pain points.

## 🛠 Architecture
1.  **The Scraper (`friction_analyzer.py`):**
    - Aggregates real-time developer complaints from Stack Overflow.
    - Uses regex to categorize issues (Reliability, Pricing, Documentation).
    - Stores intelligence in a local SQLite database (`market_friction.db`).

2.  **The Dashboard (`market_friction_monitor.py`):**
    - A Streamlit-based Command Center.
    - Visualizes which competitors are failing and why.
    - Allows the user to filter data by competitor or pain category.

3.  **The Campaign Generator (`landing_page_generator.py`):**
    - Takes the selected competitor (e.g., "MessageBird").
    - Pulls the top 3 recent complaints from the database.
    - Dynamically generates a sanitized HTML landing page pitching Sent.dm as the solution.

## 📦 How to Run
1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Gather Intelligence (Scrape Data):**
    ```bash
    python friction_analyzer.py
    ```

3.  **Launch Command Center:**
    ```bash
    streamlit run market_friction_monitor.py
    ```

## ⚖️ Legal & Ethics
- **Data Source:** Publicly available data via Stack Exchange API.
- **Sanitization:** The `landing_page_generator.py` includes regex logic to redact competitor names from the generated marketing assets to prevent trademark liability during demos.
- **License:** Proprietary / Evaluation Only. See header in source files.

---
*Created by SMilovidov - 2026*
