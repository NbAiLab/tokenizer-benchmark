# Benchmark for Nordic Language Tokenizers
When ready the benchmark will be supporting Swedish, Danish, Norwegian Bokmål, Norwegian Nynorsk and Icelandic. For reference, it will also support English. 

## sample_wikipedia.py
This script creates a corpus for Wikipedia articles for languages including English, Norwegian Bokmål, Norwegian Nynorsk, Danish, Swedish and Icelandic. It is a tool for creating the tokenization benchmark. It extracts the first 200 words from each article on a specified date. Articles shorter than 200 words are dropped. It samples until it has reached 100k words.

To create the corpus files, run the command below:
```bash
for lang in en no nn da is sv; do python sample_wikipedia.py --language $lang --output_file wikipedia_100k/wiki_$lang.text --num_articles 500 --num_words 200;done
for lang in en no nn da is sv; do python sample_wikipedia.py --language $lang --output_file wikipedia_10k/wiki_$lang.text --num_articles 500 --num_words 20;done
for lang in en no nn da is sv; do python sample_wikipedia.py --language $lang --output_file wikipedia_1k/wiki_$lang.text --num_articles 50 --num_words 20;done
```


