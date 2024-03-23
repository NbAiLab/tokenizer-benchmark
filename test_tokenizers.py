import argparse
import jsonlines
import warnings
from transformers import AutoTokenizer
import os
import glob

# Suppress specific warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="transformers.models.t5.tokenization_t5_fast")
warnings.filterwarnings("ignore", category=UserWarning, module="transformers.convert_slow_tokenizer")

def test_tokenizer_string(tokenizer, test_string):
    tokens = tokenizer.tokenize(test_string)
    token_ids = tokenizer.convert_tokens_to_ids(tokens)
    decoded_string = tokenizer.decode(token_ids, skip_special_tokens=True, clean_up_tokenization_spaces=True)
    exact_match = test_string == decoded_string
    lowercase_match = test_string.lower() == decoded_string.lower()

    if exact_match and lowercase_match:
        return "Success"
    elif not exact_match and lowercase_match:
        return "Lowercase"
    else:
        return "Failed"

def calculate_efficiency(tokenizer, directory, tokenizer_name):
    file_paths = glob.glob(os.path.join(directory, '*.txt'))
    breakpoint()
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            tokens = tokenizer.tokenize(text)
            words_count = len(text.split())
            efficiency = words_count / len(tokens) * 100 if tokens else 0
            tokens_per_word = len(tokens) / words_count if words_count else 0

            # Print efficiency and tokens per word for each file
            print(f"{tokenizer_name} - File: {os.path.basename(file_path)}, Efficiency: {efficiency:.2f}%, Tokens per Word: {tokens_per_word:.2f}")

def main(args):
    scand_test_string = "ÆØÅ æøå"
    nordic_test_string = "Åsa Ängel Örjan Ægir Øystein Ýmir Þor Ðan Måns Märtha Sölvi Kærlighed Brøn Lýður Aþena Sæði"
    eng_test_string = "This is a basic test of the tokenizer, to see if it is reversable in English."

    try:
        with jsonlines.open(args.input_file) as reader:
            for tokenizer_info in reader:
                tokenizer = AutoTokenizer.from_pretrained(tokenizer_info["url"], use_fast=True, legacy=("mT5Tokenizer" == tokenizer_info["name"]))

                scand_result = test_tokenizer_string(tokenizer, scand_test_string)
                nordic_result = test_tokenizer_string(tokenizer, nordic_test_string)
                eng_result = test_tokenizer_string(tokenizer, eng_test_string)

                print(f"{tokenizer_info['name']} - Scandinavian Test: {scand_result}, Nordic Test: {nordic_result}, English Test: {eng_result}")

                # Calculate and print efficiency for each file in the directory
                calculate_efficiency(tokenizer, args.directory, tokenizer_info["name"])

    except Exception as e:
        print(f"Error processing tokenizers: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tokenize test strings with various tokenizers, and compute efficiency for each file in a specified directory.")
    parser.add_argument('--input_file', type=str, default='tokenizer_list.jsonl', help='Path to the JSONL file containing tokenizer info. Default is "tokenizer_list.jsonl".')
    parser.add_argument('--directory', type=str, default='wikipedia_1k', help='Directory containing text files for calculating efficiency and tokens per word. Default is "wikipedia_1k".')

    args = parser.parse_args()
    main(args)

