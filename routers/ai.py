from fastapi import APIRouter, Query
from controllers.ai import run_agent
from controllers.calendar import create_event, get_events, delete_event, update_event, get_free_time

router = APIRouter()

@router.post("/ai")
def ai(prompt: str = Query(...)):
    result = run_agent(prompt)
    print("AI returned:", result)

    if not isinstance(result, dict) or "action" not in result:
        return {"error": "AI failed to return a valid action", "raw": result}

    action = result.get("action")
    args = result.get("args", {})
    
    if action == "error":
        return result
    
    if action == "talk":
        return args.get("message", "I'm not sure how to respond to that.")

    try:
        if action == "create_event":
            summary = args.get("summary") or args.get("title")
            return create_event(summary, args["start"], args["end"])
        elif action == "get_free_time":
            return get_free_time(args["time_min"], args["time_max"])
        elif action == "get_events":
            return get_events()
        elif action == "delete_event":
            return delete_event(args["event_id"])
        elif action == "update_event":
            summary = args.get("summary") or args.get("title")
            return update_event(args["event_id"], summary, args["start"], args["end"])
        
        return {"error": f"Action '{action}' not implemented"}
    except Exception as e:
        return {"error": str(e), "ai_result": result}