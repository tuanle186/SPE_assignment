import matplotlib.pyplot as plt
from get_response_time import *
from get_waiting_time import *
from get_eq import *
import math
import os

folder_path = "output/testcase2/mmc"

# Check if the folder exists
if not os.path.exists(folder_path):
    # Create the folder if it doesn't exist
    os.makedirs(folder_path)
    print(f"Folder '{folder_path}' created.")
else:
    print(f"Folder '{folder_path}' already exists.")
    
def generate_lambda(arrival_rate, dropout_rate):
    lambda_to_router = arrival_rate*(1-dropout_rate)
    lambda_to_cus_dep = (1/3)*lambda_to_router
    lambda_to_tech_dep = (2/5)*lambda_to_router
    lambda_to_sales_dep = (31/75)*lambda_to_router

    return lambda_to_cus_dep, lambda_to_tech_dep, lambda_to_sales_dep

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
        'Gateway Utilization (p)': rho,
        'Probability of customer forced to join the queue (C(c, ρ))': C_c_rho,
        'Mean # of customers in the system (E[n])': E_n,
        'Response Time (E[r])': E_r,
        'Mean Waiting Time (E[w])': E_w,
        'Mean # of customers in the queue (E[nq])': E_nq

    }

unit_of_time = 100

service_rate_router = list(range(6, 16))    # Service rate (customers per hour)
service_rate_dep = 20                       # Serivce rate of department
c = 3                                       # Number of server of each department
drop_out_rate = 0.2                         # Dropout rate

lambda_rate = 5

# Customer department
E_n_values_cus_theory = []
E_nq_values_cus_theory = []
E_w_values_cus_theory = []
E_r_values_cus_theory = []

E_n_values_cus_simu = []
E_nq_values_cus_simu = []
E_w_values_cus_simu = []
E_r_values_cus_simu = []

p_values_cus = []

# Technical department
E_n_values_tech_theory = []
E_nq_values_tech_theory = []
E_w_values_tech_theory = []
E_r_values_tech_theory = []

E_n_values_tech_simu = []
E_nq_values_tech_simu = []
E_w_values_tech_simu = []
E_r_values_tech_simu = []

p_values_tech = []

# Sales department
E_n_values_sale_theory = []
E_nq_values_sale_theory = []
E_w_values_sale_theory = []
E_r_values_sale_theory = []

E_n_values_sale_simu = []
E_nq_values_sale_simu = []
E_w_values_sale_simu = []
E_r_values_sale_simu = []

p_values_sale = []

#------------THEORY----------------#
for service_rate in service_rate_router:
    lambda_to_cus_dep, lambda_to_tech_dep, lambda_to_sales_dep = generate_lambda(lambda_rate, drop_out_rate)
    cus_dep_result = mmc_queue_calculator(lambda_to_cus_dep, service_rate_dep, c)
    tech_dep_result = mmc_queue_calculator(lambda_to_tech_dep, service_rate_dep, c)
    sales_dep_result = mmc_queue_calculator(lambda_to_sales_dep, service_rate_dep, c)
    
    p_values_cus.append(cus_dep_result['Gateway Utilization (p)'])
    E_n_values_cus_theory.append(cus_dep_result['Mean # of customers in the system (E[n])'])
    E_nq_values_cus_theory.append(cus_dep_result['Mean # of customers in the queue (E[nq])'])
    E_w_values_cus_theory.append(cus_dep_result['Mean Waiting Time (E[w])'])
    E_r_values_cus_theory.append(cus_dep_result['Response Time (E[r])'])
    
    p_values_tech.append(tech_dep_result['Gateway Utilization (p)'])
    E_n_values_tech_theory.append(tech_dep_result['Mean # of customers in the system (E[n])'])
    E_nq_values_tech_theory.append(tech_dep_result['Mean # of customers in the queue (E[nq])'])
    E_w_values_tech_theory.append(tech_dep_result['Mean Waiting Time (E[w])'])
    E_r_values_tech_theory.append(tech_dep_result['Response Time (E[r])'])
    
    p_values_sale.append(sales_dep_result['Gateway Utilization (p)'])
    E_n_values_sale_theory.append(sales_dep_result['Mean # of customers in the system (E[n])'])
    E_nq_values_sale_theory.append(sales_dep_result['Mean # of customers in the queue (E[nq])'])
    E_w_values_sale_theory.append(sales_dep_result['Mean Waiting Time (E[w])'])
    E_r_values_sale_theory.append(sales_dep_result['Response Time (E[r])'])

