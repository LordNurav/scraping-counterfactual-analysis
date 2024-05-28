import os
import openai
import random
import json
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from langchain_community.llms import AzureOpenAI

# Load environment variables
load_dotenv()

AZURE_OPENAI_ENDPOINT = os.getenv('openai_endpoint')
AZURE_OPENAI_API_KEY = os.getenv('openai_api_key')
GPT_DEPLOYMENT_NAME2 = os.getenv('gpt_deployment_name2')

# Initialize OpenAI client
openai.api_base = AZURE_OPENAI_ENDPOINT
openai.api_key = AZURE_OPENAI_API_KEY

def generate_cohesive_content(prompt):
    azure_openai = AzureOpenAI(
        model="gpt-35-turbo",
        deployment_name=GPT_DEPLOYMENT_NAME2,
        api_version="2022-12-01",
        openai_api_key=AZURE_OPENAI_API_KEY,
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        temperature=0.7  # Add some randomness to the content generation
    )
    
    final_prompt = "You are a highly intelligent article writer." + prompt
    response = azure_openai(final_prompt)
    return response

def generate_webpage_sections(target_data):
    # Read the modification factor from a configuration file
    with open('config.json', 'r') as file:
        config = json.load(file)
    modification_factor = config.get('modification_factor', 1)

    prompts = [
        "Write an introduction about the importance of data privacy in the modern digital age.",
        "Write the main points discussing various aspects of data privacy, including its benefits and challenges.",
        "Write a conclusion summarizing the key takeaways about data privacy and its significance.",
        "Provide examples of data privacy breaches and their impact.",
        "Discuss future trends in data privacy and protection measures."
    ]

    random.shuffle(prompts)  # Randomize the order of prompts to vary the content

    sections = []
    for prompt in prompts[:3]:  # Use only three prompts to ensure variation
        section_content = generate_cohesive_content(prompt)
        sections.append(section_content)

    # Combine sections into an HTML structure
    html_content = "<html><body>"
    for section in sections:
        html_content += f"<section><p>{section}</p></section>"
    html_content += "</body></html>"

    # Parse the HTML to insert the target data
    soup = BeautifulSoup(html_content, 'html.parser')
    sections = soup.find_all('section')

    if sections:
        insertion_point = random.randint(0, len(sections) - 1)
        section_content = sections[insertion_point].get_text()
        # Insert the target data into the middle of the selected section
        insertion_index = len(section_content) // (2 + modification_factor)
        updated_section_content = section_content[:insertion_index] + f" {target_data} " + section_content[insertion_index:]
        sections[insertion_point].string = updated_section_content
    else:
        soup.append(soup.new_tag("section"))
        soup.section.append(target_data)
    
    webpage_content = str(soup)
    return webpage_content

if __name__ == "__main__":
    target_data = "Target data has been proven difficult to hide."
    webpage = generate_webpage_sections(target_data)
    print(webpage)
