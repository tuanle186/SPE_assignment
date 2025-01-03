from get_response_time import *
from get_waiting_time import *
from get_eq import *
import matplotlib.pyplot as plt
import math
from tabulate import tabulate

def generate_lambda(arrival_rate, dropout_rate):
    lambda_to_router = arrival_rate*(1-dropout_rate)
    lambda_to_cus_dep = (1/3)*lambda_to_router
    lambda_to_tech_dep = (2/5)*lambda_to_router
    lambda_to_sales_dep = (31/75)*lambda_to_router

    return lambda_to_cus_dep, lambda_to_tech_dep, lambda_to_sales_dep

def mm1_queue_calculator(lambda_rate, mu_rate, drop_out_rate):
    lambda_rate_Router = lambda_rate*(1-drop_out_rate)
    p = lambda_rate_Router / mu_rate

    E_r = (1 / mu_rate) / (1 - p)
    E_w = E_r - (1 / mu_rate)
    E_n = p / (1 - p)
    E_nq = pow(p,2) / (1-p)


    return {
        # 'Gateway Utilization (p)': p,
        'Mean # of customers in the system (E[n])': E_n,
        'Response Time (E[r])': E_r,
        'Mean Waiting Time (E[w])': E_w,
        'Mean # of customers in the queue (E[nq])': E_nq
    }
    
def mmc_queue_calculator(lambda_rate, mu_rate, c):
    rho = lambda_rate / (c * mu_rate)
    def erlang_c(c, rho):
        numerator = (c * rho) ** c / math.factorial(c) * 1 / (1 - rho)
        denominator = sum((c * rho) ** k / math.factorial(k) for k in range(c)) + numerator
        return numerator / denominator

    if rho >= 1:
        return {
            'Gateway Utilization (p)': rho,
            'Probability of customer forced to join the queue (C(c, ρ))': float('inf'),
            'Mean # of customers in the system (E[n])': float('inf'),
            'Mean Waiting Time (E[w])': float('inf'),
            'Mean # of customers in the queue (E[nq])': float('inf')
        }

    C_c_rho = erlang_c(c, rho)

    E_n = (rho * C_c_rho) / (1 - rho) + c * rho
    E_nq = (rho*C_c_rho)/(1-rho)
    E_r = E_n / lambda_rate
    E_w = E_nq / lambda_rate

    # Return all results
    return {
        # 'Gateway Utilization (p)': rho,
        # 'Probability of customer forced to join the queue (C(c, ρ))': C_c_rho,
        'Mean # of customers in the system (E[n])': E_n,
        'Response Time (E[r])': E_r,
        'Mean Waiting Time (E[w])': E_w,
        'Mean # of customers in the queue (E[nq])': E_nq

    }

def get_simulation_result_router(log_file, lambda_rate, unit_of_time):
    E_r = get_response_time_department_router(log_file)
    E_w = get_waiting_time_department_router(log_file)
    E_n = get_num_customer_in_router(log_file, unit_of_time)
    E_nq = get_num_customer_in_queue_of_router(log_file, unit_of_time)
    E_n = E_r*lambda_rate
    E_nq = E_w*lambda_rate
    
    return {
        'Mean # of customers in the system (E[n])': E_n,
        'Response Time (E[r])': E_r,
        'Mean Waiting Time (E[w])': E_w,
        'Mean # of customers in the queue (E[nq])': E_nq

    }

def get_simulation_result_cus_dept(log_file, lambda_rate, unit_of_time):
    E_r = get_response_time_customer_service_department(log_file)
    E_w = get_waiting_time_customer_service_department(log_file)
    E_n = get_num_customer_in_cus_dept(log_file, unit_of_time)
    E_nq = get_num_customer_in_queue_of_cus_dept(log_file, unit_of_time)
    E_n = E_r*lambda_rate
    E_nq = E_w*lambda_rate
    
    return {
        'Mean # of customers in the system (E[n])': E_n,
        'Response Time (E[r])': E_r,
        'Mean Waiting Time (E[w])': E_w,
        'Mean # of customers in the queue (E[nq])': E_nq

    }
    
def get_simulation_result_tech_dept(log_file, lambda_rate, unit_of_time):
    E_r = get_response_time_technical_department(log_file)
    E_w = get_waiting_time_technical_department(log_file)
    E_n = get_num_customer_in_tech_dept(log_file, unit_of_time)
    E_nq = get_num_customer_in_queue_of_tech_dept(log_file, unit_of_time)
    E_n = E_r*lambda_rate
    E_nq = E_w*lambda_rate
    
    return {
        'Mean # of customers in the system (E[n])': E_n,
        'Response Time (E[r])': E_r,
        'Mean Waiting Time (E[w])': E_w,
        'Mean # of customers in the queue (E[nq])': E_nq

    }
    
def get_simulation_result_sale_dept(log_file, lambda_rate, unit_of_time):
    E_r = get_response_time_sales_department(log_file)
    E_w = get_waiting_time_sales_department(log_file)
    E_n = get_num_customer_in_sale_dept(log_file, unit_of_time)
    E_nq = get_num_customer_in_queue_of_sale_dept(log_file, unit_of_time)
    # E_n = E_r*lambda_rate
    # E_nq = E_w*lambda_rate
    
    return {
        'Mean # of customers in the system (E[n])': E_n,
        'Response Time (E[r])': E_r,
        'Mean Waiting Time (E[w])': E_w,
        'Mean # of customers in the queue (E[nq])': E_nq

    }
def test_specific_log_i(i, unit_of_time):
    # Theory
    lambda_to_cus_dep, lambda_to_tech_dep, lambda_to_sales_dep = generate_lambda(i, 0.2)
    router_result = mm1_queue_calculator(i, 30, 0.2)
    cus_dep_result = mmc_queue_calculator(lambda_to_cus_dep, 4, 3)
    tech_dep_result = mmc_queue_calculator(lambda_to_tech_dep, 4, 3)
    sales_dep_result = mmc_queue_calculator(lambda_to_sales_dep, 4, 3)
    
    router_simu = get_simulation_result_router("log_tc1/local_{}.log".format(i), i, unit_of_time)
    cus_simu = get_simulation_result_cus_dept("log_tc1/local_{}.log".format(i), lambda_to_cus_dep, unit_of_time)
    tech_simu = get_simulation_result_tech_dept("log_tc1/local_{}.log".format(i), lambda_to_tech_dep, unit_of_time)
    sale_simu = get_simulation_result_sale_dept("log_tc1/local_{}.log".format(i), lambda_to_sales_dep, unit_of_time)
    


    # Replace these with your dynamically generated results
    theoretical_data = {
        "Router": router_result,
        "Customer Service": cus_dep_result,
        "Technical Support": tech_dep_result,
        "Sales": sales_dep_result
    }

    simulation_data = {
        "Router": router_simu,
        "Customer Service": cus_simu,
        "Technical Support": tech_simu,
        "Sales": sale_simu
    }

    # Prepare the table dynamically
    table = []
    for department, theory_metrics in theoretical_data.items():
        for metric, theoretical_value in theory_metrics.items():
            simulation_value = simulation_data[department].get(metric, "N/A")
            table.append([department, metric, theoretical_value, simulation_value])

    # Define headers
    headers = ["Department", "Metric", "Theoretical", "Simulation"]

    # Print the table
    print(tabulate(table, headers=headers, tablefmt="grid"))

    
unit_of_time = 1000
test_specific_log_i(20, unit_of_time)