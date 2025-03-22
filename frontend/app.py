# app.py (frontend)
import streamlit as st
import requests
import json
import logging
import os
import base64
import io

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Point to your Azure ACI backend
BACKEND_URL = os.getenv("BACKEND_URL", "http://news-summarizer-akash.eastus.azurecontainer.io:5000/summarize")

def fetch_summary(company_name):
    """Send a POST request to the Flask backend to get the summary."""
    try:
        headers = {"Content-Type": "application/json"}
        payload = {"Company": company_name}
        response = requests.post(BACKEND_URL, headers=headers, json=payload, timeout=300)  
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching summary from backend: {e}")
        return {"error": str(e)}

def main():
    st.title("News Summarizer")
    st.markdown("Enter a company name to get a summary of recent news articles, sentiment analysis, Hindi translations, and audio summaries.")

    company_name = st.text_input("Company Name", value="Tesla", help="Enter the name of the company (e.g., Tesla, Apple)")

    if st.button("Summarize"):
        if not company_name:
            st.error("Please enter a company name.")
            return

        with st.spinner("Fetching and processing news articles... This may take up to 10 minutes."):
            result = fetch_summary(company_name)

            if "error" in result:
                st.error(f"Error: {result['error']}")
                return

            st.header(f"Summary for {result.get('Company', company_name)}")

            # Display Articles
            st.subheader("Articles")
            articles = result.get("processed_articles", [])
            for i, article in enumerate(articles, 1):
                with st.expander(f"Article {i}: {article.get('title', 'No Title')}"):
                    st.write(f"**Summary (English):** {article.get('summary', 'N/A')}")
                    st.write(f"**Hindi Summary:** {article.get('hindi_summary', 'N/A')}")
                    st.write(f"**Sentiment:** {article.get('sentiment', 'N/A')}")
                    st.write(f"**Topics:** {', '.join(article.get('topics', ['N/A']))}")
                    st.write("**Hindi TTS Audio:**")
                    audio_base64 = article.get("hindi_tts_base64", "TTS generation failed")
                    if audio_base64 != "TTS generation failed":
                        audio_bytes = base64.b64decode(audio_base64)
                        st.audio(audio_bytes, format="audio/mp3")
                    else:
                        st.write("Audio generation failed.")

            # Display Comparative Analysis
            st.subheader("Comparative Analysis")
            analysis = result.get("analysis_results", {})
            st.write("**Sentiment Distribution:**")
            sentiment_dist = analysis.get("Sentiment Distribution", {})
            for sentiment, count in sentiment_dist.items():
                st.write(f"{sentiment}: {count}")
            st.write("**Common Topics:**")
            st.write(', '.join(analysis.get("Common Topics", ["N/A"])))

if __name__ == "__main__":
    main()