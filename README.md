# Benchmark for Nordic Language Tokenizers
This repo provides tools for evaluating the efficiency of various tokenizers for Swedish, Danish, Norwegian Bokmål, Norwegian Nynorsk and Icelandic. For reference, it will also support English for comparison

### Nordic Tokenizers

| tokenizer                                                                               | vocab_size   |   da |   en |   nn |   no |   sv | Average Efficiency   |
|:----------------------------------------------------------------------------------------|:-------------|-----:|-----:|-----:|-----:|-----:|:---------------------|
| [MBart](https://hf.co/facebook/mbart-large-en-ro)                                       | 250,027      |   69 |   69 |   64 |   68 |   67 | 67.9%                |
| [mT5](https://hf.co/google/mt5-small)                                                   | 250,100      |   61 |   64 |   60 |   60 |   59 | 61.5%                |
| [Gemma](https://hf.co/google/gemma-7b)                                                  | 256,000      |   60 |   67 |   57 |   56 |   56 | 59.7%                |
| [norMistral](https://hf.co/norallm/normistral-7b-scratch)                               | 32,768       |   60 |   53 |   60 |   63 |   50 | 57.5%                |
| [GPT-J](https://hf.co/EleutherAI/gpt-j-6b)                                              | 50,257       |   49 |   74 |   49 |   48 |   47 | 53.8%                |
| [GPT2](https://hf.co/gpt2)                                                              | 50,257       |   49 |   74 |   49 |   48 |   47 | 53.8%                |
| [Roberta](https://hf.co/roberta-base)                                                   | 50,265       |   49 |   74 |   49 |   48 |   47 | 53.8%                |
| [NB-GPT-J](https://hf.co/NbAiLab/nb-gpt-j-6B-v2)                                        | 50,257       |   49 |   74 |   49 |   48 |   47 | 53.8%                |
| [Llama](https://hf.co/meta-llama/Llama-2-7b-hf)                                         | 32,000       |   47 |   58 |   48 |   45 |   49 | 49.7%                |
| [Mistral](https://hf.co/mistralai/Mistral-7B-Instruct-v0.2)                             | 32,000       |   46 |   59 |   47 |   44 |   46 | 48.6%                |
| [KBLab-Megatron](https://hf.co/KBLab/megatron.bert-large.unigram-64k-pretok.500k-steps) | 64,005       |   47 |   45 |   45 |   44 |   55 | 47.6%                |


### Not Fully Supported Tokenizers

| tokenizer                                                 | vocab_size   | scand_test   | nordic_test   | eng_test   | Average Efficiency   |
|:----------------------------------------------------------|:-------------|:-------------|:--------------|:-----------|:---------------------|
| [NB-BERT](https://hf.co/NbAiLab/nb-bert-large)            | 50,000       | OK (lower)   | Failed        | OK (lower) | 84.3%                |
| [norT5](https://hf.co/ltg/nort5-base)                     | 50,000       | Failed       | Failed        | Failed     | 76.6%                |
| [mBERT](https://hf.co/bert-base-multilingual-uncased)     | 105,879      | Failed       | Failed        | OK (lower) | 72.2%                |
| [KBLab-BERT](https://hf.co/KBLab/bert-base-swedish-cased) | 50,325       | Failed       | Failed        | Success    | 63.0%                |
| [Bert](https://hf.co/bert-base-uncased)                   | 30,522       | Failed       | Failed        | OK (lower) | 52.7%                |
| [DistilBert](https://hf.co/distilbert-base-uncased)       | 30,522       | Failed       | Failed        | OK (lower) | 52.7%                |
| [LayoutLM](https://hf.co/microsoft/layoutlm-base-uncased) | 30,522       | Failed       | Failed        | OK (lower) | 52.7%                |
| [XLNet](https://hf.co/xlnet-base-cased)                   | 32,000       | Failed       | Failed        | Success    | 41.3%                |
| [T5](https://hf.co/t5-base)                               | 32,100       | Failed       | Failed        | Success    | 37.0%                |
# sample_wikipedia.py
This script creates a corpus for Wikipedia articles for languages including English, Norwegian Bokmål, Norwegian Nynorsk, Danish, Swedish and Icelandic. It is a tool for creating the tokenization benchmark. It extracts the first 200 words from each article on a specified date. Articles shorter than 200 words are dropped. It samples until it has reached 100k words.

To create the corpus files, run the command below:
```bash
for lang in en no nn da sv; do python sample_wikipedia.py --language $lang --output_file wikipedia_100k/wiki_$lang.txt --num_articles 500 --num_words 200;done
for lang in en no nn da sv; do python sample_wikipedia.py --language $lang --output_file wikipedia_1k/wiki_$lang.txt --num_articles 50 --num_words 20;done
```

# run_test.py
This script runs the test and creates the tables in this document.

```bash
python run_test.py

# Faster test run
python run_test.py --directory wikipedia_1k/
```



