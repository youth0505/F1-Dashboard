# IMPORT PACKAGES
import requests
import json
import time
import numpy as np
import pandas as pd

# IMPORT DATA FROM API
def get_data(season):
    URL = f"https://api.jolpi.ca/ergast/f1/{season}/results.json"
    HEADERS = {"User-Agent": "DSCI510F1Dashboard/1.0"}
    return URL, HEADERS

def show_structure(obj, indent=0, max_list=1):
    pad = "  " * indent
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, (dict, list)):
                label = f"list[{len(v)}]" if isinstance(v, list) else "dict"
                print(f"{pad}{k}: {label}")
                show_structure(v, indent + 1, max_list)
            else:
                print(f"{pad}{k}: {type(v).__name__} = {v!r}")
    elif isinstance(obj, list):
        for item in obj[:max_list]:
            print(f"{pad}[0]")
            show_structure(item, indent + 1, max_list)


def flatten(data):
    races = data["MRData"]["RaceTable"]["Races"]
    df = pd.json_normalize(
        races,
        record_path="Results",
        meta=["season", "round", "raceName", "date", ["Circuit", "circuitName"]],
    )
    return df


if __name__ == "__main__":
    frames = []
    for season in [2022, 2023, 2024, 2025, 2026]:
        URL, HEADERS = get_data(season)
        offset = 0
        while True:
            while True:
                resp = requests.get(URL, params={"limit": 100, "offset": offset},
                                    headers=HEADERS, timeout=20)
                if resp.status_code == 429:
                    wait = int(resp.headers.get("Retry-After", 30))
                    print("rate limited, waiting", wait, "s")
                    time.sleep(wait)
                    continue
                resp.raise_for_status()
                break
            data = resp.json()
            frames.append(flatten(data))
            offset += 100
            if offset >= int(data["MRData"]["total"]):
                break
            time.sleep(0.5)
        print(season, "done")

    all_data = pd.concat(frames, ignore_index=True)
    all_data.to_csv("f1_results_2022_2026.csv", index=False, encoding="utf-8-sig")
    print(all_data.groupby("season").size())