try:
    from transformers import AutoModelForCausalLM, AutoTokenizer
    import torch
    import random

    # Load the lightweight D&D-friendly model
    tokenizer = AutoTokenizer.from_pretrained("ybelkada/gpt-neo-125m-detox")
    model = AutoModelForCausalLM.from_pretrained("ybelkada/gpt-neo-125m-detox")

    if tokenizer.pad_token is None:
        tokenizer.add_special_tokens({'pad_token': '[PAD]'})
        model.resize_token_embeddings(len(tokenizer))

    USE_AI = True

except Exception as e:
    print("⚠️ AI model could not be loaded:", e)
    USE_AI = False

# A small buffer to remember the last N words for context
CONTEXT_MEMORY = 30  # number of words to remember
conversation_history = ""


def generate_ai_response(user_input, players=None):
    global conversation_history

    if USE_AI:
        # Append new user input to conversation history
        conversation_history += " Player: " + user_input
        # Keep only the last CONTEXT_MEMORY words
        memory_words = conversation_history.split()[-CONTEXT_MEMORY:]
        memory_context = " ".join(memory_words)

        # Construct DM prompt
        prompt = (
            "You are the Dungeon Master in a fantasy roleplaying game. "
            "Describe events vividly, suspensefully, and without repeating the player's words. "
            "Keep responses concise and turn-based.\n\n"
            f"{memory_context}\nDM:"
        )

        # Tokenize input
        inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)
        input_ids = inputs["input_ids"]
        attention_mask = inputs["attention_mask"]

        # Generate response
        output_ids = model.generate(
            input_ids,
            attention_mask=attention_mask,
            max_length=120,
            pad_token_id=tokenizer.pad_token_id,
            do_sample=True,
            top_k=40,
            top_p=0.90,
            temperature=0.8,
            repetition_penalty=1.4,
            no_repeat_ngram_size=3,
            eos_token_id=tokenizer.encode("\n")[0]
        )

        response = tokenizer.decode(output_ids[0], skip_special_tokens=True)

        # Extract only the DM's new text
        if "DM:" in response:
            response = response.split("DM:")[-1].strip()

        # Append DM's response to conversation history
        conversation_history += " DM: " + response

        return response

    else:
        # Fallback if AI didn't load
        if players:
            backup_dm = random.choice(players)
            return f"⚠️ AI Dungeon Master failed to load. {backup_dm} has been chosen as the Dungeon Master!"
        else:
            return "⚠️ AI Dungeon Master failed to load. Please assign a human Dungeon Master."