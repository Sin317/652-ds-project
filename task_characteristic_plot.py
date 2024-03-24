import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt

# Define column names (assuming you have knowledge of the dataset structure)
columns = ['starttime', 'endtime', 'job id', 'task id', 'machine id', 'status',
           'sequence number', 'total sequence number', 'max cpu', 'avg cpu',
           'max memory', 'avg memory']

# Read the CSV file with specified column names
data = pd.read_csv("data.txt", names=columns)

# Step 2: Convert time columns to datetime
data['starttime'] = pd.to_datetime(data['starttime'], unit='s')
data['endtime'] = pd.to_datetime(data['endtime'], unit='s')

# Step 3: Aggregate data by time intervals
# For example, aggregate data into 1-hour intervals
data.set_index('starttime', inplace=True)
hourly_data = data.resample('1H').agg({
    'endtime': 'max',
    'job id': 'count',  # Count the number of tasks per hour
    # Add more aggregation functions as needed
}).reset_index()

# Step 4: Handle missing values
hourly_data.fillna(0, inplace=True)  # Fill missing values with 0
print(hourly_data.head())
# Step 5: Feature engineering
# For clustering, we'll use 'max cpu', 'avg cpu', 'max memory', and 'avg memory' features
X = data[['max cpu', 'avg cpu', 'max memory', 'avg memory']]
# print(X.head())
# Step 6: Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
# print(X_scaled)
# Step 7: Perform clustering (unsupervised learning)
dbscan = DBSCAN(eps=0.5, min_samples=5)  # You may need to adjust eps and min_samples
clusters = dbscan.fit_predict(X_scaled)

# Step 8: Visualize the clusters
plt.scatter(X_scaled[:, 0], X_scaled[:, 1], c=clusters, cmap='viridis')
plt.xlabel('Max CPU')
plt.ylabel('Avg CPU')
plt.title('Clustering of Tasks based on CPU Usage (DBSCAN)')
plt.show()


