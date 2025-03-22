# News Summarizer - First Release

This project fetches news articles for a given company, summarizes them, performs sentiment analysis, extracts topics, and generates Hindi TTS summaries. It uses a Flask backend for API processing, a Streamlit frontend for user interaction, and integrates with third-party APIs like NewsAPI and Google Gemini. The core logic is in `news_summarizer.py`, the backend is in `app.py`, and the frontend is in `frontend.py`.

## Project Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd news-summarizer
   ```

2. Set up a virtual environment (recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies using `poetry` (preferred) or `pip`:
   ```
   poetry install
   ```
   Or:
   ```
   pip install flask streamlit newsapi-python requests beautifulsoup4 google-generative-ai gtts python-dotenv
   ```

4. Create a `.env` file in the project root with your API keys:
   ```
   NEWSAPI_KEY=your-newsapi-key
   GEMINI_API_KEY=your-gemini-api-key
   ```
   Get your NewsAPI key from https://newsapi.org and your Gemini API key from Google Cloud Console.

5. Run the Flask backend:
   ```
   poetry run python app.py
   ```
   It will start on `http://localhost:5000`.

6. Run the Streamlit frontend in a separate terminal:
   ```
   poetry run streamlit run frontend.py
   ```
   It will open in your browser at `http://localhost:8501`.

## Model Details

### Summarization
- **Model**: Google Gemini (`gemini-1.5-flash`)
- **Details**: Summarizes articles into 2-3 sentences. The `generate_summary` function in `news_summarizer.py` sends article text to Gemini with a prompt to summarize. Gemini uses transformer-based embeddings for contextual understanding, outperforming traditional methods like extractive summarization.

### Sentiment Analysis
- **Model**: Google Gemini (`gemini-1.5-flash`)
- **Details**: Classifies article sentiment as Positive, Negative, or Neutral. The `analyze_sentiment` function in `news_summarizer.py` sends article text to Gemini with a prompt to classify sentiment. It leverages Gemini’s fine-tuned transformer models for accurate sentiment detection.

### Topic Extraction
- **Model**: Google Gemini (`gemini-1.5-flash`)
- **Details**: Extracts the top 5 key topics from each article. The `extract_topics` function in `news_summarizer.py` sends article text to Gemini, which returns a comma-separated list of topics. Gemini’s transformer-based approach provides better contextual topic identification than traditional methods like LDA.

### Text-to-Speech (TTS)
- **Library**: `gTTS` (Google Text-to-Speech)
- **Details**: Converts Hindi-translated summaries into audio files. The `generate_hindi_tts` function in `news_summarizer.py` uses `gTTS` to generate MP3 files. The `translate_to_hindi` function first translates English summaries to Hindi using Gemini. `gTTS` relies on Google’s TTS engine, supporting Hindi with WaveNet-based synthesis.

## API Development

The Flask backend exposes a `/summarize` endpoint to process news summarization requests. It can be accessed via tools like Postman or integrated with the Streamlit frontend.

### API Endpoint
- **Endpoint**: `/summarize`
- **Method**: `POST`
- **URL**: `http://localhost:5000/summarize`
- **Request Body** (JSON):
  ```
  {
      "Company": "Tesla"
  }
  ```
