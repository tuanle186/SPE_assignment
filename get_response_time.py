import re

def get_response_time_department_router(log_file):
    response_times_dict = {}

    start_pattern = re.compile(r"\[Enqueue\] Time (\d+\.\d+): (Customer_\d+) enqueued in 'MM1Queue'")
    end_pattern = re.compile(r"\[Routed\] Time (\d+\.\d+): (Customer_\d+) has been routed to '.+'")

    enqueue_times = {}

    with open(log_file, 'r') as file:
        for line in file:
            enqueue_match = start_pattern.search(line)
            if enqueue_match:
                time = float(enqueue_match.group(1))  # Extract time as a float
                customer_id = enqueue_match.group(2)  # Extract customer ID
                enqueue_times[customer_id] = time  # Store enqueue time for this customer

            routed_match = end_pattern.search(line)
            if routed_match:
                time = float(routed_match.group(1))  # Extract time as a float
                customer_id = routed_match.group(2)  # Extract customer ID
                
                # Calculate response time if we have an enqueue time for this customer
                if customer_id in enqueue_times:
                    response_time = time - enqueue_times[customer_id]
                    response_times_dict[customer_id] = response_time  # Store response time in the dictionary
                    del enqueue_times[customer_id]  # Remove from enqueue_times as it's processed

    return sum(response_times_dict.values()) / len(response_times_dict)

def get_response_time_customer_service_department(log_file):
    response_times_dict = {}

    start_pattern = re.compile(r"\[Enqueue\] Time (\d+\.\d+): (Customer_\d+) enqueued in 'CustomerServiceQueue'")
    end_pattern = re.compile(r"\[Department CustomerService Complete\] Time (\d+\.\d+): (Customer_\d+) has completed service in 'CustomerService'")

    enqueue_times = {}

    with open(log_file, 'r') as file:
        for line in file:
            enqueue_match = start_pattern.search(line)
            if enqueue_match:
                time = float(enqueue_match.group(1))  # Extract time as a float
                customer_id = enqueue_match.group(2)  # Extract customer ID
                enqueue_times[customer_id] = time  # Store enqueue time for this customer

            routed_match = end_pattern.search(line)
            if routed_match:
                time = float(routed_match.group(1))  # Extract time as a float
                customer_id = routed_match.group(2)  # Extract customer ID
                
                # Calculate response time if we have an enqueue time for this customer
                if customer_id in enqueue_times:
                    response_time = time - enqueue_times[customer_id]
                    response_times_dict[customer_id] = response_time  # Store response time in the dictionary
                    del enqueue_times[customer_id]  # Remove from enqueue_times as it's processed

    return sum(response_times_dict.values()) / len(response_times_dict)

def get_response_time_technical_department(log_file):
    response_times_dict = {}

    start_pattern = re.compile(r"\[Enqueue\] Time (\d+\.\d+): (Customer_\d+) enqueued in 'TechnicalSupportQueue'")
    end_pattern = re.compile(r"\[Department TechnicalSupport Complete\] Time (\d+\.\d+): (Customer_\d+) has completed service in 'TechnicalSupport'")

    enqueue_times = {}

    with open(log_file, 'r') as file:
        for line in file:
            enqueue_match = start_pattern.search(line)
            if enqueue_match:
                time = float(enqueue_match.group(1))  # Extract time as a float
                customer_id = enqueue_match.group(2)  # Extract customer ID
                enqueue_times[customer_id] = time  # Store enqueue time for this customer

            routed_match = end_pattern.search(line)
            if routed_match:
                time = float(routed_match.group(1))  # Extract time as a float
                customer_id = routed_match.group(2)  # Extract customer ID
                
                # Calculate response time if we have an enqueue time for this customer
                if customer_id in enqueue_times:
                    response_time = time - enqueue_times[customer_id]
                    response_times_dict[customer_id] = response_time  # Store response time in the dictionary
                    del enqueue_times[customer_id]  # Remove from enqueue_times as it's processed

    return sum(response_times_dict.values()) / len(response_times_dict)

def get_response_time_sales_department(log_file):
    response_times_dict = {}

    start_pattern = re.compile(r"\[Enqueue\] Time (\d+\.\d+): (Customer_\d+) enqueued in 'SalesBillingQueue'")
    end_pattern = re.compile(r"\[Department SalesBilling Complete\] Time (\d+\.\d+): (Customer_\d+) has completed service in 'SalesBilling'")

    enqueue_times = {}

    with open(log_file, 'r') as file:
        for line in file:
            enqueue_match = start_pattern.search(line)
            if enqueue_match:
                time = float(enqueue_match.group(1))  # Extract time as a float
                customer_id = enqueue_match.group(2)  # Extract customer ID
                enqueue_times[customer_id] = time  # Store enqueue time for this customer

            routed_match = end_pattern.search(line)
            if routed_match:
                time = float(routed_match.group(1))  # Extract time as a float
                customer_id = routed_match.group(2)  # Extract customer ID
                
                # Calculate response time if we have an enqueue time for this customer
                if customer_id in enqueue_times:
                    response_time = time - enqueue_times[customer_id]
                    response_times_dict[customer_id] = response_time  # Store response time in the dictionary
                    del enqueue_times[customer_id]  # Remove from enqueue_times as it's processed

    return sum(response_times_dict.values()) / len(response_times_dict)
