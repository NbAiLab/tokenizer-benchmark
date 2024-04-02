import sentencepiece as spm
import argparse

def compare_tokenizers(model_path1, model_path2):
    sp1 = spm.SentencePieceProcessor(model_file=model_path1)
    sp2 = spm.SentencePieceProcessor(model_file=model_path2)
    
    # Compare vocabulary size
    vocab_size1 = sp1.get_piece_size()
    vocab_size2 = sp2.get_piece_size()
    print(f"Vocabulary size comparison: {vocab_size1} vs {vocab_size2}")
    
    # Compare control characters
    control_chars1 = {sp1.id_to_piece(i) for i in range(vocab_size1) if sp1.is_control(i)}
    control_chars2 = {sp2.id_to_piece(i) for i in range(vocab_size2) if sp2.is_control(i)}
    print(f"Control characters are {'the same' if control_chars1 == control_chars2 else 'different'}.")

    # Attempt to identify and compare byte fallback tokens
    byte_fallback_pattern = r"<0x[0-9A-Fa-f]{2}>"
    byte_tokens1 = {sp1.id_to_piece(i) for i in range(vocab_size1) if sp1.id_to_piece(i).startswith('<0x')}
    byte_tokens2 = {sp2.id_to_piece(i) for i in range(vocab_size2) if sp2.id_to_piece(i).startswith('<0x')}
    print(f"Byte fallback tokens are {'the same' if byte_tokens1 == byte_tokens2 else 'different'}.")

    # Direct comparison of model type (BPE vs Unigram) is not provided by the API

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare two SentencePiece tokenizer model files.")
    parser.add_argument("model_path1", type=str, help="Path to the first SentencePiece .model file.")
    parser.add_argument("model_path2", type=str, help="Path to the second SentencePiece .model file.")
    
    args = parser.parse_args()
    
    compare_tokenizers(args.model_path1, args.model_path2)

