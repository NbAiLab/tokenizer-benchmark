import sentencepiece as spm
import argparse

def train_tokenizer(input_file, model_prefix, vocab_size, control_tokens):
    """
    Train a SentencePiece BPE tokenizer with specific control tokens.
    
    Parameters:
    - input_file: Path to the text file used for training the tokenizer.
    - model_prefix: Prefix for the output model file.
    - vocab_size: Desired size of the vocabulary.
    - control_tokens: A list of control tokens to include in the tokenizer.
    """
    control_symbols = ",".join(control_tokens)
    spm.SentencePieceTrainer.Train(
        f"--input={input_file} "
        f"--model_prefix={model_prefix} "
        f"--vocab_size={vocab_size} "
        f"--model_type=bpe "
        f"--control_symbols={control_symbols}"
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a SentencePiece tokenizer with specific control tokens.")
    parser.add_argument("--input_file", type=str, required=True, help="Path to the text file for training the tokenizer.")
    parser.add_argument("--model_prefix", type=str, required=True, help="Prefix for the output model files.")
    parser.add_argument("--vocab_size", type=int, required=True, help="The desired vocabulary size.")

    args = parser.parse_args()

    # Specify your control tokens here
    control_tokens = ["[PAD]", "[CLS]", "[SEP]", "[UNK]"]
    
    train_tokenizer(args.input_file, args.model_prefix, args.vocab_size, control_tokens)
    
    print(f"Model trained successfully and saved as {args.model_prefix}.model")
