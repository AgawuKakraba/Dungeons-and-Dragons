from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load AI model
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small")

# Set pad token (reuse EOS token)
tokenizer.pad_token = tokenizer.eos_token

chat_history = None

def generate_ai_response(user_input):
    global chat_history

    inputs = tokenizer(user_input + tokenizer.eos_token, return_tensors='pt', padding=True)
    input_ids = inputs["input_ids"]
    attention_mask = inputs["attention_mask"]

    if chat_history is not None:
        bot_input_ids = torch.cat([chat_history, input_ids], dim=-1)
        attention_mask = torch.cat([torch.ones(chat_history.shape, dtype=torch.long), attention_mask], dim=-1)
    else:
        bot_input_ids = input_ids

    chat_history = model.generate(
        bot_input_ids,
        attention_mask=attention_mask,
        max_length=1000,
        pad_token_id=tokenizer.eos_token_id
    )

    bot_response = tokenizer.decode(chat_history[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    return bot_response