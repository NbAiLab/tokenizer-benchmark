# Benchmark for Scandinavian Language Tokenizers
This repo provides tools for evaluating the efficiency of various tokenizers for Swedish, Danish, Norwegian Bokmål and  Norwegian Nynorsk. It will also support English for comparison. Here we meassyre the tokenizer efficiency by tokenizing a total of 100k words from the top 500 Wikipedia pages for this language.

Tokenizer efficincy, E, can be defined as the ratio of the total number of words to the total number of tokens, multiplied by 100 to express it as a percentage:


Tokenizer efficiancy: ![Tokenizer Efficiency Formula](images/efficiency.png) 

Tokenizer efficiency: <img src="images/efficiency.png" alt="Tokenizer Efficiency Formula" style="vertical-align: -5px;" />


### Scandinavian Tokenizers

| tokenizer                                                                               | type          | vocab_size   |   da |   en |   nn |   no |   sv | Average Efficiency   |
|:----------------------------------------------------------------------------------------|:--------------|:-------------|-----:|-----:|-----:|-----:|-----:|:---------------------|
| [MBart](https://hf.co/facebook/mbart-large-en-ro)                                       | SentencePiece | 250,027      |   67 |   74 |   63 |   67 |   65 | 68.0%                |
| [Gemma](https://hf.co/google/gemma-7b)                                                  | SentencePiece | 256,000      |   61 |   81 |   60 |   61 |   60 | 65.0%                |
| [norMistral](https://hf.co/norallm/normistral-7b-scratch)                               | BPE           | 32,768       |   62 |   62 |   66 |   70 |   52 | 62.9%                |
| [mT5](https://hf.co/google/mt5-small)                                                   | SentencePiece | 250,100      |   60 |   69 |   58 |   60 |   58 | 61.7%                |
| [GPT-J](https://hf.co/EleutherAI/gpt-j-6b)                                              | BPE           | 50,257       |   49 |   89 |   48 |   50 |   46 | 56.8%                |
| [GPT2](https://hf.co/gpt2)                                                              | BPE           | 50,257       |   49 |   89 |   48 |   50 |   46 | 56.8%                |
| [Roberta](https://hf.co/roberta-base)                                                   | BPE           | 50,265       |   49 |   89 |   48 |   50 |   46 | 56.8%                |
| [NB-GPT-J](https://hf.co/NbAiLab/nb-gpt-j-6B-v2)                                        | BPE           | 50,257       |   49 |   89 |   48 |   50 |   46 | 56.8%                |
| [Llama](https://hf.co/meta-llama/Llama-2-7b-hf)                                         | BPE           | 32,000       |   49 |   71 |   49 |   49 |   50 | 54.1%                |
| [Mistral](https://hf.co/mistralai/Mistral-7B-Instruct-v0.2)                             | BPE           | 32,000       |   48 |   72 |   48 |   48 |   48 | 53.3%                |
| [KBLab-Megatron](https://hf.co/KBLab/megatron.bert-large.unigram-64k-pretok.500k-steps) | WordPiece     | 64,005       |   45 |   52 |   45 |   45 |   61 | 50.1%                |


### Not Fully Supported Tokenizers

| tokenizer                                                 | type          | vocab_size   | scand_test   | nordic_test   | eng_test   | Average Efficiency   |
|:----------------------------------------------------------|:--------------|:-------------|:-------------|:--------------|:-----------|:---------------------|
| [NB-BERT](https://hf.co/NbAiLab/nb-bert-large)            | WordPiece     | 50,000       | OK (lower)   | Failed        | OK (lower) | 86.0%                |
| [norT5](https://hf.co/ltg/nort5-base)                     | SentencePiece | 50,000       | Failed       | Failed        | Failed     | 82.5%                |
| [mBERT](https://hf.co/bert-base-multilingual-uncased)     | WordPiece     | 105,879      | Failed       | Failed        | OK (lower) | 72.8%                |
| [KBLab-BERT](https://hf.co/KBLab/bert-base-swedish-cased) | WordPiece     | 50,325       | Failed       | Failed        | Success    | 63.2%                |
| [Bert](https://hf.co/bert-base-uncased)                   | WordPiece     | 30,522       | Failed       | Failed        | OK (lower) | 52.3%                |
| [DistilBert](https://hf.co/distilbert-base-uncased)       | WordPiece     | 30,522       | Failed       | Failed        | OK (lower) | 52.3%                |
| [LayoutLM](https://hf.co/microsoft/layoutlm-base-uncased) | WordPiece     | 30,522       | Failed       | Failed        | OK (lower) | 52.3%                |
| [XLNet](https://hf.co/xlnet-base-cased)                   | SentencePiece | 32,000       | Failed       | Failed        | Success    | 41.0%                |
| [T5](https://hf.co/t5-base)                               | SentencePiece | 32,100       | Failed       | Failed        | Success    | 36.9%                |


# sample_wikipedia.py
This script creates a corpus for Wikipedia articles for the defined set of languages. It is a tool for creating the tokenization benchmark. It extracts the first 200 words from each article on a specified date. Articles shorter than 200 words are dropped. In the default mode it samples until it has reached 100k words.

To create the corpus files, run the command below:
```bash
for lang in en no nn da sv; do python sample_wikipedia.py --language $lang --output_file wikipedia_100k/wiki_$lang.txt --num_articles 500 --num_words 200;done
for lang in en no nn da sv; do python sample_wikipedia.py --language $lang --output_file wikipedia_1k/wiki_$lang.txt --num_articles 50 --num_words 20;done
```

# run_test.py
This script runs the test and creates the tables in this document.

```bash
python run_test.py
```

# Faster test run
python run_test.py --directory wikipedia_1k/
```



