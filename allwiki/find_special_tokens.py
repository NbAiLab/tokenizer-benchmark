import argparse
import sentencepiece as spm
import re

def load_vocab_from_tokenizer(model_path):
    """Loads vocabulary from a SentencePiece tokenizer model."""
    sp = spm.SentencePieceProcessor()
    sp.Load(model_path)
    vocab = {sp.IdToPiece(id) for id in range(sp.GetPieceSize())}
    return vocab

def valid_token(token):
    """Checks if a token is valid based on a regex pattern."""
    # Adjust the pattern to match the tokens you consider valid.
    pattern = re.compile(r'^[\w\-\.,]+$')
    return bool(pattern.match(token))

def extract_unique_tokens(model_path_a, model_path_b, model_path_c):
    """Extracts tokens that are in both model A and B but not in C."""
    vocab_a = load_vocab_from_tokenizer(model_path_a)
    vocab_b = load_vocab_from_tokenizer(model_path_b)
    vocab_c = load_vocab_from_tokenizer(model_path_c)

    # Find tokens common to A and B but not in C
    unique_tokens = (vocab_a & vocab_b) - vocab_c
    # Filter tokens using the valid_token function
    #filtered_tokens = {token for token in unique_tokens if valid_token(token)}
    return unique_tokens

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Finds tokens that are common to both tokenizer A and B but not in tokenizer C.")
    parser.add_argument("--model_a", type=str, required=True, help="Path to the SentencePiece model file for tokenizer A.")
    parser.add_argument("--model_b", type=str, required=True, help="Path to the SentencePiece model file for tokenizer B.")
    parser.add_argument("--model_c", type=str, required=True, help="Path to the SentencePiece model file for tokenizer C.")

    args = parser.parse_args()

    unique_tokens = extract_unique_tokens(args.model_a, args.model_b, args.model_c)

    output_file = "unique_tokens.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        for token in sorted(unique_tokens):
            f.write(token + "\n")
    print(f"Unique tokens have been saved to {output_file}")
    print(f"\nTotal Unique Tokens Found: {len(unique_tokens)}")

