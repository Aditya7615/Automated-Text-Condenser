# Import the libraries
import os
import pandas as pd
from bs4 import BeautifulSoup
import requests
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import re
import time
import random

# --- Change: Using relative paths for portability ---
POSITIVE_WORDS_FILE = 'MasterDictionary/positive-words.txt'
NEGATIVE_WORDS_FILE = 'MasterDictionary/negative-words.txt'
STOPWORDS_DIR = 'StopWords'
OUTPUT_FILE = 'Output.csv'

def load_stop_words(stopwords_dir):
    """Loads stop words from all .txt files in a directory."""
    stopwords = set()
    try:
        for filename in os.listdir(stopwords_dir):
            if filename.endswith('.txt'):
                with open(os.path.join(stopwords_dir, filename), 'r', encoding='latin-1') as file:
                    stopwords.update(word.strip().lower() for word in file.readlines())
    except FileNotFoundError:
        print(f"Error: Stopwords directory not found at '{stopwords_dir}'")
    return stopwords

def load_sentiment_words(file_path, stopwords):
    """Loads sentiment words, excluding any stopwords."""
    try:
        with open(file_path, 'r', encoding='latin-1') as file:
            return {word.strip() for word in file if word.strip().lower() not in stopwords}
    except FileNotFoundError:
        print(f"Error: Sentiment file not found at '{file_path}'")
        return set()

def extract_article_text(url):
    """Retrieves article text from URL using BeautifulSoup."""
    # --- Change: Added headers to mimic a browser ---
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        title_tag = soup.find('h1') or soup.find('title')
        title = title_tag.get_text().strip() if title_tag else "No Title Found"

        article_content = soup.find('div', class_='td-post-content') or soup.find('article')

        if not article_content:
            text = soup.get_text()
        else:
            text = article_content.get_text()

        # Clean up text
        cleaned_text = '\n'.join(line.strip() for line in text.splitlines() if line.strip())
        return title, cleaned_text

    except requests.exceptions.RequestException as e:
        print(f"Error fetching article from {url}: {e}")
        return None, None

def count_syllables(word):
    """Counts syllables in a word, handling common exceptions."""
    word = word.lower().strip()
    if not word:
        return 0
    # Words ending in "es" or "ed" are not counted as syllables
    if word.endswith(('es', 'ed')):
        word = word[:-2]

    vowels = "aeiouy"
    syllable_count = 0
    if word and word[0] in vowels:
        syllable_count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            syllable_count += 1

    # A word must have at least one syllable
    return max(1, syllable_count)

def calculate_text_metrics(text, stopwords, positive_dict, negative_dict):
    """Calculates all text analysis metrics."""
    # Tokenize sentences and clean/tokenize words
    sentences = sent_tokenize(text)
    words = [word.lower() for word in word_tokenize(text) if word.isalpha() and word.lower() not in stopwords]

    # --- Change: Handle cases with no words to prevent errors ---
    if not words or not sentences:
        return {
            'POSITIVE SCORE': 0, 'NEGATIVE SCORE': 0, 'POLARITY SCORE': 0,
            'SUBJECTIVITY SCORE': 0, 'AVG SENTENCE LENGTH': 0,
            'PERCENTAGE OF COMPLEX WORDS': 0, 'FOG INDEX': 0,
            'AVG NUMBER OF WORDS PER SENTENCE': 0, 'COMPLEX WORD COUNT': 0,
            'WORD COUNT': 0, 'SYLLABLE PER WORD': 0, 'PERSONAL PRONOUNS': 0,
            'AVG WORD LENGTH': 0
        }

    word_count = len(words)
    sentence_count = len(sentences)

    # Calculate scores
    positive_score = sum(1 for word in words if word in positive_dict)
    negative_score = sum(1 for word in words if word in negative_dict)
    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
    subjectivity_score = (positive_score + negative_score) / (word_count + 0.000001)

    # Readability and complexity metrics
    avg_sentence_length = word_count / sentence_count
    complex_words = [word for word in words if count_syllables(word) > 2]
    complex_word_count = len(complex_words)
    percentage_of_complex_words = complex_word_count / word_count
    fog_index = 0.4 * (avg_sentence_length + percentage_of_complex_words)

    # Other metrics
    syllable_per_word = sum(count_syllables(word) for word in words) / word_count
    personal_pronouns = len(re.findall(r'\b(I|we|my|ours|us)\b', text, re.I))
    avg_word_length = sum(len(word) for word in words) / word_count

    return {
        'POSITIVE SCORE': positive_score,
        'NEGATIVE SCORE': negative_score,
        'POLARITY SCORE': polarity_score,
        'SUBJECTIVITY SCORE': subjectivity_score,
        'AVG SENTENCE LENGTH': avg_sentence_length,
        'PERCENTAGE OF COMPLEX WORDS': percentage_of_complex_words,
        'FOG INDEX': fog_index,
        'AVG NUMBER OF WORDS PER SENTENCE': avg_sentence_length,
        'COMPLEX WORD COUNT': complex_word_count,
        'WORD COUNT': word_count,
        'SYLLABLE PER WORD': syllable_per_word,
        'PERSONAL PRONOUNS': personal_pronouns,
        'AVG WORD LENGTH': avg_word_length
    }

def main():
    """Main function to execute the analysis."""
    # Download nltk data if not present
    try:
        nltk.data.find('tokenizers/punkt')
    except nltk.downloader.DownloadError:
        print("Downloading 'punkt' for tokenization...")
        nltk.download('punkt')

    stopwords = load_stop_words(STOPWORDS_DIR)
    positive_dict = load_sentiment_words(POSITIVE_WORDS_FILE, stopwords)
    negative_dict = load_sentiment_words(NEGATIVE_WORDS_FILE, stopwords)

    try:
        input_df = pd.read_excel('Input.xlsx')
    except FileNotFoundError:
        print("Error: 'Input.xlsx' not found. Please ensure it is in the same directory.")
        return

    # --- Change: Logic to resume progress ---
    if os.path.exists(OUTPUT_FILE):
        output_df = pd.read_csv(OUTPUT_FILE)
        processed_urls = set(output_df['URL'])
    else:
        output_df = pd.DataFrame()
        processed_urls = set()
    
    # --- Change: Collect results in a list for efficiency ---
    results = []

    for _, row in input_df.iterrows():
        url_id = row['URL_ID']
        url = row['URL']

        if url in processed_urls:
            print(f"Skipping already processed URL: {url_id}")
            continue

        print(f"Processing URL: {url_id} - {url}")

        # --- Change: Added delay to be respectful to server ---
        time.sleep(random.uniform(1, 3))

        title, text = extract_article_text(url)
        if text is None:
            print(f"Skipping URL due to fetch error: {url_id}")
            continue

        metrics = calculate_text_metrics(text, stopwords, positive_dict, negative_dict)
        metrics['URL_ID'] = url_id
        metrics['URL'] = url
        results.append(metrics)

    # --- Change: Create DataFrame from results list and save ---
    if results:
        new_results_df = pd.DataFrame(results)
        output_df = pd.concat([output_df, new_results_df], ignore_index=True)

    output_df.to_csv(OUTPUT_FILE, index=False)
    print(f"\nProcessing complete. Results saved to '{OUTPUT_FILE}'.")

if __name__ == "__main__":
    main()