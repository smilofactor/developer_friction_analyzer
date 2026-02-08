"""
Project: Developer Friction Analyzer (Case Study)
Author:  SMilovidov (github.com/smilofactor)
Date:    2026-02-08

COPYRIGHT NOTICE:
This source code is the sole property of SMilovidov (github.com/smilofactor). 
It is provided for **evaluation and demonstration purposes only**.

RESTRICTIONS:
- You may NOT use this code in a production environment.
- You may NOT modify, distribute, or sub-license this code.
- This code is intended solely to demonstrate technical capability 
  for the purpose of hiring/employment evaluation.

Copyright (c) 2026 SMilovidov (github.com/smilofactor). All Rights Reserved.
"""

import sqlite3
import pandas as pd
import os
import datetime
import re

# --- CONFIGURATION ---
DB_PATH = os.path.join("analyze_store", "market_friction.db")
CAMPAIGN_PAGES="campaign_pages"
REDACT_LIST = ['twilio', 'messagebird', 'plivo', 'sendgrid']

def sanitize_text(text):
    """Replaces competitor names with generic terms using Regex."""
    if not text: return ""
    for brand in REDACT_LIST:
        pattern = re.compile(re.escape(brand), re.IGNORECASE)
        text = pattern.sub("[Provider]", text)
    return text

# FIX: This function must accept 'target_competitor'
def generate_landing_page(target_competitor=None):

    if not os.path.exists(CAMPAIGN_PAGES):
        os.makedirs(CAMPAIGN_PAGES)
        print(f"[*] Created directory: {CAMPAIGN_PAGES}")

    if not os.path.exists(DB_PATH):
        return f"Error: Database not found at {DB_PATH}"

    conn = sqlite3.connect(DB_PATH)

    # FIX: Filter by the specific competitor if requested
    if target_competitor:
        query = "SELECT * FROM friction_points WHERE competitor = ?"
        df = pd.read_sql_query(query, conn, params=(target_competitor,))
    else:
        df = pd.read_sql_query("SELECT * FROM friction_points", conn)

    conn.close()

    if df.empty:
        return f"Error: No data found for {target_competitor}."

    try:
        # Get statistics specific to this competitor
        top_pain = df['pain_category'].mode()[0]
        recent_issues = df.head(3).to_dict('records')

        # Sanitize titles
        for issue in recent_issues:
            issue['title'] = sanitize_text(issue['title'])
    except:
        top_pain = "Reliability"
        recent_issues = []

    # Dynamic Filename
    safe_name = target_competitor.lower() if target_competitor else "generic"
    campaign_filename = f"campaign_{safe_name}.html"
    output_path = os.path.join(CAMPAIGN_PAGES, campaign_filename)

    # HTML Content
    headline = f"Tired of {top_pain} Issues?"
    subhead = f"Switch to Us for reliable delivery."

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Comparison: {target_competitor} vs Us</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-50 text-slate-800 font-sans p-10">
        <div class="max-w-3xl mx-auto bg-white p-8 rounded shadow">
            <h1 class="text-3xl font-bold text-indigo-700 mb-4">{headline}</h1>
            <p class="text-lg text-slate-600 mb-6">{subhead}</p>
            <div class="bg-gray-100 p-4 rounded mb-6">
                <h3 class="font-bold mb-2 text-sm uppercase text-gray-500">Real User Complaints:</h3>
                <ul class="list-disc pl-5 space-y-2">
                    {''.join([f'<li>"{issue["title"]}" <span class="text-red-500 text-xs font-bold">({issue["pain_category"]})</span></li>' for issue in recent_issues])}
                </ul>
            </div>
            <p class="text-xs text-center text-gray-400">Generated from public data. Names redacted where applicable.</p>
        </div>
    </body>
    </html>
    """

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    return output_path

if __name__ == "__main__":
    # Test run
    print(generate_landing_page())

