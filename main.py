import numpy as np
import pandas as pd
import json, os
from dotenv import load_dotenv
from typing import Any

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

META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
IG_USER_ID = os.getenv("IG_USER_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

N = CONFIG["top_n"]

def score( post : dict[str, Any] ) -> float:
    likes = post.get("like_count", 0) or 0
    comms = post.get("comments_count", 0) or 0
    hours_old = max( post.get("hours_old", 1), 
                    CONFIG["min_hours_old"])

    return (likes + comms * CONFIG["comment_weight"]) / hours_old

def fetch( limit : int = 5000 ) -> list[dict[str, Any]]:
    pass # Insta API

def process( data : list[dict[str, Any]] ) -> Any:
    return {
        "count" : len(data),
    }

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

if __name__ == "__main__":
    main()