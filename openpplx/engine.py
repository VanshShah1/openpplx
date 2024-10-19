from g4f.client import Client
import requests
from bs4 import BeautifulSoup
from googlesearch import search

client = Client()

system_prompt = """You are helpful assistant that can answer questions and help with tasks. You can use web context to help you answer questions."""

# Add this new list to store conversation history
conversation_history = []

def search_web(query: str):
   search_results = next(search(f"{query} articles, information.", lang='en'))
   return search_results

def scrape_text(url):

  try:
    response = requests.get(url)
    response.raise_for_status() 
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text(strip=True)
    return text
  except requests.exceptions.RequestException as e:
    print(f"Error: {e}")

def generate(prompt: str):
    link = search_web(prompt)
    web_context = scrape_text(link)
    
    # Add the user's prompt to the conversation history
    conversation_history.append({"role": "user", "content": prompt})
    
    # Prepare the messages for the API request
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"User prompt: {prompt} \nWeb context: {web_context}"}#\nWeb context: {web_context}
    ] + conversation_history
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    res = response.choices[0].message.content
    
    # Add the AI's response to the conversation history
    conversation_history.append({"role": "assistant", "content": res})
    result = {'link': link, 'response': res}
    return result