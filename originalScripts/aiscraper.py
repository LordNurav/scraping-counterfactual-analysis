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

# Load environment variables
load_dotenv()

AZURE_OPENAI_ENDPOINT = os.getenv('openai_endpoint')
AZURE_OPENAI_API_KEY = os.getenv('openai_api_key')
GPT_DEPLOYMENT_NAME1 = os.getenv('gpt_deployment_name1')
GPT_DEPLOYMENT_NAME2 = os.getenv('gpt_deployment_name2')

# Set up Azure OpenAI client
openai.api_type = 'azure'
openai.api_key = AZURE_OPENAI_API_KEY
openai.api_base = AZURE_OPENAI_ENDPOINT

# Scrape web content
def scrape_webpage(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        text = ' '.join(p.get_text() for p in soup.find_all('p'))
        if not text.strip():  # Check if text is empty after stripping
            raise ValueError("Failed to scrape content from the webpage.")
        return text
    except (requests.RequestException, ValueError) as e:
        print(f"Error: {e}")
        return "Failed to scrape content from the webpage."

# Create LangChain retriever
def create_langchain_retriever(documents):
    embeddings = AzureOpenAIEmbeddings(
        model="text-embedding-ada-002",
        deployment=GPT_DEPLOYMENT_NAME1,
        openai_api_key=AZURE_OPENAI_API_KEY,
        openai_api_base=AZURE_OPENAI_ENDPOINT
    )
    vector_store = FAISS.from_documents(documents, embeddings)
    retriever = vector_store.as_retriever()
    return retriever

# Summarize content
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

# Main function
def main(url):
    content = scrape_webpage(url)
    if content == "Failed to scrape content from the webpage.":
        return content

    document = Document(page_content=content, metadata={"source": url})
    retriever = create_langchain_retriever([document])
    summary = summarize_content(content)
    return summary

if __name__ == "__main__":
    url = "https://apnews.com/article/us-intelligence-services-ai-models-9471e8c5703306eb29f6c971b6923187"  # Replace with your target URL
    summary = main(url)
    print("Summary:", summary)
