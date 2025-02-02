import pandas as pd
from datetime import datetime, timedelta
from pulp import LpMinimize, LpProblem, LpVariable, lpSum

# Firefighting resource definitions
resources = {
    "Smoke Jumpers": {"deployment_time": 30, "cost": 5000, "available": 5},
    "Fire Engines": {"deployment_time": 60, "cost": 2000, "available": 10},
    "Helicopters": {"deployment_time": 45, "cost": 8000, "available": 3},
    "Tanker Planes": {"deployment_time": 120, "cost": 15000, "available": 2},
    "Ground Crews": {"deployment_time": 90, "cost": 3000, "available": 8}
}

damage_costs = {"low": 50000, "medium": 100000, "high": 200000}

def parse_time(time_str):
    return datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")

def allocate_resources_ilp(fire_reports):
    total_cost = 0
    missed_fires = {"low": 0, "medium": 0, "high": 0}
    addressed_fires_set = set()  # Track unique fires addressed
    allocation = {}
    
    # Define ILP problem
    for date in fire_reports["fire_reported_date"].unique():
        daily_reports = fire_reports[fire_reports["fire_reported_date"] == date]
        daily_fire_ids = daily_reports.index.tolist()
        
        model = LpProblem("Fire_Resource_Allocation", LpMinimize)
        x = {(r, f): LpVariable(f"x_{r}_{f}", cat="Binary") for r in resources for f in daily_fire_ids}
        
        model += lpSum(x[r, f] * resources[r]["cost"] for r in resources for f in daily_fire_ids) + \
                 lpSum((1 - lpSum(x[r, f] for r in resources)) * damage_costs[daily_reports.loc[f, "severity"]] for f in daily_fire_ids)
        
        for r in resources:
            model += lpSum(x[r, f] for f in daily_fire_ids) <= resources[r]["available"]
        
        for f in daily_fire_ids:
            if daily_reports.loc[f, "severity"] == "high":
                model += lpSum(x[r, f] for r in resources) <= 3
            else:
                model += lpSum(x[r, f] for r in resources) <= 1
        
        # Constraint to prevent overlapping deployment
        for r in resources:
            for i, f1 in enumerate(daily_fire_ids):
                for f2 in daily_fire_ids[i+1:]:
                    if (daily_reports.loc[f1, "fire_start_time"] < 
                        daily_reports.loc[f2, "fire_start_time"] + timedelta(minutes=resources[r]["deployment_time"])) and \
                       (daily_reports.loc[f2, "fire_start_time"] < 
                        daily_reports.loc[f1, "fire_start_time"] + timedelta(minutes=resources[r]["deployment_time"])):
                        model += x[r, f1] + x[r, f2] <= 1
        
        model.solve()
        
        allocation[date] = {f: [] for f in daily_fire_ids}
        for r in resources:
            for f in daily_fire_ids:
                if x[r, f].value() == 1:
                    allocation[date][f].append(r)
                    addressed_fires_set.add(f)  # Add only unique fire IDs
                    total_cost += resources[r]["cost"]
        
        for f in daily_fire_ids:
            if not allocation[date][f]:
                severity = daily_reports.loc[f, "severity"]
                missed_fires[severity] += 1
                print(f"Missed Fire: {f} | Severity: {severity}")  # Debugging Output
    
    return len(addressed_fires_set), missed_fires, total_cost, allocation

def process_wildfire_data(file_path):
    df = pd.read_csv(file_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["fire_start_time"] = pd.to_datetime(df["fire_start_time"])
    df["fire_reported_date"] = df["timestamp"].dt.date
    
    severity_order = {"high": 3, "medium": 2, "low": 1}
    df["severity_rank"] = df["severity"].map(severity_order)
    df = df.sort_values(by=["fire_reported_date", "severity_rank", "fire_start_time"], ascending=[True, False, True]).reset_index()
    df.drop(columns=["severity_rank"], inplace=True)
    
    addressed_fires, missed_fires, total_cost, allocation = allocate_resources_ilp(df)
    missed_damage_cost = sum(missed_fires[severity] * damage_costs[severity] for severity in missed_fires)
    
    report = {
        "Number of fires addressed": addressed_fires,
        "Number of fires delayed": sum(missed_fires.values()),
        "Total operational costs": total_cost,
        "Estimated damage costs from delayed responses": missed_damage_cost,
        "Fire severity report": missed_fires,
        "Resource allocation": allocation
    }
    
    return report

# Example usage
file_path = "current_wildfiredata.csv"
report = process_wildfire_data(file_path)
for key, value in report.items():
    print(f"{key}: {value}")
