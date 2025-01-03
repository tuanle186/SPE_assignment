import re

def get_num_customer_in_queue_of_router(log_file, unit_of_time):
    # Dictionary to store total time spent in each state
    state_num_customer = {}
    
    # Pattern to extract time and the number of customers
    pattern = re.compile(r"\[Update router\] Time (\d+\.\d+): Number of customer in queue of router is (\d+)")
    
    prev_time = 0
    prev_state = None
    
    row_count = 0
    with open(log_file, 'r') as file:
        row_count = sum(1 for line in file)
        
    with open(log_file, 'r') as file:
        counter = 0
        for line in file:
            counter += 1
            match = pattern.search(line)
            if match:
                # Extract time and state from the log line
                current_time = float(match.group(1))
                current_state = int(match.group(2))
                
                # If this is not the first state, calculate the duration of the previous state
                if prev_state is not None:
                    duration = current_time - prev_time
                    state_num_customer[prev_state] = state_num_customer.get(prev_state, 0) + duration
                
                # Update the previous time and state
                prev_time = current_time
                prev_state = current_state

            if counter == row_count:
                duration = unit_of_time - prev_time
                state_num_customer[prev_state] = state_num_customer.get(prev_state, 0) + duration
                
    sum_ret = 0
    for key, values in state_num_customer.items():
        sum_ret += key*values
    
    # Return the result as a dictionary
    return sum_ret/unit_of_time


def get_num_customer_in_router(log_file, unit_of_time):
    # Dictionary to store total time spent in each state
    state_num_customer = {}
    
    # Pattern to extract time and the number of customers
    pattern = re.compile(r"\[Update router\] Time (\d+\.\d+): Number of customer in router is (\d+)")
    
    prev_time = 0
    prev_state = None
    
    with open(log_file, 'r') as file:
        for line in file:
            match = pattern.search(line)
            if match:
                # Extract time and state from the log line
                current_time = float(match.group(1))
                current_state = int(match.group(2))
                
                # If this is not the first state, calculate the duration of the previous state
                if prev_state is not None:
                    duration = current_time - prev_time
                    state_num_customer[prev_state] = state_num_customer.get(prev_state, 0) + duration
                
                # Update the previous time and state
                prev_time = current_time
                prev_state = current_state
    
    sum_ret = 0
    for key, values in state_num_customer.items():
        sum_ret += key*values
    
    # Return the result as a dictionary
    return sum_ret/unit_of_time

def get_num_customer_in_queue_of_cus_dept(log_file, unit_of_time):
    # Dictionary to store total time spent in each state
    state_num_customer = {}
    
    # Pattern to extract time and the number of customers
    pattern = re.compile(r"\[Update CustomerService\] Time (\d+\.\d+): Number of customer in queue of customer dept is (\d+)")
    
    prev_time = 0
    prev_state = None
    
    with open(log_file, 'r') as file:
        for line in file:
            match = pattern.search(line)
            if match:
                # Extract time and state from the log line
                current_time = float(match.group(1))
                current_state = int(match.group(2))
                
                # If this is not the first state, calculate the duration of the previous state
                if prev_state is not None:
                    duration = current_time - prev_time
                    state_num_customer[prev_state] = state_num_customer.get(prev_state, 0) + duration
                
                # Update the previous time and state
                prev_time = current_time
                prev_state = current_state
    
    sum_ret = 0
    for key, values in state_num_customer.items():
        sum_ret += key*values
    
    # Return the result as a dictionary
    return sum_ret/unit_of_time


def get_num_customer_in_cus_dept(log_file, unit_of_time):
    # Dictionary to store total time spent in each state
    state_num_customer = {}
    
    # Pattern to extract time and the number of customers
    pattern = re.compile(r"\[Update CustomerService\] Time (\d+\.\d+): Number of customer in customer dept is (\d+)")
    
    prev_time = 0
    prev_state = None
    
    with open(log_file, 'r') as file:
        for line in file:
            match = pattern.search(line)
            if match:
                # Extract time and state from the log line
                current_time = float(match.group(1))
                current_state = int(match.group(2))
                
                # If this is not the first state, calculate the duration of the previous state
                if prev_state is not None:
                    duration = current_time - prev_time
                    state_num_customer[prev_state] = state_num_customer.get(prev_state, 0) + duration
                
                # Update the previous time and state
                prev_time = current_time
                prev_state = current_state
    
    sum_ret = 0
    for key, values in state_num_customer.items():
        sum_ret += key*values
    
    # Return the result as a dictionary
    return sum_ret/unit_of_time

