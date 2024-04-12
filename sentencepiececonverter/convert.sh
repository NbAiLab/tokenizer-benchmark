# Script made by Javier de la Rosa

# For models trained with SentencePiece with byte_fallback for autoregressive models
# ./spm_train --vocab_size 32000 --character_coverage 1.0 --hard_vocab_limit  --model_type bpe --pad_id 3 --shuffle_input_sentence true --model_prefix ./sentencepiece.model --byte_fallback=true --input text.txt  --input_sentence_size=100000 --num_threads 8
wget -O sentencepiece_extractor.py https://raw.githubusercontent.com/huggingface/tokenizers/master/bindings/python/scripts/sentencepiece_extractor.py
python sentencepiece_extractor.py --provider sentencepiece --model sentencepiece.model --merges-output-path ./merges.txt --vocab-output-path ./vocab.json

python <<EOF
from transformers import AutoTokenizer
from tokenizers import SentencePieceBPETokenizer
SentencePieceBPETokenizer.from_file("./vocab.json", "./merges.txt")
tokenizer = SentencePieceBPETokenizer.from_file("./vocab.json", "./merges.txt")
tokenizer.model.byte_fallback=True
tokenizer.model.fuse_unk=True
tokenizer.save("./tokenizer.json")
htok = AutoTokenizer.from_pretrained("./")
htok.padding_side = "right"
htok.save_pretrained("./")
EOF

