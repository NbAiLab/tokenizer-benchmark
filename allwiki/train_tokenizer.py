import argparse
import sentencepiece as spm

def train_bpe_tokenizer(input_file, vocab_size, model_prefix, byte_fallback=False):
    # Define the SentencePiece model parameters
    spm_params = f"--input={input_file} --model_prefix={model_prefix} " \
                 f"--vocab_size={vocab_size} --model_type=bpe"
    
    # If byte_fallback is enabled, add all byte values as user_defined_symbols
    if byte_fallback:
        byte_symbols = [f"<0x{i:02X}>" for i in range(256)]
        user_defined_symbols = ",".join(byte_symbols)
        spm_params += f" --user_defined_symbols={user_defined_symbols}"

    # Train the SentencePiece model
    spm.SentencePieceTrainer.Train(spm_params)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a BPE tokenizer with SentencePiece and save it, with an option for byte-level fallback.")
    parser.add_argument("--input_file", type=str, required=True, help="Path to the input text file for training.")
    parser.add_argument("--vocab_size", type=int, required=True, help="Vocabulary size for the BPE tokenizer.")
    parser.add_argument("--model_prefix", type=str, default="tokenizer", help="Prefix for the output model file names.")
    parser.add_argument("--byte_fallback", action='store_true', help="Include all byte values as user_defined_symbols for fallback.")

    args = parser.parse_args()

    # The model will be saved as 'tokenizer.model'
    train_bpe_tokenizer(args.input_file, args.vocab_size, args.model_prefix, args.byte_fallback)

