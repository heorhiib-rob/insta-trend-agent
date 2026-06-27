import numpy as np
import pandas as pd
import json, os
from dotenv import load_dotenv
from typing import Any
from google import genai
from pathlib import Path

# Fetch all resent content
# Sort by score
# Take N best
# Send to ChatGPT
# Generate output

load_dotenv()

def load_config( path : str = "config.json" ) -> dict[str, Any]:
    with open( path, "r", encoding="utf-8") as f:
        return json.load( f )

CONFIG = load_config()
PROMPT_DIR = Path("prompts")
META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
IG_USER_ID = os.getenv("IG_USER_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client_gemini = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
    )

N = CONFIG["top_n"]

def score( post : dict[str, Any] ) -> float:
    likes = post.get("like_count", 0) or 0
    comms = post.get("comments_count", 0) or 0
    hours_old = max( post.get("hours_old", 1), 
                    CONFIG["min_hours_old"])

    return (likes + comms * CONFIG["comment_weight"]) / hours_old

def fetch( limit : int = 5000 ) -> list[dict[str, Any]]:
    pass # Insta API

def load_prompt( name : str, **kwargs ) -> str:
    text = (PROMPT_DIR / name).read_text(encoding="utf-8")
    return text.format(**kwargs)

def process( data : list[dict[str, Any]] ) -> Any:
    prompt = load_prompt(
        "analyze_reels.txt",
        DATA = json.dump(data, ensure_ascii=False, indent=2))
    
    response = client_gemini.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response

def main():
    # load config 
    # fetch recent
    content = fetch()
    # sort and take N best
    content.sort( key = score, reverse=True )
    data = content[:N]

    # send to chatGPT
    ret = process( data )

    with open("ideas.json", "w", encoding="utf-8") as f:
        json.dump(ret, f, ensure_ascii=False, indent=2)

    #DONE

def test():
    response = client_gemini.models.generate_content(
        model="gemini-2.5-flash",
        contents="Привет!"
    )

    print(response)

if __name__ == "__main__":
    main()