# Benchmark for Nordic Language Tokenizers
This repo provides tools for evaluating the efficiency of various tokenizers for Swedish, Danish, Norwegian Bokmål, Norwegian Nynorsk and Icelandic. For reference, it will also support English for comparison

## Nordic Tokenizers
| tokenizer             | vocab_size   |   da |   en |   nn |   no |   sv | Average Efficiency   |
|:----------------------|:-------------|-----:|-----:|-----:|-----:|-----:|:---------------------|
| MBartTokenizer        | 250,027      | 67.7 | 75   | 63.4 | 67.9 | 65.8 | 68.0%                |
| mT5Tokenizer          | 250,100      | 60.6 | 69.8 | 58.9 | 61.0 | 58.2 | 61.7%                |
| GPT2Tokenizer         | 50,257       | 50.0  | 89.6 | 48.4 | 50.0 | 46.0 | 56.8%                |
| GPT-JTokenizer        | 50,257       | 50.0 | 89.6 | 48.4 | 50.0 | 46.0 | 56.8%                |
| RobertaTokenizer      | 50,265       | 50.0 | 89.6 | 48.4 | 50.0 | 46.0 | 56.8%                |
| KBLaMegatronTokenizer | 64,005       | 45.8 | 52.2 | 45.6 | 45.6 | 61.2 | 50.1%                |


### Not Fully Working Nordic Tokenizers (inkl lowercase-only)

| tokenizer           | vocab_size   | scand_test   | nordic_test   | eng_test   | Average Efficiency   |
|:--------------------|:-------------|:-------------|:--------------|:-----------|:---------------------|
| NB-BERTTokenizer    | 50,000       | Lowercase    | Failed        | Lowercase  | 86.0%                |
| mBERTTokenizer      | 105,879      | Failed       | Failed        | Lowercase  | 72.8%                |
| KBLabBERTTokenizer  | 50,325       | Failed       | Failed        | Success    | 63.2%                |
| BertTokenizer       | 30,522       | Failed       | Failed        | Lowercase  | 52.3%                |
| DistilBertTokenizer | 30,522       | Failed       | Failed        | Lowercase  | 52.3%                |
| LayoutLMTokenizer   | 30,522       | Failed       | Failed        | Lowercase  | 52.3%                |
| XLNetTokenizer      | 32,000       | Failed       | Failed        | Success    | 41.0%                |
| T5Tokenizer         | 32,100       | Failed       | Failed        | Success    | 36.9%                |


# sample_wikipedia.py
This script creates a corpus for Wikipedia articles for languages including English, Norwegian Bokmål, Norwegian Nynorsk, Danish, Swedish and Icelandic. It is a tool for creating the tokenization benchmark. It extracts the first 200 words from each article on a specified date. Articles shorter than 200 words are dropped. It samples until it has reached 100k words.

To create the corpus files, run the command below:
```bash
for lang in en no nn da is sv; do python sample_wikipedia.py --language $lang --output_file wikipedia_100k/wiki_$lang.txt --num_articles 500 --num_words 200;done
for lang in en no nn da is sv; do python sample_wikipedia.py --language $lang --output_file wikipedia_10k/wiki_$lang.txt --num_articles 500 --num_words 20;done
for lang in en no nn da is sv; do python sample_wikipedia.py --language $lang --output_file wikipedia_1k/wiki_$lang.txt --num_articles 50 --num_words 20;done
```


