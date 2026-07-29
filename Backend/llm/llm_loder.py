
from unsloth import FastLanguageModel
from dotenv import load_dotenv
import os
load_dotenv()

MODEL_PATH = os.getenv("MODEL_PATH")

max_seq_length = 8192
dtype = None
load_in_4bit = True

print("Loading Checkpoint...")
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = MODEL_PATH,
    max_seq_length = max_seq_length,
    dtype = dtype,
    load_in_4bit = load_in_4bit,
)

FastLanguageModel.for_inference(model)

terminators = [
    tokenizer.eos_token_id,
    tokenizer.convert_tokens_to_ids("<|im_end|>")
]

