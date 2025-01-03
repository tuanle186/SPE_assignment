import matplotlib.pyplot as plt
from get_response_time import *
from get_waiting_time import *
from get_eq import *
import os

folder_path = "output/testcase1/mm1"

# Check if the folder exists
if not os.path.exists(folder_path):
    # Create the folder if it doesn't exist
    os.makedirs(folder_path)
    print(f"Folder '{folder_path}' created.")
else:
    print(f"Folder '{folder_path}' already exists.")
    
def mm1_queue_calculator(lambda_rate, mu_rate, drop_out_rate):
    lambda_rate_Router = lambda_rate*(1-drop_out_rate)
    p = lambda_rate_Router / mu_rate

    E_r = (1 / mu_rate) / (1 - p)
    E_w = E_r - (1 / mu_rate)
    E_n = p / (1 - p)
    E_nq = pow(p,2) / (1-p)


    return {
        'Gateway Utilization (p)': p,
        'Mean # of customers in the system (E[n])': E_n,
        'Response Time (E[r])': E_r,
        'Mean Waiting Time (E[w])': E_w,
        'Mean # of customers in the queue (E[nq])': E_nq
    }

service_rate_router = 30    # Service rate (customers per hour)
drop_out_rate = 0.2         # Dropout rate

lambda_rates = list(range(1, 31)) # 1 to 30
E_n_values_theory = []
E_nq_values_theory = []
E_w_values_theory = []
E_r_values_theory = []

E_n_values_simu = []
E_nq_values_simu = []
E_w_values_simu = []
E_r_values_simu = []

p_values = []

for lambda_rate in lambda_rates:
    results = mm1_queue_calculator(lambda_rate, service_rate_router, drop_out_rate)
    p_values.append(results['Gateway Utilization (p)'])
    E_n_values_theory.append(results['Mean # of customers in the system (E[n])'])
    E_nq_values_theory.append(results['Mean # of customers in the queue (E[nq])'])
    E_w_values_theory.append(results['Mean Waiting Time (E[w])'])
    E_r_values_theory.append(results['Response Time (E[r])'])

unit_of_time = 3000

for lambda_rate in lambda_rates:
    res_time_dep_router = get_response_time_department_router("log_tc1/local_{}.log".format(lambda_rate))
    E_r_values_simu.append(res_time_dep_router)
    
    wait_time_dep_router = get_waiting_time_department_router("log_tc1/local_{}.log".format(lambda_rate))
    E_w_values_simu.append(wait_time_dep_router)
    
    E_n_values_simu.append(get_num_customer_in_router("log_tc1/local_{}.log".format(lambda_rate), unit_of_time))
    E_nq_values_simu.append(get_num_customer_in_queue_of_router("log_tc1/local_{}.log".format(lambda_rate), unit_of_time))
    
    print("Done log {}".format(lambda_rate))


# Plot p vs Lambda Rate
plt.figure(figsize=(10, 5))
plt.plot(lambda_rates, p_values, marker='o', color='orange')
plt.xlabel("Lambda Rate")
plt.ylabel("Resource Utilization (p) of router")
plt.title("p vs Lambda Rate")
plt.grid(True)
plt.savefig("output/testcase1/mm1/p_of_router_tc1.png", dpi=300) 
plt.close()

# Plot E[n], E[nq] vs Lambda Rate
plt.figure(figsize=(10, 5))
plt.plot(lambda_rates, E_n_values_theory, marker='.', color='red', label="E[n] of router - theory")
plt.plot(lambda_rates, E_n_values_simu, marker='.', color='green', label="E[n] of router - simulation")
plt.plot(lambda_rates, E_nq_values_theory, marker='.', color='orange', label="E[nq] of router - theory")
plt.plot(lambda_rates, E_nq_values_simu, marker='.', color='blue', label="E[nq] of router - simulation")
plt.xlabel("Lambda Rate")
plt.ylabel("E[n], E[nq]")
plt.title("E[n], E[nq] vs Lambda Rate")
plt.grid(True)
plt.legend()
plt.savefig("output/testcase1/mm1/en_and_enq_of_router_tc1.png", dpi=300)  # Save with 300 DPI for high quality
plt.close()

# Plot E[r], E[w] vs Lambda Rate
plt.figure(figsize=(10, 5))
plt.plot(lambda_rates, E_w_values_theory, marker='.', color='red', label="E[w] of router - theory")
plt.plot(lambda_rates, E_w_values_simu, marker='.', color='green', label="E[w] of router - simulation")
plt.plot(lambda_rates, E_r_values_theory, marker='.', color='orange', label="E[r] of router - theory")
plt.plot(lambda_rates, E_r_values_simu, marker='.', color='blue', label="E[r] of router - simulation")
plt.xlabel("Lambda Rate")
plt.ylabel("E[w], E[r]")
plt.title("E[w], E[r] vs Lambda Rate")
plt.legend()
plt.grid(True)
plt.savefig("output/testcase1/mm1/ew_and_er_of_router_tc1.png", dpi=300)
plt.close()

