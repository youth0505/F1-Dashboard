# Project Proposal

Course: DSCI - 510  

Team/Member(s): Zhu Lingfei  

USC ID: 8599420339  

## Team Members

Zhu Lingfei

I will be responsible for API data acquisition, data cleaning, analysis, dashboard development, and the final report.

## Project Topic Motivation and Intended Application

**Project topic:** Formula 1 Race Result Dashboard

**Motivation:** I plan to use Formula 1 race results to compare drivers and teams across a season. The data can show points, finishing positions, and how drivers perform compared with their starting positions.

**Intended application:** A simple dashboard will allow users to select a season, driver, or team and view charts and summary statistics.

## API and Data Sources

**Jolpica F1 API - public Formula 1 race data**

Documentation: https://github.com/jolpica/jolpica-f1/blob/main/docs/README.md

API base URL: https://api.jolpi.ca/ergast/f1/

Expected data: season, round, race name, date, circuit, driver name, constructor/team, grid position, finish position, points, laps, and race status.

The API documentation requires a custom User-Agent. I will check the current access rules and rate limits before implementation.

I will use Python requests to get JSON data from the API. The project will collect race-result data for at least three completed seasons, initially 2022 to 2025. Because one request returns at most 100 records, I will use the offset parameter in a loop until all available results are collected.

```python
import requests

url = "https://api.jolpi.ca/ergast/f1/2024/results.json"

params = {
    "limit": 100,
    "offset": 0
}

headers = {
    "User-Agent": "DSCI510F1Dashboard/1.0"
}

response = requests.get(
    url,
    params=params,
    headers=headers,
    timeout=20
)

response.raise_for_status()
data = response.json()
```

## Initial Project Questions

1. Which drivers have the highest total points and best average finishing positions in a selected season? Which constructors have the highest total points?
2. Which drivers gain or lose the most positions from the starting grid to the classified finish?
3. Among classified finishers, how strongly are grid position and finishing position related?

## Pandas and NumPy

Pandas will be used to clean the JSON data, create DataFrames, group results by driver or team, and calculate summary statistics. NumPy will be used to calculate average finish position, standard deviation, percentiles, and the correlation between grid position and finish position.
