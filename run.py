import pandas as pd
import mlx.core as mx
from tqdm import tqdm
from mlx_lm import load, generate
from transformers import pipeline
from huggingface_hub import login, snapshot_download
import os
from pathlib import Path
from dotenv import load_dotenv


messages = [
        {
            "role": "system", 
            "content": """You are an expert Senior Software Engineer and Security Auditor.
            Your task is to evaluate code snippets against specific Non-Functional Requirements (NFRs).
            STRICT OUTPUT RULE:
            1. You must begin your response with exactly one word: \"Yes\" or \"No\".
            2. Follow that word with a single newline.
            3. Provide a concise explanation for your verdict.
            Do not provide any introductory text or conversational filler."""
        },
        # Example 1 (Few-shot)
        {"role": "user", "content": "NFR: Security\nCode: query = 'SELECT * FROM u WHERE id=' + id"},
        {"role": "assistant", "content": "No\nThis code is vulnerable to SQL injection via string concatenation."},
        
        # Example 2 (Few-shot)
        {"role": "user", "content": "NFR: Readability\nCode: x = [i for i in range(10) if i % 2 == 0]"},
        {"role": "assistant", "content": "Yes\nThe list comprehension is idiomatic and easy to read for Python developers."},
        
    ]

def make_message(tag, code):
    """Creates a message to prompt the llm with.

    Parameters
    ----------
    tag : String
        The type of NFR that the bug was fixed for.

    code : String
        The code of the bug either fixed or not.
    
    Returns
    -------
    message : Dict
        The built user message to prompt the LLM with
    """  
        
    # Strip leading/trailing whitespace from code to prevent "double newlines"
    clean_code = code.strip()
    # Use a clearer separator that the model recognizes from its training
    content = f"NFR Category: {tag}\n\nCode Input:\n```python\n{clean_code}\n```"
    return {"role": "user", "content": content}

def make_entry(index, fixed, text):
    """Creates a row of data for the pd dataframe.

    Parameters
    ----------
    index : String
        The index of the row will be the same as the index for it's code
        chunk in the original data.csv.

    fixed : Bool
        A tag showing weather or not the code contains a fix or if the NFR 
        is not being followed.

    text : list
        A list of both the llm's decision on weather or not the code follows the NFR 
        and also it's reasoning behind it's decision.
    
    Returns
    -------
    pddataframe
        A dataframe object with the row of data containing wether the LLM was correct 
        and it's reasoning
    """  

    category = ""

    if fixed: 
        if text[0] == "Yes":
            category = "TP"
        elif text[0] == "No":
            category = "FN"
        else: 
            category = "N/A"
    else: 
        if text[0] == "Yes":
            category = "FP"
        elif text[0] == "No":
            category = "TN"
        else: 
            category = "N/A"

    return pd.DataFrame(data={
        'category': category,
        'reasoning': text[1],
    }, index=pd.Index(data=[index], name='ID'))


def main():
    """Reads the issue data from a CSV and prompts an LLM to decide on weather or not 
    the code follows the specificed NFR as well as give reasoning for it's decision
    """
    os.environ["HF_XET_HIGH_PERFORMANCE"] = "1"

    models = [
        "./models/deepseek-coder-1.3b-instruct-mlx",
        "./models/deepseek-coder-6.7b-instruct-hf-4bit-mlx",
        "mlx-community/Llama-3.2-1B-Instruct-bf16",
        "mlx-community/Llama-3.2-3B-Instruct-bf16",
        "mlx-community/Qwen3.5-0.8B-MLX-4bit",
        "mlx-community/Qwen3.5-4B-MLX-4bit",
        "mlx-community/Qwen3.5-9B-MLX-4bit",
    ]
    load_dotenv()
    login(os.getenv('HF_TOKEN'))

    for model_name in models:
        model, tokenizer = load(model_name)

        i = 0
        df = pd.read_csv("./data.csv", index_col=0)
        data = []
        for index, row in tqdm(df.iterrows(), total=len(df)):
            code  = row["usages"]
            tag = row["tag"]
            message = make_message(tag, code)
            cur_message = messages + [message]

            prompt = tokenizer.apply_chat_template(
                cur_message, add_generation_prompt=True,
                enable_thinking=False, tokenize=False,
            )

            response = generate(
                model, 
                tokenizer,
                prompt=prompt)

            values = []
            if "deepseek" in model_name: 
                if response[0] == "Y":
                    values.append("Yes")
                    values.append(response[3:])
                else:
                    values.append("No")
                    values.append(response[2:])

            else: 
                values = response.split("\n")
            data.append(make_entry(index, row["fixed"], values))
            

        data = pd.concat(data)
        data.to_csv(f'./results/{model_name.split("/")[1]}.csv')


if __name__ == '__main__':
    main()