- **Response** (JSON):
  ```
  {
      "Company": "Tesla",
      "Articles": [
          {
              "Title": "Tesla Faces New Challenges in 2025",
              "Summary": "Tesla is facing new challenges in 2025 due to increased competition and regulatory hurdles.",
              "Sentiment": "Negative",
              "Topics": ["Tesla", "competition", "regulations", "market share", "autonomous driving"],
              "HindiTTSFile": "http://localhost:5000/audio/summary_1.mp3"
          },
          {
              "Title": "Tesla's New Model Breaks Sales Records",
              "Summary": "Tesla's latest EV sees record sales in Q3, boosting investor confidence.",
              "Sentiment": "Positive",
              "Topics": ["Tesla", "electric vehicles", "stock market", "innovation"],
              "HindiTTSFile": "http://localhost:5000/audio/summary_2.mp3"
          }
      ],
      "Comparative Sentiment Score": {
          "Sentiment Distribution": {
              "Positive": 1,
              "Negative": 1,
              "Neutral": 0
          },
          "Coverage Differences": [
              {
                  "Comparison": "Article 1 (Negative) vs Article 2 (Positive)",
                  "Impact": "Focus: Tesla, competition vs Tesla, electric vehicles"
              }
          ],
          "Topic Overlap": {
              "Common Topics": ["Tesla"],
              "Unique Topics in Article 1": ["competition", "regulations", "market share", "autonomous driving"],
              "Unique Topics in Article 2": ["electric vehicles", "stock market", "innovation"]
          }
      },
      "Final Sentiment Analysis": "Tesla’s latest news coverage is balanced. Mixed impact on stock expected.",
      "Audio": "[Play Hindi Speech]"
  }
  ```

### Accessing the API via Postman
1. Install Postman from https://www.postman.com/downloads/.
2. Create a new request in Postman.
3. Configure the request:
   - Method: `POST`
   - URL: `http://localhost:5000/summarize`
   - Headers:
     - Key: `Content-Type`
     - Value: `application/json`
   - Body (raw JSON):
     ```
     {
         "Company": "Tesla"
     }
     ```
4. Send the request by clicking "Send". The response includes summaries, sentiment analysis, and Hindi TTS audio links.
5. To play the audio, copy the `HindiTTSFile` URL (e.g., `http://localhost:5000/audio/summary_1.mp3`), create a new `GET` request in Postman, paste the URL, and send to download the MP3 file.

## API Usage

### NewsAPI
- **Purpose**: Fetches news articles for a given company from NPR.
- **Integration**:
  - API Key: Required (sign up at https://newsapi.org).
  - Endpoint: `https://newsapi.org/v2/everything`
  - Parameters: `q` (company name), `domains` (npr.org), `language` (en), `sort_by` (publishedAt), `page_size` (10).
  - Implementation: The `fetch_news_articles` function in `news_summarizer.py` uses the `newsapi-python` library to fetch articles.
- **Usage**: Returns article titles, URLs, and descriptions for further processing.

### Google Gemini API
- **Purpose**: Handles summarization, sentiment analysis, topic extraction, and Hindi translation.
- **Integration**:
  - API Key: Required (generate from Google Cloud Console).
  - Model: `gemini-1.5-flash`
  - Implementation:
    - `generate_summary`: Summarizes articles.
    - `analyze_sentiment`: Classifies sentiment.
    - `extract_topics`: Extracts topics.
    - `translate_to_hindi`: Translates summaries to Hindi.
  - Usage: The `google-generative-ai` library sends prompts to Gemini and processes responses.
- **Cost**: Usage may incur costs (check Google Cloud pricing).

### Google Text-to-Speech (gTTS)
- **Purpose**: Converts Hindi summaries into audio files.
- **Integration**:
  - Library: `gtts`
  - Implementation: The `generate_hindi_tts` function in `news_summarizer.py` generates MP3 files.
  - Usage: Requires an internet connection. No API key needed.

## Assumptions & Limitations

### Assumptions
- NewsAPI will return articles for the given company from NPR.
- NPR articles have a `div` with `id="storytext"` for content extraction.
- Gemini API returns valid responses for summarization, sentiment analysis, topic extraction, and translation.
- The system has internet access for NewsAPI, Gemini API, and gTTS.
- Gemini can accurately translate English summaries to Hindi.

### Limitations
- Fetches only 10 articles per request (configurable but limited by NewsAPI rate limits).
- Relies on NPR (`npr.org`) for articles; no results if NPR lacks recent articles.
- Gemini API usage may incur costs and has rate limits.
- Hindi TTS quality depends on `gTTS` and may not be perfect for complex sentences.
- Unexpected API failures (e.g., NewsAPI downtime) may cause errors.
- Flask backend isn’t optimized for high traffic; consider a WSGI server for production.
- TTS audio files accumulate in the project directory without cleanup.
