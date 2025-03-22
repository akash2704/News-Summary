# app.py (backend)
from flask import Flask, request, jsonify
import logging
from news_summarizer import fetch_and_process_articles

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json()
    company_name = data.get("Company")
    if not company_name:
        return jsonify({"error": "Company name is required"}), 400

    logger.info(f"Received request to summarize news for company: {company_name}")
    processed_articles, analysis_results = fetch_and_process_articles(company_name)

    if not processed_articles:
        return jsonify({"error": "No articles found or processed"}), 404

    response = {
        "Company": company_name,
        "processed_articles": processed_articles,
        "analysis_results": analysis_results
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)