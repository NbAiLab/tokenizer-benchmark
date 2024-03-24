# Benchmark for Nordic Language Tokenizers
This repo provides tools for evaluating the efficiency of various tokenizers for Swedish, Danish, Norwegian Bokmål, Norwegian Nynorsk and Icelandic. For reference, it will also support English for comparison

### Nordic Tokenizers

| tokenizer               | vocab_size   | da    | en    | is    | nn    | no    | sv    | Average Efficiency   |
|:------------------------|:-------------|:------|:------|:------|:------|:------|:------|:---------------------|
| MBartTokenizer          | 250,027      | 67.7% | 75.0% | 56.4% | 63.4% | 67.9% | 65.8% | 66.0%                |
| GemmaTokenizer          | 256,000      | 61.4% | 81.4% | 42.4% | 61.0% | 61.1% | 60.4% | 61.3%                |
| mT5Tokenizer            | 250,100      | 60.6% | 69.8% | 49.1% | 58.9% | 61.0% | 58.2% | 59.6%                |
| LTG-norMistralTokenizer | 32,768       | 62.4% | 62.9% | 35.5% | 66.7% | 70.4% | 52.2% | 58.4%                |
| GPT-JTokenizer          | 50,257       | 50.0% | 89.6% | 34.7% | 48.4% | 50.0% | 46.0% | 53.1%                |
| GPT2Tokenizer           | 50,257       | 50.0% | 89.6% | 34.7% | 48.4% | 50.0% | 46.0% | 53.1%                |
| NB-GPT-J-Tokenizer      | 50,257       | 50.0% | 89.6% | 34.7% | 48.4% | 50.0% | 46.0% | 53.1%                |
| RobertaTokenizer        | 50,265       | 50.0% | 89.6% | 34.7% | 48.4% | 50.0% | 46.0% | 53.1%                |
| LlamaTokenizer          | 32,000       | 49.9% | 71.5% | 35.8% | 49.8% | 49.3% | 50.0% | 51.0%                |
| MistralTokenizer        | 32,000       | 48.5% | 72.8% | 34.7% | 48.6% | 48.1% | 48.2% | 50.2%                |
| KBLabMegatronTokenizer  | 64,005       | 45.8% | 52.2% | 29.5% | 45.6% | 45.6% | 61.2% | 46.6%                |


### Not Fully Supported Tokenizers

| tokenizer           | vocab_size   | scand_test   | nordic_test   | eng_test   | Average Efficiency   |
|:--------------------|:-------------|:-------------|:--------------|:-----------|:---------------------|
| NB-BERTTokenizer    | 50,000       | Lowercase    | Failed        | Lowercase  | 86.0%                |
| LTG-norT5Tokenizer  | 50,000       | Failed       | Failed        | Failed     | 82.5%                |
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
for lang in en no nn da is sv; do python sample_wikipedia.py --language $lang --output_file wikipedia_1k/wiki_$lang.txt --num_articles 50 --num_words 20;done
```

# run_test.py
This script runs the test and creates the tables in this document.

```bash
python run_test.py

# Faster test run
python run_test.py --directory wikipedia_1k/
```