#------------SIMULATION----------------#
for service_rate in service_rate_router:
    res_time_customer_service_dep = get_response_time_customer_service_department("log_tc2/local_{}.log".format(service_rate))
    E_r_values_cus_simu.append(res_time_customer_service_dep)
    
    res_time_tech_dep = get_response_time_technical_department("log_tc2/local_{}.log".format(service_rate))
    E_r_values_tech_simu.append(res_time_tech_dep)

    res_time_sales_dep = get_response_time_sales_department("log_tc2/local_{}.log".format(service_rate))
    E_r_values_sale_simu.append(res_time_sales_dep)
    
    wait_time_customer_service_dep = get_waiting_time_customer_service_department("log_tc2/local_{}.log".format(service_rate))
    E_w_values_cus_simu.append(wait_time_customer_service_dep)

    wait_time_tech_dep = get_waiting_time_technical_department("log_tc2/local_{}.log".format(service_rate))
    E_w_values_tech_simu.append(wait_time_tech_dep)
    
    wait_time_sales_dep = get_waiting_time_sales_department("log_tc2/local_{}.log".format(service_rate))
    E_w_values_sale_simu.append(wait_time_sales_dep)
    
    E_n_values_cus_simu.append(get_num_customer_in_cus_dept("log_tc2/local_{}.log".format(service_rate), unit_of_time))
    E_nq_values_cus_simu.append(get_num_customer_in_queue_of_cus_dept("log_tc2/local_{}.log".format(service_rate), unit_of_time))
    
    E_n_values_tech_simu.append(get_num_customer_in_tech_dept("log_tc2/local_{}.log".format(service_rate), unit_of_time))
    E_nq_values_tech_simu.append(get_num_customer_in_queue_of_tech_dept("log_tc2/local_{}.log".format(service_rate), unit_of_time))
    
    E_n_values_sale_simu.append(get_num_customer_in_sale_dept("log_tc2/local_{}.log".format(service_rate), unit_of_time))
    E_nq_values_sale_simu.append(get_num_customer_in_queue_of_sale_dept("log_tc2/local_{}.log".format(service_rate), unit_of_time))
    
    # E_n_values_cus_simu.append(res_time_customer_service_dep*lambda_rate)
    # E_nq_values_cus_simu.append(wait_time_customer_service_dep*lambda_rate)
    
    # E_n_values_tech_simu.append(res_time_tech_dep*lambda_rate)
    # E_nq_values_tech_simu.append(wait_time_tech_dep*lambda_rate)
    
    # E_n_values_sale_simu.append(res_time_sales_dep*lambda_rate)
    # E_nq_values_sale_simu.append(wait_time_sales_dep*lambda_rate)
    
    print("Done log {}".format(service_rate))



# Plot p vs Service Rate
plt.figure(figsize=(10, 5))
plt.plot(service_rate_router, p_values_cus, marker='o', color='red', label="Resourse utilization - Customer department")
plt.plot(service_rate_router, p_values_tech, marker='o', color='green', label="Resourse utilization - Technical department")
plt.plot(service_rate_router, p_values_sale, marker='o', color='blue', label="Resourse utilization - Sales department")
plt.xlabel("Service Rate")
plt.ylabel("Resource Utilization (p) of departments")
plt.title("p vs Service Rate")
plt.legend()
plt.grid(True)
plt.savefig("output/testcase2/mmc/p_of_departments_tc2.png", dpi=300) 
plt.close()

