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

import streamlit as st
import pandas as pd
import sqlite3
import os
import streamlit.components.v1 as components

# --- IMPORT THE REAL GENERATOR ---
# This ensures the output is exactly the same as running the script manually
from landing_page_generator import generate_landing_page

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Market Friction Analyzer", layout="wide")
st.title("Developer Friction Tracker & Campaign Generator")

# --- DATABASE CONNECTION ---
DB_PATH = os.path.join("analyze_store", "market_friction.db")

def load_data():
    """Connects to the SQLite database and returns the dataframe."""
    if not os.path.exists(DB_PATH):
        return None
    
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM friction_points", conn)
    conn.close()
    return df

# --- MAIN APP LOGIC ---
df = load_data()

if df is None:
    st.error(f"Database not found at: {DB_PATH}")
    st.info("Run 'friction_analyzer.py' first.")

elif df.empty:
    st.warning("The database is currently empty.")

else:
    # Use Tabs to separate Analysis from Action
    tab1, tab2 = st.tabs(["📊 Market Analysis", "🚀 Campaign Generator"])

    with tab1:
        # Sidebar Filters (Analysis Tab Only)
        st.sidebar.header("Filters")
        all_competitors = df['competitor'].unique()
        selected_competitors = st.sidebar.multiselect(
            "Select Competitor",
            options=all_competitors,
            default=all_competitors
        )
        
        df_filtered = df[df['competitor'].isin(selected_competitors)]

        # Metrics & Charts
        col1, col2, col3 = st.columns(3)
        col1.metric("Friction Points", len(df_filtered))
        col2.metric("Top Pain", df_filtered['pain_category'].mode()[0] if not df_filtered.empty else "N/A")
        col3.metric("Competitors", len(df_filtered['competitor'].unique()))

        st.divider()

        c1, c2 = st.columns(2)
        c1.bar_chart(df_filtered['competitor'].value_counts())
        c2.bar_chart(df_filtered['pain_category'].value_counts())

        st.subheader("Raw Data Feed")
        st.dataframe(
            df_filtered[['competitor', 'pain_category', 'title', 'link']],
            column_config={"link": st.column_config.LinkColumn("Link")},
            use_container_width=True
        )
    with tab2:
        st.header("Auto-Generated Landing Page")
        st.caption("Select a competitor to create a targeted campaign asset.")
        
        # FIX: Explicit Dropdown to choose the target
        # We use the unique list of competitors found in the database
        target_camp = st.selectbox(
            "Choose Competitor to Target:", 
            options=df['competitor'].unique()
        )

        if st.button(f"Generate Campaign for {target_camp}"):
            with st.spinner(f"Drafting copy against {target_camp}..."):
                try:
                    # PASS THE TARGET TO THE FUNCTION
                    generated_file = generate_landing_page(target_competitor=target_camp)
                    
                    if "Error" in generated_file:
                        st.error(generated_file)
                    else:
                        st.success(f"Asset generated: {generated_file}")
                        
                        # Read and Display
                        with open(generated_file, "r", encoding="utf-8") as f:
                            html_code = f.read()

                        st.download_button(
                            label="Download HTML",
                            data=html_code,
                            file_name=generated_file,
                            mime="text/html"
                        )
                        
                        st.divider()
                        components.html(html_code, height=800, scrolling=True)
                        
                except TypeError:
                    st.error("Mismatch Error: Ensure landing_page_generator.py is updated to accept arguments.")
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")

