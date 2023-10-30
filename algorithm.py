
def algorithm(sort_key, task_queue):
    """Implement the Round Robin algorithm and collect metrics.
    
    Parameters:
        sort_key (str): The key to sort the task queue by.
        task_queue (list): The queue of tasks to be scheduled.
    
    Returns:
        dict: A dictionary containing the metrics collected.
    """

    metrics = []
    current_time = 0  # Initialize current time to simulate the environment
    cpu_busy_until = 0  # Time until which CPU is busy
    task_queue_arrival_order = sorted(task_queue, key=lambda x: x['arrival_time'])

    while task_queue:
        # Filter out future tasks. This isn't included in metrics because it's
        # calculating part of the simulated environment. In a real scenario, the
        # scheduler would have no knowledge of future tasks.
        current_tasks = list(filter(lambda x: x['arrival_time'] <= current_time, task_queue_arrival_order))

        # Get the next task to execute
        if (len(current_tasks) > 0):
            task = sorted(current_tasks, key=lambda x: x[sort_key])[0]
            task_queue_arrival_order.remove(task)
        else:
            # if there are no tasks to execute, increment time and continue
            current_time += 1
            continue         

        # Wait until the task's arrival time
        current_time = max(current_time, task['arrival_time'])
        
        # Wait for CPU to become free if needed
        if current_time < cpu_busy_until:
            current_time = cpu_busy_until
        
        # Calculate waiting time (time spent in queue)
        waiting_time = current_time - task['arrival_time']
        
        # Execute the task
        current_time += task['execution_time']
        cpu_busy_until = current_time  # CPU will be busy until this time
        
        # Calculate response time
        response_time = current_time - task['arrival_time']
        
        # Store metrics for this task
        metrics.append({
            'Task ID': len(metrics),
            'Arrival Timestamp': task['arrival_time'],
            'Completion Timestamp': current_time,
            'Waiting Time': waiting_time,
            'Completion Time': response_time,
            'Queued Tasks': len(current_tasks) - 1,
        })

        # Remove the task from the queue
        task_queue.remove(task)

    return metrics
