import tkinter as tk
from tkinter import filedialog
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# Function to simulate load balancing for identified potential straggler tasks
def simulate_load_balancing(resources, straggler_indices):
    # Distribute the identified potential straggler tasks among resources
    cpu_utilizations = {
        "Resource1": 0.9,
        "Resource2": 0.1,
        "Resource3": 0.1
    }
    def calculate_load(resource):
        return resources[resource] * cpu_utilizations[resource]

    for straggler_index in straggler_indices:
        # Identify the resource with the lowest workload
        target_resource = min(resources, key=calculate_load)
        # print(straggler_index, target_resource)
        resources[target_resource] += 1  # Assign the straggler task to the resource with the lowest workload
        cpu_utilizations[target_resource] *= 1.1 # increase cpu utilization.
    # Update the workload plot
    update_workload_plot(resources)


# Function to update the workload plot
def update_workload_plot(resources):
    plt.cla()
    resources_list = list(resources.keys())
    workloads = list(resources.values())
    plt.bar(resources_list, workloads, color=['blue', 'orange', 'green'])
    plt.xlabel('Resources')
    plt.ylabel('Workload')
    plt.title('Resource Workload')
    plt.tight_layout()


# Function to perform load balancing simulation
def simulate_load_balancing_at_time_step(resources, time_intervals, file_path):
    data = pd.read_csv(file_path, header=None)  # Load the time series data
    print(data.head())
    for t in time_intervals:
        # Select relevant features for clustering at the current time step
        X = data.iloc[:t + 1, :4]  # Use data up to the current time step

        # Standardize the features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Perform DBSCAN clustering at the current time step
        dbscan = DBSCAN(eps=0.5, min_samples=5)  # Adjust parameters as needed
        cluster_labels = dbscan.fit_predict(X_scaled)

        # Identify outliers as potential straggler tasks at the current time step
        straggler_indices = [i for i, label in enumerate(cluster_labels) if label == -1]

        # Simulate load balancing for identified potential straggler tasks at the current time step
        simulate_load_balancing(resources, straggler_indices)
        plt.pause(1)  # Pause for visualization


# Function to handle the button click event
def simulate_load_balancing_click():
    # Get the parameters from the GUI
    file_path = file_entry.get()
    time_intervals = range(int(time_entry.get()))
    # print("time_intervals", time_intervals)
    resources = {
        "Resource1": int(res1_entry.get()),
        "Resource2": int(res2_entry.get()),
        "Resource3": int(res3_entry.get())
    }
    # print("resources --", resources)

    # Perform load balancing simulation
    simulate_load_balancing_at_time_step(resources, time_intervals, file_path)


# Create the main window
root = tk.Tk()
root.title("Load Balancing Simulation")

# Create file path entry
file_label = tk.Label(root, text="File Path:")
file_label.grid(row=0, column=0, sticky="w")
file_entry = tk.Entry(root)
file_entry.grid(row=0, column=1)
file_button = tk.Button(root, text="Browse",
                        command=lambda: file_entry.insert(0,
                                                          filedialog.askopenfilename()))
file_button.grid(row=0, column=2)

# Create time interval entry
time_label = tk.Label(root, text="Time Intervals:")
time_label.grid(row=1, column=0, sticky="w")
time_entry = tk.Entry(root)
time_entry.grid(row=1, column=1)

# Create resource entries
res1_label = tk.Label(root, text="Resource 1 Workload:")
res1_label.grid(row=2, column=0, sticky="w")
res1_entry = tk.Entry(root)
res1_entry.grid(row=2, column=1)

res2_label = tk.Label(root, text="Resource 2 Workload:")
res2_label.grid(row=3, column=0, sticky="w")
res2_entry = tk.Entry(root)
res2_entry.grid(row=3, column=1)

res3_label = tk.Label(root, text="Resource 3 Workload:")
res3_label.grid(row=4, column=0, sticky="w")
res3_entry = tk.Entry(root)
res3_entry.grid(row=4, column=1)

# Create button to trigger simulation
simulate_button = tk.Button(root, text="Simulate Load Balancing",
                            command=simulate_load_balancing_click)
simulate_button.grid(row=5, column=0, columnspan=2)

# Initialize the workload plot
plt.figure()
plt.ion()

# Run the main event loop
root.mainloop()
