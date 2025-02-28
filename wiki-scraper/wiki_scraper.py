import requests
from bs4 import BeautifulSoup
import re
import os

def get_wikipedia_body_content(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to fetch the page. Status code: {response.status_code}")
        return "", ""

    soup = BeautifulSoup(response.text, "html.parser")

    # Extract the title (topic) of the Wikipedia page
    page_title = soup.find("h1", {"id": "firstHeading"}).get_text().strip()

    # Find the content section (main article body)
    content_section = soup.find("div", {"class": "mw-parser-output"})
    
    # Extract all body content as text (without references), split into sentences
    body_content = ""
    sentence_number = 1  # For numbering sentences
    if content_section:
        for para in content_section.find_all("p"):  # All paragraphs
            para_text = para.get_text().strip()
            # Remove references like [34], [a], etc.
            para_text_cleaned = re.sub(r'\[\d+\]|\[\w+\]', '', para_text)  # Remove square bracketed references
            
            # Split the paragraph into sentences and add them to body content with numbering
            sentences = re.split(r'(?<=[.!?])\s+', para_text_cleaned)  # Split based on punctuation marks
            for sentence in sentences:
                # Ensure that only non-empty sentences are added
                if sentence.strip():
                    body_content += f"{sentence_number}. {sentence.strip()}\n"
                    sentence_number += 1

    return page_title, body_content

def save_to_file(title, data):
    if not data:
        print("No data extracted! Check the Wikipedia page structure.")
        return

    # Sanitize the title for use in filenames (remove invalid characters)
    sanitized_title = re.sub(r'[\\/*?:"<>|]', "", title)
    
    # Create the filename based on the topic, e.g., "Python-summary.txt"
    filename = f"{sanitized_title}-summary.txt"

    # Write the title and body content to a text file
    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"Topic: {title}\n\n")  # Write the title at the top of the file
        file.write(data)  # Write the numbered sentences
    
    print(f"Body content successfully saved to {filename}")


# main
# Example: Scrape the "Python (programming language)" Wikipedia page
wiki_url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
page_title, body_content = get_wikipedia_body_content(wiki_url)

# Save results to a text file
save_to_file(page_title, body_content)

print("Process completed.")
