from LangGraph.state import SQLState
import torch
from collections import Counter
from llm.llm_loder import tokenizer, terminators, model
from Prompt.prompts import system_instruction

def generate_sql_node(state: SQLState):
    schema = state["schema"]
    question = state["question"]
    previous_error = state.get("error", "")
    previous_sql = state.get("generated_sql", "")
    retry_count = state.get("retry_count", 0)
        
    if previous_error:
        prompt_text = (
            f"Given the SQL schema:\n{schema}\n\n"
            f"Question: {question}\n\n"
            f"Your previous query was:\n{previous_sql}\n\n"
            f"It produced this error:\n{previous_error}\n\n"
            f"Please correct the query to fix the error."
        )
    else:
        prompt_text = f"Given the following SQL schema:\n{schema}\n\nQuestion: {question}"

    messages = [
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": prompt_text}
    ]
    
    inputs = tokenizer.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_tensors="pt"
    ).to("cuda")
    
    generated_queries = []
    
    print(f"Generating 5 queries for verification (Attempt {retry_count + 1})...")
    
    for i in range(5):
        with torch.no_grad():
            outputs = model.generate(
                input_ids=inputs,
                max_new_tokens=150,
                use_cache=True,
                eos_token_id=terminators,
                pad_token_id=tokenizer.pad_token_id,
                # do_sample is required here! Without it, you get 5 identical queries.
                do_sample=True,
                temperature=0.6 
            )
            
        input_length = inputs.shape[1]
        generated_ids = outputs[0][input_length:]
        generated_sql = tokenizer.decode(generated_ids, skip_special_tokens=True).strip()
        
        # Clean up Markdown formatting if the LLM adds it
        if generated_sql.startswith("```sql"):
            generated_sql = generated_sql.replace("```sql", "").replace("```", "").strip()
        elif generated_sql.startswith("```"):
            generated_sql = generated_sql.replace("```", "").strip()
            
        generated_queries.append(generated_sql)
        print(f"Run {i+1}/5 completed.")
        
    # Find the most common query among the 5 runs
    best_query = Counter(generated_queries).most_common(1)[0][0]
    print(f"Verification complete. Selected query:\n{best_query}")
    
    return {
        "generated_sql": best_query,
        "retry_count": retry_count + 1 if previous_error else retry_count
    }