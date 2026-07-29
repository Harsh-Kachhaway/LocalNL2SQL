from LangGraph.state import SQLState
import torch
from llm.llm_loder import tokenizer, terminators, model

def summarize_node(state: SQLState):
    question = state["question"]
    sql_result = state.get("final_result", "")
    error = state.get("error", "")
    
    system_prompt = (
        "You are a helpful data assistant. Provide a natural, conversational, "
        "and concise final answer based on the raw database result. "
        "Do not mention SQL, databases, or raw code."
    )
    
    if error:
        prompt_text = (
            f"The user asked: '{question}'.\n\n"
            f"However, the database returned this error during execution:\n{error}\n\n"
            f"Briefly explain to the user that something went wrong."
        )
    else:
        prompt_text = (
            f"User Question: {question}\n\n"
            f"Raw Database Result: {sql_result}\n\n"
            f"Summarize this data into a clear final answer."
        )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt_text}
    ]
    
    inputs = tokenizer.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_tensors="pt"
    ).to("cuda")
    
    print("Generating final summary...")
    
    with torch.no_grad():
        outputs = model.generate(
            input_ids=inputs,
            max_new_tokens=250, # Allowed a bit more length for a conversational answer
            use_cache=True,
            eos_token_id=terminators,
            pad_token_id=tokenizer.pad_token_id,
            do_sample=False # Greedy decoding is perfectly fine for the summary step
        )
        
    input_length = inputs.shape[1]
    generated_ids = outputs[0][input_length:]
    final_answer = tokenizer.decode(generated_ids, skip_special_tokens=True).strip()
    
    return {
        "final_answer": final_answer
    }