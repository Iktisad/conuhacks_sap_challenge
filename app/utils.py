import pandas as pd
from datetime import datetime, timedelta
from collections import deque

# Define firefighting resources
resources = {
    "Smoke Jumpers": {"priority": 1, "deployment_time": timedelta(minutes=30), "cost": 5000, "available": 5},
    "Fire Engines": {"priority": 2, "deployment_time": timedelta(hours=1), "cost": 2000, "available": 10},
    "Helicopters": {"priority": 3, "deployment_time": timedelta(minutes=45), "cost": 8000, "available": 3},
    "Tanker Planes": {"priority": 4, "deployment_time": timedelta(hours=2), "cost": 15000, "available": 2},
    "Ground Crews": {"priority": 5, "deployment_time": timedelta(hours=1, minutes=30), "cost": 3000, "available": 8},
}

# Damage cost per severity level for missed responses
damage_costs = {"low": 50000, "medium": 100000, "high": 200000}

def load_wildfire_data(file_path):
    try:
        df = pd.read_csv(file_path)
        df.to_csv("data/loaded_wildfiredata.csv", index=False)
    except Exception as e:
        print(f"Error loading file: {e}")

def process_wildfire_data(file_path):
    wildfire_data = pd.read_csv(file_path)
    wildfire_data["timestamp"] = pd.to_datetime(wildfire_data["timestamp"])
    wildfire_data["fire_start_time"] = pd.to_datetime(wildfire_data["fire_start_time"])

    severity_order = {"high": 1, "medium": 2, "low": 3}
    wildfire_data["severity_rank"] = wildfire_data["severity"].map(severity_order)
    wildfire_data = wildfire_data.sort_values(by=["severity_rank", "timestamp"])

    total_operational_cost = 0
    missed_responses = {"low": 0, "medium": 0, "high": 0}
    fires_addressed = {"low": 0, "medium": 0, "high": 0}
    active_deployments = {key: deque() for key in resources}

    wildfire_data["date"] = wildfire_data["timestamp"].dt.date
    unique_dates = wildfire_data["date"].unique()

    for fire_date in unique_dates:
        resource_tracker = {key: val["available"] for key, val in resources.items()}
        for resource, queue in active_deployments.items():
            while queue and queue[0] <= datetime.combine(fire_date, datetime.min.time()):
                queue.popleft()

        daily_fires = wildfire_data[wildfire_data["date"] == fire_date]
        for _, fire in daily_fires.iterrows():
            severity = fire["severity"]
            report_time = fire["timestamp"]
            response_time = report_time - fire["fire_start_time"]
            deployed = False

            for resource, details in sorted(resources.items(), key=lambda x: (x[1]["cost"], x[1]["priority"])):
                if resource_tracker[resource] > 0 and response_time <= details["deployment_time"]:
                    resource_tracker[resource] -= 1
                    total_operational_cost += details["cost"]
                    fires_addressed[severity] += 1
                    end_time = report_time + details["deployment_time"]
                    active_deployments[resource].append(end_time)
                    deployed = True
                    break

            if not deployed:
                missed_responses[severity] += 1

    total_damage_cost = sum(missed_responses[sev] * damage_costs[sev] for sev in damage_costs)

    return {
        "Number of fires addressed": sum(fires_addressed.values()),
        "Number of fires missed": sum(missed_responses.values()),
        "Total operational costs": total_operational_cost,
        "Estimated damage costs from missed responses": total_damage_cost,
        "Fire severity report": fires_addressed
    }