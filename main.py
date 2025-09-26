from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from dotenv import load_dotenv
from linkedin_agent import create_linkedin_agent, generate_post_from_topic
import os


load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY not found in .env file")
if not os.getenv("TAVILY_API_KEY"):
    raise ValueError("TAVILY_API_KEY not found in .env file")

app = FastAPI(
    title="AI-Powered LinkedIn Post Generator",
    description="An API service that uses Google Gemini and LangChain to generate LinkedIn posts from recent news on a given topic.",
    version="1.0.0"
)

linkedin_agent = create_linkedin_agent()


class PostRequest(BaseModel):
    """Request model for the /generate-post endpoint."""
    topic: str


class PostResponse(BaseModel):
    """Response model for the /generate-post endpoint."""
    topic: str
    news_sources: List[str]
    linkedin_post: str
    image_suggestion: Optional[str] = None


@app.post("/generate-post", response_model=PostResponse)
async def generate_post(request: PostRequest):
    """
    Receives a topic, fetches recent news, and generates a LinkedIn-style post.
    """
    try:
        linkedin_post, news_sources = generate_post_from_topic(
            linkedin_agent, request.topic)

        if not linkedin_post:
            raise HTTPException(
                status_code=500, detail="Failed to generate LinkedIn post. The agent returned an empty response.")

        image_suggestion = f"A professional image related to '{request.topic}'"

        return PostResponse(
            topic=request.topic,
            news_sources=news_sources,
            linkedin_post=linkedin_post,
            image_suggestion=image_suggestion
        )
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
