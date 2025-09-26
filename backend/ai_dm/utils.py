from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Use a lighter model
tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
model = AutoModelForCausalLM.from_pretrained("distilgpt2")

# Add padding token if missing
if tokenizer.pad_token is None:
    tokenizer.add_special_tokens({'pad_token': '[PAD]'})
    model.resize_token_embeddings(len(tokenizer))

def generate_ai_response(user_input):
    inputs = tokenizer(user_input, return_tensors="pt", padding=True, truncation=True)
    input_ids = inputs["input_ids"]
    attention_mask = inputs["attention_mask"]

    output_ids = model.generate(
        input_ids,
        attention_mask=attention_mask,
        max_length=150,
        pad_token_id=tokenizer.pad_token_id
    )

    response = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return response