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

import requests
import sqlite3
import time
import os

# --- CONFIGURATION ---
DATA_DIR = "analyze_store"
DB_NAME = "market_friction.db"
# This creates the full path: analyze_store/market_friction.db
DB_PATH = os.path.join(DATA_DIR, DB_NAME)

def init_db():
    """Initializes the SQLite manifold in the specific sub-directory."""
    
    # 1. Create the directory if it doesn't exist (mkdir -p behavior)
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        print(f"[*] Created storage directory: {DATA_DIR}")

    # 2. Connect to the database inside that directory
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create a table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS friction_points (
            id TEXT PRIMARY KEY,
            competitor TEXT,
            title TEXT,
            link TEXT,
            score INTEGER,
            view_count INTEGER,
            is_answered BOOLEAN,
            pain_category TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    return conn

def fetch_competitor_issues(conn, tags=['twilio', 'messagebird', 'plivo', 'sendgrid']):
    url = "https://api.stackexchange.com/2.3/search/advanced"
    pain_keywords = ['error', 'fail', 'slow', 'stuck', 'limit', 'bug', 'exception', 'help']
    cursor = conn.cursor()
    
    total_new = 0

    for tag in tags:
        print(f"[*] Scanning {tag} stream...")
        params = {
            'order': 'desc',
            'sort': 'creation',
            'tagged': tag,
            'site': 'stackoverflow',
            'pagesize': 50,
            'filter': 'withbody' 
        }
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            
            for item in data.get('items', []):
                title = item['title'].lower()
                
                if any(keyword in title for keyword in pain_keywords):
                    issue_id = str(item['question_id'])
                    competitor = tag
                    pain_category = detect_pain_category(title)
                    
                    cursor.execute('''
                        INSERT OR IGNORE INTO friction_points 
                        (id, competitor, title, link, score, view_count, is_answered, pain_category)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (issue_id, competitor, item['title'], item['link'], item['score'], item['view_count'], item['is_answered'], pain_category))
                    
                    if cursor.rowcount > 0:
                        total_new += 1
            
            conn.commit() 
            time.sleep(1.0) 
            
        except Exception as e:
            print(f"[!] Error scanning {tag}: {e}")

    return total_new

def detect_pain_category(text):
    text = text.lower()
    if 'cost' in text or 'price' in text: return 'Pricing'
    if 'fail' in text or 'error' in text or 'exception' in text: return 'Reliability'
    if 'slow' in text or 'timeout' in text: return 'Performance'
    return 'Implementation'

if __name__ == "__main__":
    print(f"--- Starting Friction Analysis (Target: {DB_PATH}) ---")
    db_conn = init_db()
    new_records = fetch_competitor_issues(db_conn)
    print(f"Success! Added {new_records} new friction points to database.")
    db_conn.close()
