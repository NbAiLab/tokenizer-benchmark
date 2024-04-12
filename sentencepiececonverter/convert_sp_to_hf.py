import argparse
from tokenizers import SentencePieceBPETokenizer
from transformers import AutoTokenizer
import os
import subprocess
import wget

def download_extractor_script(output_dir):
    # Download the SentencePiece extractor script
    script_url = "https://raw.githubusercontent.com/huggingface/tokenizers/master/bindings/python/scripts/sentencepiece_extractor.py"
    script_path = os.path.join(output_dir, "sentencepiece_extractor.py")
    if not os.path.exists(script_path):
        wget.download(script_url, out=script_path)
    return script_path

def extract_spm_vocab_and_merges(model_file, output_dir, script_path):
    # Extract vocab and merges using the SentencePiece model
    subprocess.run([
        "python", script_path,
        "--provider", "sentencepiece",
        "--model", model_file,
        "--merges-output-path", os.path.join(output_dir, "merges.txt"),
        "--vocab-output-path", os.path.join(output_dir, "vocab.json")
    ], check=True)

def create_and_save_tokenizer(output_dir):
    # Create tokenizer from extracted files
    tokenizer = SentencePieceBPETokenizer.from_file(
        os.path.join(output_dir, "vocab.json"), os.path.join(output_dir, "merges.txt"))
    tokenizer.model.byte_fallback = True
    tokenizer.model.fuse_unk = True

    # Save the tokenizer locally
    tokenizer.save(os.path.join(output_dir, "tokenizer.json"))

    # Convert to HuggingFace tokenizer and save
    htok = AutoTokenizer.from_pretrained(output_dir)
    htok.padding_side = "right"
    htok.save_pretrained(output_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert SentencePiece model to HuggingFace Tokenizer.")
    parser.add_argument("--model_file", type=str, required=True, help="Path to the SentencePiece model file.")
    parser.add_argument("--output_dir", type=str, required=True, help="Directory to save the output files and tokenizer.")

    args = parser.parse_args()

    # Ensure output directory exists
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    script_path = download_extractor_script(args.output_dir)
    extract_spm_vocab_and_merges(args.model_file, args.output_dir, script_path)
    create_and_save_tokenizer(args.output_dir)

