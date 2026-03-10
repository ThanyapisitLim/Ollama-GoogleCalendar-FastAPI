from openai import OpenAI
import re  
import json

client = OpenAI(base_url="http://localhost:11434/v1", api_key="eiei")

def run_agent(prompt: str):
    system_prompt = """
    You are an AI calendar assistant. 
    
    1. If the user wants to manage their calendar (create, delete, list, etc.), return ONLY JSON:
       {"action": "create_event" | "delete_event" | "get_events" | "update_event" | "get_free_time", "args": {...}}
       Note: For event descriptions, use 'summary' or 'title'.
    
    2. If the user is just chatting, asking a general question, or you need to clarify something, return ONLY JSON with a 'talk' action:
       {"action": "talk", "args": {"message": "Your friendly response here"}}

    Rules:
    - ALWAYS return valid JSON.
    - Use ISO 8601 for dates.
    """

    response = client.chat.completions.create(
        model="llama3.2",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"}
    )
    
    raw_content = response.choices[0].message.content.strip()
    try:
        return json.loads(raw_content)
    except json.JSONDecodeError:
        # Fallback if the model somehow breaks JSON mode
        return {"action": "talk", "args": {"message": raw_content}}