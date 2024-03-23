# Benchmark for Nordic Language Tokenizers
Will be supporting no, nn, sv, da and is, in addition to en for reference. Coming soon.

## sample_wikipedia.py
This script creates a corpus for Wikipedia articles for languages including English, Norwegian Bokmål, Norwegian Nynorsk, Danish, Swedish and Icelandic. It is a tool for creating the tokenization benchmark. It extracts the first 200 words from each article on a specified date. Articles shorter than 200 words are dropped. It samples until it has reached 1M words.
