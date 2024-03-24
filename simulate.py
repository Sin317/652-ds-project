import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt


# Function to simulate load balancing for identified potential straggler tasks using WLOR algorithm
# Function to simulate load balancing for identified potential straggler tasks using WLOR algorithm
def simulate_load_balancing(resources, straggler_tasks):
    # Assign weights to resources based on their current workload
    total_workload = sum(len(tasks) for tasks in resources.values())
    weights = {resource: len(tasks) / total_workload for resource, tasks in resources.items()}

    def calculate_load(resource):
        return len(resources[resource]) * (1 - weights[resource])

    for straggler_task in straggler_tasks:
        # Calculate the remaining time for the straggler task on each resource
        remaining_time = {resource: max(0, straggler_task[1] - max(task[1] for task in resources[resource])) for resource in resources}

        # Calculate the weighted least outstanding requests for each resource
        outstanding_requests = {resource: calculate_load(resource) for resource in resources}

        # Assign the straggler task to the resource with the least outstanding requests
        target_resource = min(outstanding_requests, key=outstanding_requests.get)
        resources[target_resource].append(straggler_task)

    # Update the workload plot
    update_workload_plot(resources)



# Function to update the workload plot
def update_workload_plot(resources):
    plt.cla()
    resources_list = list(resources.keys())
    workloads = [len(tasks) for tasks in resources.values()]
    plt.bar(resources_list, workloads, color=['blue', 'orange', 'green'])
    plt.xlabel('Resources')
    plt.ylabel('Number of Tasks')
    plt.title('Resource Workload')
    plt.tight_layout()


# Function to perform load balancing simulation
def simulate_load_balancing_at_time_step(resources, straggler_tasks, file_path):
    data = pd.read_csv(file_path, header=None)  # Load the time series data
    for _, row in data.iterrows():
        # Simulate load balancing for identified potential straggler tasks at the current time step
        simulate_load_balancing(resources, straggler_tasks)
        plt.pause(1)  # Pause for visualization


# Function to handle the button click event
def simulate_load_balancing_click():
    # Get the parameters from the GUI
    file_path = file_entry.get()

    # Initialize resources with no tasks initially
    resources = {
        "Resource1": [],
        "Resource2": [],
        "Resource3": []
    }

    # Initialize straggler tasks list
    straggler_tasks = []

    # Perform load balancing simulation
    simulate_load_balancing_at_time_step(resources, straggler_tasks, file_path)


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

# Create button to trigger simulation
simulate_button = tk.Button(root, text="Simulate Load Balancing",
                            command=simulate_load_balancing_click)
simulate_button.grid(row=1, column=0, columnspan=2)

# Initialize the workload plot
plt.figure()
plt.ion()

# Run the main event loop
root.mainloop()

