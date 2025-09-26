# AI-Powered LinkedIn Post Generator

Generate professional, engaging LinkedIn posts based on the latest news for any topic using FastAPI, Google Gemini API, and LangChain.

---

## ✨ Features

- **Dynamic Content Creation:** Generates unique LinkedIn posts on any topic.
- **Real-time News Aggregation:** Fetches the latest news using a web search tool.
- **AI Summarization:** Utilizes Google Gemini to summarize complex articles.
- **Robust API:** Built with FastAPI, providing high performance and interactive docs.
- **Source Attribution:** Returns URLs of the news sources used.

---

## 🛠️ Tech Stack

- **Backend:** FastAPI
- **LLM:** Google Gemini (`gemini-2.5-flash`)
- **Framework:** LangChain (Agents, Tools, Chains)
- **Web Search:** Tavily Search API
- **Language:** Python

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- Google API Key ([Google AI Studio](https://aistudio.google.com/))
- Tavily API Key ([Tavily AI](https://www.tavily.com/))

### 1. Clone the Repository

```sh
git clone <repository-url>
```

### 2. Create a Virtual Environment

```sh
python -m venv venv
```

Activate the environment:

- **Windows:**  
  ```sh
  .\venv\Scripts\activate
  ```
- **macOS/Linux:**  
  ```sh
  source venv/bin/activate
  ```

### 3. Install Dependencies

```sh
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY_HERE"
TAVILY_API_KEY="YOUR_TAVILY_API_KEY_HERE"
```

---

## ▶️ Running the Application

Start the FastAPI server:

```sh
uvicorn main:app --reload
```

- Server runs at: [http://localhost:8000](http://localhost:8000)
- Hot-reloading enabled with `--reload`

---

## 📖 API Usage

### Interactive Docs

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Endpoint: `POST /generate-post`

**Request Body:**

```json
{
  "topic": "Quantum Computing"
}
```

**Example with curl:**

```sh
curl -X 'POST' \
  'http://localhost:8000/generate-post' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"topic": "Quantum Computing"}'
```

**Sample Success Response:**

```json
{
  "topic": "Quantum Computing",
  "news_sources": [
    "https://www.forbes.com/sites/arthurherman/2024/05/29/the-quantum-tech-race-with-china-is-one-america-cant-afford-to-lose/",
    "https://www.euronews.com/next/2024/05/28/a-quantum-leap-finlands-first-quantum-computer-is-now-online-and-free-for-all-to-use"
  ],
  "linkedin_post": "The quantum realm is buzzing with excitement! ⚛️ ...",
  "image_suggestion": null
}
```

---

