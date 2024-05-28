import os
import openai
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import AzureOpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.schema import Document
from langchain_community.llms import AzureOpenAI
import sys

# Load environment variables
load_dotenv()

AZURE_OPENAI_ENDPOINT = os.getenv('openai_endpoint')
AZURE_OPENAI_API_KEY = os.getenv('openai_api_key')
GPT_DEPLOYMENT_NAME1 = os.getenv('gpt_deployment_name1')
GPT_DEPLOYMENT_NAME2 = os.getenv('gpt_deployment_name2')

# Set up Azure OpenAI client
openai.api_base = AZURE_OPENAI_ENDPOINT
openai.api_key = AZURE_OPENAI_API_KEY

def scrape_webpage(html_content):
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        text = ' '.join(p.get_text() for p in soup.find_all('p'))
        if not text.strip():  # Check if text is empty after stripping
            raise ValueError("Failed to scrape content from the webpage.")
        return text
    except ValueError as e:
        print(f"Error: {e}")
        return "Failed to scrape content from the webpage."

def summarize_content(content):
    azure_openai = AzureOpenAI(
        model="gpt-35-turbo",
        deployment_name=GPT_DEPLOYMENT_NAME2,
        api_version="2022-12-01",
        openai_api_key=AZURE_OPENAI_API_KEY,
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        temperature=0
    )

    prompt_template = """
    You are a highly intelligent summarization AI. Please read the following content and provide a clear, concise summary of all key details.

    Content: {content}

    Summary:
    """

    prompt = prompt_template.format(content=content)

    response = azure_openai(prompt)
    return response

def main(html_content):
    content = scrape_webpage(html_content)
    if content == "Failed to scrape content from the webpage.":
        return content

    document = Document(page_content=content, metadata={"source": "generated_html"})
    summary = summarize_content(content)
    return summary

if __name__ == "__main__":
    html_content = sys.stdin.read()  # Read HTML content from stdin
    summary = main(html_content)
    print(summary)
