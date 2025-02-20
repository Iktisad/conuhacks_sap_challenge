# Wildfire Response and Prediction Challenge

## Introduction
Your role is to develop a comprehensive software solution for optimizing the deployment of firefighting resources and predicting future wildfire occurrences in the province of Quebec during wildfire season. The fire department operates 24/7 from June 1st to September 30th. Your solution should address both immediate response optimization and future risk prediction.

Provided Files:
-	historical_environmental_data.csv: Environmental data for the years 2020-2023.
-	historical_wildfiredata.csv: Wildfire occurrence data for the years 2020-2023.
-	current_wildfiredata.csv: Wildfire occurrence data for the year 2024.
-	future_environmental_data.csv: Future environmental data for the year 2025.

### Part 1: Resource Deployment Optimization
Problem Statement:
Your task is to develop a software solution to optimize the deployment of firefighting resources for the current wildfire season (2024). The optimized solution will minimize operating cost + damage cost. The resources available include different types of firefighting units, each with specific capabilities, deployment times, operational costs, and total availability:
-	Smoke Jumpers: 30 minutes deployment time, $5,000 per operation, 5 units available.
-	Fire Engines: 1-hour deployment time, $2,000 per operation, 10 units available.
-	Helicopters: 45 minutes deployment time, $8,000 per operation, 3 units available.
-	Tanker Planes: 2 hours deployment time, $15,000 per operation, 2 units available.
-	Ground Crews: 1.5 hours deployment time, $3,000 per operation, 8 units available.
-our solution must process information from the provided CSV file (current_wildfiredata.csv), where each row represents a wildfire report with the following details:
-	timestamp: The time the report was made.
-	fire_start_time: The estimated start time of the fire.
-	location: GPS coordinates of the fire location.
-	severity: The fire severity level (low, medium, high).

or overlapping deployment requests, prioritize based on fire severity (high severity takes precedence). Label any fires that cannot be addressed immediately due to lack of

ailable resources as "missed response".

our solution should track

-	The actual cost of deployed resources.
-	The potential environmental and property damage costs from missed responses.
Damage Costs for Missed Responses:
-	Low severity: $50,000
-	Medium severity: $100,000
-	High severity: $200,000
Generate a report that details:
-	The number of fires addressed and missed for each severity level.
-	The total operational costs.
-	The estimated damage costs from missed responses.

Evaluation Criteria

-	Correct Implementation: The solution correctly processes wildfire data from the CSV file.
-	Resource Deployment: Properly deploys firefighting resources based on severity and availability rules.
-	Cost Calculation: Accurately calculates operational costs and damage costs for missed responses.
-	Code Quality


### Expected Output

```txt
  Number of fires addressed: X
  Number of fires delayed: X
  Total operational costs: X
  Estimated damage costs from delayed responses: X
  Fire severity report: {'low': X, 'medium': X, 'high': X}
```

### OPTIONAL Part 2: Predictive Modeling for Future Fire Occurrences
Problem Statement:
Your task is to develop a predictive model for future fire occurrences using historical data. You will be provided with the following files:
•	historical_environmental_data.csv: Historical environmental data for the years 2020-2023.
•	historical_wildfiredata.csv: Historical wildfire occurrence data for the years 2020-2023.
•	future_environmental_data.csv: Future environmental data for the year 2025.
Your predictive model should:
1.	Analyze historical patterns of wildfire occurrences in relation to various environmental factors such as weather conditions, seasonality, vegetation indices, and human activity indicators.
2.	Predict future fire occurrences using the future environmental data.
3.	Visualize these predictions on a map of Quebec. Also, output a list of gps coordinates where fire is predicted. 

Feel free to use any mathematical/ML library to accomplish this (sklearn, facebook prophet, etc.)


Evaluation Criteria
•	Prediction Accuracy: The model accurately predicts fire occurrences compared to expected trends based on historical data.
•	Map Visualization: Clear and accurate visualization of predicted fire risks on a map of Quebec
•	GPS Coordinates List: Correctly outputs a list of GPS coordinates where fires are predicted

 

Evaluation Criteria – Detailed
Part 1: Resource Deployment Optimization
1.	Resource Deployment (10 points)
a.	Properly deploys firefighting resources based on fire severity and availability rules. 
b.	Prioritizes overlapping deployment requests based on fire severity (high, medium, low). 
c.	Addresses as many fires as possible with the available resources.
2.	Cost Calculation (10 points)
a.	Accurate calculation of operational costs for the deployment of resources. 
b.	Accurate calculation of potential environmental and property damage costs from missed responses.
3.	Code Quality (25 points)
a.	Code is well-organized, readable, and maintainable. 
b.	Follows best practices for software development, including appropriate error handling. 
c.	Proper documentation and comments explaining the implementation.

Part 2: Predictive Modeling for Future Fire Occurrences (Optional)
1.	Map Visualization (5 points)
a.	Clear, accurate visualization on a map of Quebec.
2.	GPS Coordinates List (5 points)
a.	Correct, comprehensive list of predicted fire locations.
b.	Ensures the list is comprehensive and matches the visual representation on the map.
3.	Model Implementation and Code Quality (10 points)
a.	Implementation with suitable libraries, well-documented and organized code.