def get_num_customer_in_queue_of_tech_dept(log_file, unit_of_time):
    # Dictionary to store total time spent in each state
    state_num_customer = {}
    
    # Pattern to extract time and the number of customers
    pattern = re.compile(r"\[Update TechnicalSupport\] Time (\d+\.\d+): Number of customer in queue of technical dept is (\d+)")
    
    prev_time = 0
    prev_state = None
    
    with open(log_file, 'r') as file:
        for line in file:
            match = pattern.search(line)
            if match:
                # Extract time and state from the log line
                current_time = float(match.group(1))
                current_state = int(match.group(2))
                
                # If this is not the first state, calculate the duration of the previous state
                if prev_state is not None:
                    duration = current_time - prev_time
                    state_num_customer[prev_state] = state_num_customer.get(prev_state, 0) + duration
                
                # Update the previous time and state
                prev_time = current_time
                prev_state = current_state
    
    sum_ret = 0
    for key, values in state_num_customer.items():
        sum_ret += key*values
    
    # Return the result as a dictionary
    return sum_ret/unit_of_time


def get_num_customer_in_tech_dept(log_file, unit_of_time):
    # Dictionary to store total time spent in each state
    state_num_customer = {}
    
    # Pattern to extract time and the number of customers
    pattern = re.compile(r"\[Update TechnicalSupport\] Time (\d+\.\d+): Number of customer in technical dept is (\d+)")
    
    prev_time = 0
    prev_state = None
    
    with open(log_file, 'r') as file:
        for line in file:
            match = pattern.search(line)
            if match:
                # Extract time and state from the log line
                current_time = float(match.group(1))
                current_state = int(match.group(2))
                
                # If this is not the first state, calculate the duration of the previous state
                if prev_state is not None:
                    duration = current_time - prev_time
                    state_num_customer[prev_state] = state_num_customer.get(prev_state, 0) + duration
                
                # Update the previous time and state
                prev_time = current_time
                prev_state = current_state
    
    sum_ret = 0
    for key, values in state_num_customer.items():
        sum_ret += key*values
    
    # Return the result as a dictionary
    return sum_ret/unit_of_time

def get_num_customer_in_queue_of_sale_dept(log_file, unit_of_time):
    # Dictionary to store total time spent in each state
    state_num_customer = {}
    
    # Pattern to extract time and the number of customers
    pattern = re.compile(r"\[Update SalesBilling\] Time (\d+\.\d+): Number of customer in queue of sale dept is (\d+)")
    
    prev_time = 0
    prev_state = None
    
    with open(log_file, 'r') as file:
        for line in file:
            match = pattern.search(line)
            if match:
                # Extract time and state from the log line
                current_time = float(match.group(1))
                current_state = int(match.group(2))
                
                # If this is not the first state, calculate the duration of the previous state
                if prev_state is not None:
                    duration = current_time - prev_time
                    state_num_customer[prev_state] = state_num_customer.get(prev_state, 0) + duration
                
                # Update the previous time and state
                prev_time = current_time
                prev_state = current_state
    
    sum_ret = 0
    for key, values in state_num_customer.items():
        sum_ret += key*values
    
    # Return the result as a dictionary
    return sum_ret/unit_of_time


def get_num_customer_in_sale_dept(log_file, unit_of_time):
    # Dictionary to store total time spent in each state
    state_num_customer = {}
    
    # Pattern to extract time and the number of customers
    pattern = re.compile(r"\[Update SalesBilling\] Time (\d+\.\d+): Number of customer in sale dept is (\d+)")
    
    prev_time = 0
    prev_state = None
    
    with open(log_file, 'r') as file:
        for line in file:
            match = pattern.search(line)
            if match:
                # Extract time and state from the log line
                current_time = float(match.group(1))
                current_state = int(match.group(2))
                
                # If this is not the first state, calculate the duration of the previous state
                if prev_state is not None:
                    duration = current_time - prev_time
                    state_num_customer[prev_state] = state_num_customer.get(prev_state, 0) + duration
                
                # Update the previous time and state
                prev_time = current_time
                prev_state = current_state
    
    sum_ret = 0
    for key, values in state_num_customer.items():
        sum_ret += key*values
    
    # Return the result as a dictionary
    return sum_ret/unit_of_time




# get_num_customer_in_queue_of_router("log_tc1/local_20.log", 200)