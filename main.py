import csv
import random
from copy import deepcopy

from algorithm import algorithm

TOTAL_TASKS = 20000
MAX_TASKS_PER_SECOND = 250
# Establish a maximum arrival time for tasks, using a rate limit. This is used
# to prevent too much overflow and calculate the maximum deadline time.
ARRIVAL_TIME_MAX = 0.75 * (TOTAL_TASKS / MAX_TASKS_PER_SECOND) * 1000  # Convert to milliseconds (1 second = 1000 milliseconds)
DEADLINE_TIME_MAX = ARRIVAL_TIME_MAX * 2  # Assuming deadline is always after arrival

def generate_tasks(num_tasks):
    """Generate a list of tasks with random attributes."""
    return [
        {
            'arrival_time': random.randint(0, ARRIVAL_TIME_MAX),  # Convert to milliseconds (1 second = 1000 milliseconds)
            'execution_time': random.randint(1, round(1000 / MAX_TASKS_PER_SECOND)),
            'priority': random.randint(1, 10),
            'deadline': random.randint(ARRIVAL_TIME_MAX + 1, DEADLINE_TIME_MAX)  # Assuming deadline is always after arrival
        }
        for _ in range(num_tasks)
    ]

def main():
    # Generate initial tasks
    initial_tasks = generate_tasks(TOTAL_TASKS)

    # Initialize overall metrics
    overall_metrics = []

    # Run each algorithm
    for algo in [
        {'name': 'Round Robin', 'sort_key': 'arrival_time'},
        {'name': 'Priority Scheduling', 'sort_key': 'priority'},
        {'name': 'Earliest Deadline First', 'sort_key': 'deadline'}
    ]:
        print(algo)
        print(f"Simulating {algo['name']} algorithm...")
        
        # Create a deep copy of the initial tasks to ensure each algorithm starts with the same task queue
        task_queue = deepcopy(initial_tasks)
        
        # Run the algorithm
        metrics = algorithm(algo['sort_key'], task_queue)
        print(f"Metrics collected from {algo['name']}")

        # Log metrics to CSV
        with open(f"metrics/{algo['name']}.csv", 'w', newline='') as csvfile:
            fieldnames = metrics[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for metric in metrics:
                writer.writerow(metric)

        # Store metrics for this task
        overall_metrics.append({
            'Algorithm': algo['name'],
            'Average Waiting Time': sum([metric['Waiting Time'] for metric in metrics]) / len(metrics),
            'Lowest Waiting Time': min([metric['Waiting Time'] for metric in metrics]),
            'Lowest Waiting Time (50th Percentile)': sorted([metric['Waiting Time'] for metric in metrics])[int(len(metrics) * 0.50)],
            'Highest Waiting Time': max([metric['Waiting Time'] for metric in metrics]),
            'Highest Waiting (99th Percentile)': sorted([metric['Waiting Time'] for metric in metrics])[int(len(metrics) * 0.99)],
            'Average Completion Time': sum([metric['Completion Time'] for metric in metrics]) / len(metrics),
            'Lowest Completion Time': min([metric['Completion Time'] for metric in metrics]),
            'Lowest Completion Time (50th Percentile)': sorted([metric['Completion Time'] for metric in metrics])[int(len(metrics) * 0.50)],
            'Highest Completion Time': max([metric['Completion Time'] for metric in metrics]),
            'Highest Completion (99th Percentile)': sorted([metric['Completion Time'] for metric in metrics])[int(len(metrics) * 0.99)],
            'Average Backlog Tasks': sum([metric['Queued Tasks'] for metric in metrics]) / len(metrics),
        })

    # Log overall metrics to CSV
    with open(f"metrics/summary.csv", 'w', newline='') as csvfile:
        # Obtain headers from first algorithm
        fieldnames = overall_metrics[0].keys()

        # Write headers
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Write metrics
        for metric in overall_metrics:
            writer.writerow(metric)

if __name__ == "__main__":
    main()
