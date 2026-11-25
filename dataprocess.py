# IMPORT PACKAGES
import requests
import json
import numpy as np
import pandas as pd

# IMPORT DATA FROM API
URL = "https://api.jolpi.ca/ergast/f1/2024/results.json"
HEADERS = {"User-Agent": "DSCI510F1Dashboard/1.0"}

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
    resp = requests.get(URL, params={"limit": 5, "offset": 0},
                        headers=HEADERS, timeout=20)
    resp.raise_for_status()
    data = resp.json()

    print("=== raw JSON (first 1500 chars) ===")
    print(json.dumps(data, indent=2)[:1500])

    print("\n=== structure ===")
    show_structure(data)

    df = flatten(data)
    print("\n=== flattened table: columns ===")
    print(list(df.columns))

    pd.set_option("display.width", 200, "display.max_columns", None)
    print("\n=== flattened table ===")
    print(df[["season", "round", "raceName", "number", "position", "grid",
              "points", "laps", "status", "Driver.familyName",
              "Constructor.name"]])