import requests
import argparse
import re
from datetime import datetime

def fetch_top_articles(date, language='en'):
    headers = {'User-Agent': 'WikipediaPopularArticlesFetcher/1.0 (your_email@example.com)'}
    base_url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/top/{language}.wikipedia.org/all-access/{date}"
    response = requests.get(base_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        articles = data['items'][0]['articles']
        return [article['article'] for article in articles]
    else:
        print(f"Failed to fetch popular articles for {date}. HTTP Status Code: {response.status_code}")
        return []

def fetch_article_content(title, language='en'):
    headers = {'User-Agent': 'WikipediaPopularArticlesFetcher/1.0 (your_email@example.com)'}
    params = {
        'action': 'query',
        'format': 'json',
        'titles': title,
        'prop': 'extracts',
        'explaintext': True,
    }
    base_url = f"https://{language}.wikipedia.org/w/api.php"
    response = requests.get(base_url, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        page = next(iter(data['query']['pages'].values()))
        if 'extract' in page:
            return page['extract']
    return ""

def extract_first_n_words(text, n=100):
    words = re.findall(r'\b\w+\b|[,.!?;]', text)
    return ' '.join(words[:n])

def main():
    parser = argparse.ArgumentParser(description='Fetch and extract the first N words of the top Wikipedia articles.')
    parser.add_argument('--date', type=str, default='2024/01/01', help='Date in YYYY/MM/DD format for fetching articles')
    parser.add_argument('--language', type=str, default='en', help='Wikipedia language edition (default: en)')
    parser.add_argument('--num_articles', type=int, default=500, help='Number of valid articles to fetch (default: 500)')
    parser.add_argument('--num_words', type=int, default=200, help='Minimum number of words per article (default: 200)')
    parser.add_argument('--output_file', type=str, default=None, help='File to write the extracted text (default: wiki_{lang}.txt)')
    args = parser.parse_args()

    # Set default output file name if not provided
    if args.output_file is None:
        args.output_file = f"wiki_{args.language}.txt"

    # Open (and clear) the output file at the beginning
    with open(args.output_file, 'w') as file:
        pass

    top_articles = fetch_top_articles(args.date, args.language)
    valid_articles_count = 0
    total_word_count = 0
    articles_processed = 0

    for title in top_articles:
        articles_processed += 1
        if valid_articles_count >= args.num_articles:
            break
        content = fetch_article_content(title, args.language)
        if content:
            first_n_words = extract_first_n_words(content, args.num_words)
            word_count = len(first_n_words.split())
            if word_count >= args.num_words:
                valid_articles_count += 1
                total_word_count += word_count
                with open(args.output_file, 'a') as file:
                    file.write(first_n_words + '\n')

    print(f"Successfully extracted texts for {valid_articles_count} articles in {args.language} with a total of {total_word_count} words, after processing {articles_processed} articles.")

if __name__ == "__main__":
    main()

