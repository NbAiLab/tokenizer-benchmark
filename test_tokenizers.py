import argparse
import jsonlines
import warnings
from transformers import AutoTokenizer

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

def main(args):
    scand_test_string = "Åsa Ängel Örjan Ægir Øystein Måns Märtha Sölvi Kærlighed Brøn"
    nordic_test_string = "Åsa Ängel Örjan Ægir Øystein Ýmir Þor Ðan Måns Märtha Sölvi Kærlighed Brøn Lýður Aþena Sæði"
    eng_test_string = "This is a basic test of the tokenizer, to see if it is reversable in English."

    try:
        with jsonlines.open(args.input_file) as reader:
            for tokenizer_info in reader:
                tokenizer = AutoTokenizer.from_pretrained(tokenizer_info["url"], use_fast=True, legacy=("mT5Tokenizer" == tokenizer_info["name"]))
                
                nordic_result = test_tokenizer_string(tokenizer, nordic_test_string)
                scand_result = test_tokenizer_string(tokenizer, scand_test_string)
                eng_result = test_tokenizer_string(tokenizer, eng_test_string)

                # Efficiency is calculated for the Nordic Test String
                nordic_tokens = tokenizer.tokenize(nordic_test_string)
                efficiency = len(nordic_test_string.split()) / len(nordic_tokens) * 100
                tokens_per_word = len(nordic_tokens) / len(nordic_test_string.split())
                vocab_size = tokenizer.vocab_size

                output = f"{tokenizer_info['name']}: Efficiency: {efficiency:.2f}%, Tokens per Word: {tokens_per_word:.2f}, Vocabulary Size: {vocab_size}, Scandinavian Test: {scand_result}, Nordic Test: {nordic_result}, English Test: {eng_result}"

                print(output)

    except Exception as e:
        print(f"Error loading tokenizers: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tokenize Nordic and English test strings with various tokenizers, compute efficiency based on the Nordic Test String, and evaluate the exact match after decoding. Reports match result.")
    parser.add_argument('--input_file', type=str, default='tokenizer_list.jsonl', help='Path to the JSONL file containing tokenizer info. Default is "tokenizer_list.jsonl".')
    
    args = parser.parse_args()
    main(args)