# Plot E[n] vs Service Rate
plt.figure(figsize=(10, 5))
plt.plot(service_rate_router, E_n_values_cus_theory, marker='.', color='red', label="E[n] of customer dept - theory")
plt.plot(service_rate_router, E_n_values_cus_simu, marker='.', color='green', label="E[n] of customer dept - simulation")
plt.plot(service_rate_router, E_n_values_tech_theory, marker='.', color='orange', label="E[n] of technical dept - theory")
plt.plot(service_rate_router, E_n_values_tech_simu, marker='.', color='purple', label="E[n] of technical dept - simulation")
plt.plot(service_rate_router, E_n_values_sale_theory, marker='.', color='blue', label="E[n] of sale dept - theory")
plt.plot(service_rate_router, E_n_values_sale_simu, marker='.', color='brown', label="E[n] of sale dept - simulation")
plt.xlabel("Service Rate")
plt.ylabel("E[n]")
plt.title("E[n] vs Service Rate")
plt.grid(True)
plt.legend()
plt.savefig("output/testcase2/mmc/en_of_3_depts_tc2.png", dpi=300)  # Save with 300 DPI for high quality
plt.close()

# Plot E[nq] vs Service Rate
plt.figure(figsize=(10, 5))
plt.plot(service_rate_router, E_nq_values_cus_theory, marker='.', color='red', label="E[nq] of customer dept - theory")
plt.plot(service_rate_router, E_nq_values_cus_simu, marker='.', color='green', label="E[nq] of customer dept - simulation")
plt.plot(service_rate_router, E_nq_values_tech_theory, marker='.', color='orange', label="E[nq] of technical dept - theory")
plt.plot(service_rate_router, E_nq_values_tech_simu, marker='.', color='purple', label="E[nq] of technical dept - simulation")
plt.plot(service_rate_router, E_nq_values_sale_theory, marker='.', color='blue', label="E[nq] of sale dept - theory")
plt.plot(service_rate_router, E_nq_values_sale_simu, marker='.', color='brown', label="E[nq] of sale dept - simulation")
plt.xlabel("Service Rate")
plt.ylabel("E[nq]")
plt.title("E[nq] vs Service Rate")
plt.grid(True)
plt.legend()
plt.savefig("output/testcase2/mmc/enq_of_3_depts_tc2.png", dpi=300)  # Save with 300 DPI for high quality
plt.close()

# Plot E[w] vs Service Rate
plt.figure(figsize=(10, 5))
plt.plot(service_rate_router, E_w_values_cus_theory, marker='.', color='red', label="E[w] of customer dept - theory")
plt.plot(service_rate_router, E_w_values_cus_simu, marker='.', color='green', label="E[w] of customer dept - simulation")
plt.plot(service_rate_router, E_w_values_tech_theory, marker='.', color='orange', label="E[w] of technical dept - theory")
plt.plot(service_rate_router, E_w_values_tech_simu, marker='.', color='purple', label="E[w] of technical dept - simulation")
plt.plot(service_rate_router, E_w_values_sale_theory, marker='.', color='blue', label="E[w] of sale dept - theory")
plt.plot(service_rate_router, E_w_values_sale_simu, marker='.', color='brown', label="E[w] of sale dept - simulation")
plt.xlabel("Service Rate")
plt.ylabel("E[w]")
plt.title("E[w] vs Service Rate")
plt.legend()
plt.grid(True)
plt.savefig("output/testcase2/mmc/ew_of_3_depts_tc2.png", dpi=300)
plt.close()

# Plot E[r] vs Service Rate
plt.figure(figsize=(10, 5))
plt.plot(service_rate_router, E_r_values_cus_theory, marker='.', color='red', label="E[r] of customer dept - theory")
plt.plot(service_rate_router, E_r_values_cus_simu, marker='.', color='green', label="E[r] of customer dept - simulation")
plt.plot(service_rate_router, E_r_values_tech_theory, marker='.', color='orange', label="E[r] of technical dept - theory")
plt.plot(service_rate_router, E_r_values_tech_simu, marker='.', color='purple', label="E[r] of technical dept - simulation")
plt.plot(service_rate_router, E_r_values_sale_theory, marker='.', color='blue', label="E[r] of sale dept - theory")
plt.plot(service_rate_router, E_r_values_sale_simu, marker='.', color='brown', label="E[r] of sale dept - simulation")
plt.xlabel("Service Rate")
plt.ylabel("E[r]")
plt.title("E[r] vs Service Rate")
plt.legend()
plt.grid(True)
plt.savefig("output/testcase2/mmc/er_of_3_depts_tc2.png", dpi=300)
plt.close()