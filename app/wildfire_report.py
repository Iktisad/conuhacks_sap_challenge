import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from collections import defaultdict
import os

def process_wildfire_data(file_path):
    """Processes wildfire data from CSV and allocates resources efficiently."""
    if not os.path.exists(file_path):
        return {"error": "File not found"}

    # Load wildfire data
    df_fires = pd.read_csv(file_path, parse_dates=["timestamp"])

    # Map severity to numerical values for sorting
    severity_order = {"high": 3, "medium": 2, "low": 1}
    df_fires["severity_value"] = df_fires["severity"].str.lower().map(severity_order)

    # Sort fires by severity (descending) and timestamp (ascending)
    df_fires.sort_values(by=["severity_value", "timestamp"], ascending=[False, True], inplace=True)

    # Define resources with structured NumPy array
    resources = np.array([
        ("Smoke Jumpers", timedelta(minutes=30), 5000, 5),
        ("Fire Engines", timedelta(hours=1), 2000, 10),
        ("Ground Crews", timedelta(hours=1.5), 3000, 8),
        ("Helicopters", timedelta(minutes=45), 8000, 3),
        ("Tanker Planes", timedelta(hours=2), 15000, 2),
    ], dtype=[("name", "U20"), ("deploy_time", "O"), ("cost", "i4"), ("units", "i4")])

    # Calculate efficiency: cost × deployment time in hours
    efficiency = np.array([r[2] * r[1].total_seconds() / 3600 for r in resources])

    # Sort resources by efficiency (ascending)
    resources = resources[np.argsort(efficiency)]

    # Track resource availability using pandas DataFrame
    availability_df = pd.DataFrame({
        "resource": np.repeat(resources["name"], resources["units"]),
        "available_time": datetime.min
    })

    # Track fire response
    addressed = defaultdict(int)
    missed = defaultdict(int)
    total_operational = 0
    total_damage = 0
    damage_costs = {"low": 50000, "medium": 100000, "high": 200000}

    # Assign resources to fires
    for i, fire in df_fires.iterrows():
        fire_time = fire["timestamp"]
        severity = fire["severity"]
        next_fire_time = df_fires["timestamp"].iloc[i + 1] if i + 1 < len(df_fires) else None
        assigned = False

        # Try resources sorted by cost-time efficiency
        for res in resources:
            res_name, deploy_time, cost, _ = res

            # Find earliest available unit
            available_units = availability_df[availability_df["resource"] == res_name]
            available_units = available_units[available_units["available_time"] <= fire_time]

            if not available_units.empty:
                # Assign the earliest available unit
                idx = available_units.index[0]
                new_available_time = fire_time + deploy_time

                # Ensure it doesn't block the next fire
                if next_fire_time and new_available_time > next_fire_time:
                    continue  # Skip this resource

                availability_df.at[idx, "available_time"] = new_available_time
                total_operational += cost
                addressed[severity] += 1
                assigned = True
                break

        if not assigned:
            # Fallback: Use any available unit
            for res in resources:
                res_name, deploy_time, cost, _ = res
                available_units = availability_df[availability_df["resource"] == res_name]
                available_units = available_units[available_units["available_time"] <= fire_time]

                if not available_units.empty:
                    idx = available_units.index[0]
                    availability_df.at[idx, "available_time"] = fire_time + deploy_time
                    total_operational += cost
                    addressed[severity] += 1
                    assigned = True
                    break

        if not assigned:
            total_damage += damage_costs[severity]
            missed[severity] += 1

    # Generate report
    severity_counts = df_fires["severity"].value_counts().to_dict()

    return {
        "fires_addressed": sum(addressed.values()),
        "fires_delayed": sum(missed.values()),
        "total_operational_costs": total_operational,
        "estimated_damage_costs": total_damage,
        "fire_severity_report": severity_counts
    }