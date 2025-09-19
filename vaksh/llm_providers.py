import os
import json
import re
from typing import List
from pydantic import BaseModel
from groq import Groq
from llama_cpp import Llama

class CommandList(BaseModel):
    cmds: List[str]

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("Please set GROQ_API_KEY in your environment.")

client = Groq(api_key=GROQ_API_KEY)
schema = CommandList.model_json_schema()

def groq_llm(prompt: str) -> List[str]:
    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant. Convert natural language to Linux commands. "
                    "Respond only in JSON with the schema: {\"cmds\": [\"...\"]}"
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        max_completion_tokens=512,
        top_p=1,
        stream=False,
        reasoning_effort="medium",
        response_format={
            "type": "json_schema",
            "json_schema": {"name": "command_list", "schema": schema},
        },
    )
    content = completion.choices[0].message.content
    data = json.loads(content)
    cmds = CommandList(**data).cmds
    return cmds

# --- Local Llama.cpp (phi-2) ---
MODEL_PATH = os.getenv(
    "LOCAL_MODEL_PATH",
    "/home/raj/Desktop/models/phi-2.Q4_K_M.gguf",
)

try:
    llm = Llama(model_path=MODEL_PATH, n_ctx=2048)
except Exception as e:
    print(f"Failed to load local model from {MODEL_PATH}: {e}")
    llm = None

def extract_json(content: str) -> str:
    """Extract the first JSON object from the model output."""
    match = re.search(r"\{.*\}", content, re.DOTALL)
    if match:
        return match.group(0)
    return ""

def local_llm(prompt: str) -> List[str]:
    if llm is None:
        return ["echo 'Local model not available. Please check LOCAL_MODEL_PATH.'"]

    system_prompt = (
        "You are a function that strictly outputs JSON.\n"
        "Schema: {\"cmds\": [\"first command\", \"second command\", ...]}.\n"
        "Rules:\n"
        "- Output only valid JSON (no markdown, no text outside JSON).\n"
        "- Each shell command must be a separate string in the list.\n"
        "- If the task requires multiple steps, list them in order.\n"
        "- If unclear, still output a valid list with a best-guess command like [\"echo 'invalid'\"]"
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]

    completion = llm.create_chat_completion(
        messages=messages,
        max_tokens=256,
        temperature=0.3,
        response_format={"type": "json_object", "schema": schema},
    )

    content = completion["choices"][0]["message"]["content"]
    content = extract_json(content)

    try:
        data = json.loads(content)
        cmds = CommandList(**data).cmds
        return [cmd.strip() for cmd in cmds]
    except Exception:
        return [f"echo 'Invalid local output: {content}'"]
