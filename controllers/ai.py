from openai import OpenAI
import re  
import json

client = OpenAI(base_url="http://localhost:11434/v1", api_key="eiei")

def run_agent(prompt: str):
    system_prompt = """
    You are an AI calendar assistant. Your goal is to map user requests to these actions:
    1. get_events -> returns list of events
    2. create_event -> requires (summary, start, end)
    3. delete_event -> requires (event_id)
    4. update_event -> requires (event_id, summary, start, end)
    5. get_free_time -> requires (time_min, time_max)

    Return ONLY JSON: {"action": "function_name", "args": {...}}
    Example: {"action": "create_event", "args": {"summary": "Lunch", "start": "2026-03-09T12:00:00+07:00", "end": "2026-03-09T13:00:00+07:00"}}
    """

    response = client.chat.completions.create(
        model="llama3.2",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )
    
    raw_content = response.choices[0].message.content.strip()
    print("--- RAW AI RESPONSE ---")
    print(raw_content)
    print("-----------------------")
    json_match = re.search(r'\{.*\}', raw_content, re.DOTALL)
    
    if json_match:
        try:
            return json.loads(json_match.group(0))
        except json.JSONDecodeError:
            return {"action": "error", "args": {"message": "Invalid JSON format"}}
    
    return {"action": "error", "args": {"message": "No JSON found in response"}}