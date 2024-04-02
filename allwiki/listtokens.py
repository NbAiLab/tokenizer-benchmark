import sentencepiece as spm
import argparse

def list_first_tokens(model_path, num_tokens=10):
    sp = spm.SentencePieceProcessor()
    sp.load(model_path)
    
    for i in range(num_tokens):
        token = sp.id_to_piece(i)
        print(f"ID {i}: Token '{token}'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List the first N tokens from a SentencePiece model file.")
    parser.add_argument("--model_path", type=str, required=True, help="Path to the SentencePiece .model file.")
    parser.add_argument("--num_tokens", type=int, default=10, help="Number of tokens to list, default is 10.")
    
    args = parser.parse_args()
    
    list_first_tokens(args.model_path, args.num_tokens)

