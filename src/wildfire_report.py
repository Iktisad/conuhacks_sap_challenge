import csv
from datetime import datetime, timedelta
from collections import defaultdict

# Parse and sort fires by severity and timestamp
fires = []
with open('current_wildfiredata.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        fires.append({
            'timestamp': datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S'),
            'severity': row['severity'].lower(),
        })

severity_order = {'high': 3, 'medium': 2, 'low': 1}
fires.sort(key=lambda x: (-severity_order[x['severity']], x['timestamp']))

# Define resources with cost-time efficiency priority
resources = [
    {'name': 'Smoke Jumpers', 'deployment_time': timedelta(minutes=30), 'cost': 5000, 'units': 5},
    {'name': 'Fire Engines', 'deployment_time': timedelta(hours=1), 'cost': 2000, 'units': 10},
    {'name': 'Ground Crews', 'deployment_time': timedelta(hours=1.5), 'cost': 3000, 'units': 8},
    {'name': 'Helicopters', 'deployment_time': timedelta(minutes=45), 'cost': 8000, 'units': 3},
    {'name': 'Tanker Planes', 'deployment_time': timedelta(hours=2), 'cost': 15000, 'units': 2},
]

# Sort resources by cost × deployment time (ascending)
resources_sorted = sorted(
    resources,
    key=lambda x: x['cost'] * x['deployment_time'].total_seconds() / 3600  # Convert to hours
)

# Track availability for each resource unit
resource_availability = {
    res['name']: [datetime.min] * res['units'] for res in resources
}

addressed = defaultdict(int)
missed = defaultdict(int)
total_operational = 0
total_damage = 0
damage_costs = {'low': 50000, 'medium': 100000, 'high': 200000}

for i, fire in enumerate(fires):
    fire_time = fire['timestamp']
    severity = fire['severity']
    next_fire_time = fires[i+1]['timestamp'] if i+1 < len(fires) else None
    assigned = False

    # Try resources sorted by cost-time efficiency
    for res in resources_sorted:
        name = res['name']
        deploy_time = res['deployment_time']
        cost = res['cost']

        # Find the earliest available unit
        available_units = resource_availability[name]
        for idx in range(len(available_units)):
            if available_units[idx] <= fire_time:
                # Check if this unit can handle the next fire
                new_available_time = fire_time + deploy_time
                if next_fire_time and new_available_time > next_fire_time:
                    continue  # Skip if it blocks the next fire

                # Assign the unit
                resource_availability[name][idx] = new_available_time
                total_operational += cost
                addressed[severity] += 1
                assigned = True
                break
        if assigned:
            break

    if not assigned:
        # Fallback: Use any available unit (even if it blocks future fires)
        for res in resources_sorted:
            name = res['name']
            available_units = resource_availability[name]
            for idx in range(len(available_units)):
                if available_units[idx] <= fire_time:
                    resource_availability[name][idx] = fire_time + res['deployment_time']
                    total_operational += res['cost']
                    addressed[severity] += 1
                    assigned = True
                    break
            if assigned:
                break

    if not assigned:
        total_damage += damage_costs[severity]
        missed[severity] += 1

# Generate report
severity_counts = defaultdict(int)
for fire in fires:
    severity_counts[fire['severity']] += 1

print(f"Number of fires addressed: {sum(addressed.values())}")
print(f"Number of fires delayed: {sum(missed.values())}")
print(f"Total operational costs: {total_operational}")
print(f"Estimated damage costs from delayed responses: {total_damage}")
print(f"Fire severity report: {dict(severity_counts)}")