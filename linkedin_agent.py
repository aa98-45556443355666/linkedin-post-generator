import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import AgentType, initialize_agent
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory


def create_linkedin_agent():
    """
    Initializes and returns a LangChain agent powered by Google's Gemini model.
    """
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)
    search_tool = TavilySearchResults(
        max_results=3, description="A search engine optimized for comprehensive, accurate, and trusted results.")
    tools = [search_tool]

    prompt_template = """
    You are a highly skilled LinkedIn content creator. Your task is to generate a professional and engaging LinkedIn post based on the latest news about the topic provided in the user's input.

    Here is your workflow:
    1.  Analyze the user's request to identify the core topic.
    2.  Use your search tool to find 2-3 of the most recent, relevant news articles or blog posts about this topic.
    3.  Read and analyze the search results to understand the key takeaways and latest developments.
    4.  Synthesize the information and write a LinkedIn post that is:
        -   **Engaging:** Start with a strong hook to grab attention.
        -   **Informative:** Summarize the key news or findings.
        -   **Professional:** Maintain a business-appropriate tone.
        -   **Concise:** Keep it easy to read, ideally under 200 words.
        -   **Action-oriented:** End with a question or a call to action to encourage engagement.
    5.  Include 3-5 relevant hashtags at the end of the post.
    6.  You do not need to list the source URLs in your final answer, as they will be extracted automatically. Focus only on writing the best possible post.

    Here is the information you have from previous conversations:
    {chat_history}

    Here is the user's request:
    {input}

    Your final response must be only the LinkedIn post text.
    """

    prompt = PromptTemplate(
        input_variables=["chat_history", "input"],
        template=prompt_template
    )

    memory = ConversationBufferMemory(
        memory_key="chat_history", return_messages=True)

    agent_executor = initialize_agent(
        tools,
        llm,
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        memory=memory,
        prompt=prompt,
        verbose=True,
        handle_parsing_errors=True,
        return_intermediate_steps=True
    )

    return agent_executor


def generate_post_from_topic(agent_executor, topic):
    """
    Takes a topic, runs the agent, and reliably extracts both the generated post
    and the news sources from the agent's intermediate steps.
    """
    response = agent_executor.invoke({
        "input": f"Generate a LinkedIn post about the latest news on {topic}"
    })

    linkedin_post = response.get('output', '').strip()

    news_sources = []
    intermediate_steps = response.get('intermediate_steps', [])

    source_urls = set()

    for step in intermediate_steps:
        observation = step[1]
        if isinstance(observation, list):
            for result in observation:
                if isinstance(result, dict) and 'url' in result:
                    source_urls.add(result['url'])

    news_sources = list(source_urls)

    return linkedin_post, news_sources
