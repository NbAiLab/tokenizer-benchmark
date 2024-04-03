import argparse
import sentencepiece as spm
import re

def is_valid_token(token):
    """Checks if a token is valid. 
    Invalid if it contains commas or is solely punctuation."""
    # Exclude tokens with commas or that are only punctuation (adjust as needed)
    if "," in token or '"' in token or "." in token:
        return False
    return True

def train_bpe_tokenizer(input_file, vocab_size, model_prefix, user_defined_tokens_file=None, byte_fallback=False):
    # Basic SentencePiece parameters
    spm_params = f"--input={input_file} --model_prefix={model_prefix} " \
                 f"--vocab_size={vocab_size} --model_type=bpe --byte_fallback"

    user_defined_symbols = []

    # If byte_fallback is enabled, add all byte values as part of user_defined_symbols
    if byte_fallback:
        byte_symbols = [f"<0x{i:02X}>" for i in range(256)]
        user_defined_symbols.extend(byte_symbols)

    # If a file with user-defined tokens is provided, filter and append its contents to user_defined_symbols
    if user_defined_tokens_file:
        with open(user_defined_tokens_file, 'r', encoding='utf-8') as f:
            tokens = [line.strip() for line in f.readlines() if line.strip() and is_valid_token(line.strip())]
        user_defined_symbols.extend(tokens[:50])
        print(f"Loaded {len(tokens)} user-defined tokens after filtering.")

    # Convert the list of user-defined symbols to a comma-separated string and add to the parameters
    if user_defined_symbols:
        spm_params += " --user_defined_symbols=" + ",".join(user_defined_symbols)

    # Train the SentencePiece model
    spm.SentencePieceTrainer.Train(spm_params)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a BPE tokenizer with SentencePiece, including options for adding user-defined tokens and enabling byte-level fallback.")
    parser.add_argument("--input_file", type=str, required=True, help="Path to the input text file for training.")
    parser.add_argument("--vocab_size", type=int, required=True, help="Vocabulary size for the BPE tokenizer.")
    parser.add_argument("--model_prefix", type=str, default="tokenizer", help="Prefix for the output model file names.")
    parser.add_argument("--user_defined_tokens_file", type=str, help="Path to a file containing user-defined tokens to include in the tokenizer.")
    parser.add_argument("--byte_fallback", action='store_true', help="Include all byte values as user_defined_symbols for fallback.")

    args = parser.parse_args()

    train_bpe_tokenizer(args.input_file, args.vocab_size, args.model_prefix, args.user_defined_tokens_file, args.byte_fallback)

