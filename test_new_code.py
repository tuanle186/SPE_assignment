import logging
import simpy
import random
import os


def configure_logger(log_path):
    """Configures the logger with a specific file path."""
    logger = logging.getLogger('my_logger')
    logger.handlers = []  # Clear existing handlers to avoid duplicate logs
    logger.setLevel(logging.INFO)

    # Create handlers
    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(log_path)

    # Set level for handlers
    console_handler.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)

    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

# Number of queue in router
class numberCustomer:
    def __init__(self):
        self.num_customer_in_router_queue       = 0
        self.num_customer_in_router             = 0
        self.num_customer_in_cus_dept_queue     = 0
        self.num_customer_in_cus_dept           = 0
        self.num_customer_in_tech_dept_queue    = 0
        self.num_customer_in_tech_dept          = 0
        self.num_customer_in_sale_dept_queue    = 0
        self.num_customer_in_sale_dept          = 0


# ArrivalEvent Class
class CustomerGenerator:
    def __init__(self, env: simpy.Environment, arrival_rate: float, service_rate_router: float, service_rate_dept: float, num_customer: numberCustomer):
        self.env = env
        self.customer_id = 0  # To assign unique IDs to customers
        
        self.arrival_rate = arrival_rate
        self.service_rate_router = service_rate_router
        self.service_rate_dept = service_rate_dept
        
        self.router = simpy.Resource(env, capacity=1)
        self.agents_customer = simpy.Resource(env, capacity=3)
        self.agents_technical = simpy.Resource(env, capacity=3)
        self.agents_sales = simpy.Resource(env, capacity=3)
        
        self.env.process(self.generateArrival())
        
        self.num_customer = num_customer

    @staticmethod
    def ProbGen():
        request_type = random.choice(['CustomerService', 'TechnicalSupport', 'SalesBilling'])
        is_leaving = random.random() < 0.2
        return request_type, is_leaving

    def generateArrival(self):
        while True:
            request_type, is_leaving = CustomerGenerator.ProbGen()
            self.customer_id += 1
            customer = Customer(self.env, f'Customer_{self.customer_id}', request_type, self.service_rate_router, self.service_rate_dept, self.router, self.agents_customer, self.agents_technical, self.agents_sales, self.num_customer)

            logger.info(f"[Arrival] Time {self.env.now}: {customer.customerID} arrives with request type '{customer.requestType}'")
            if is_leaving:
                logger.info(f"[Leave Early - Level 1] Time {self.env.now:.2f}: {customer.customerID} leaves without joining the queue")
            else:
                logger.info(f"[Enqueue] Time {self.env.now}: Customer_{self.customer_id} enqueued in 'MM1Queue'")
                
                self.num_customer.num_customer_in_router_queue  += 1
                self.num_customer.num_customer_in_router        += 1
                logger.info(f"[Update router] Time {self.env.now}: Number of customer in queue of router is {self.num_customer.num_customer_in_router_queue}")
                logger.info(f"[Update router] Time {self.env.now}: Number of customer in router is {self.num_customer.num_customer_in_router}")

                self.env.process(customer.run())
            
            inter_arrival_time = random.expovariate(self.arrival_rate)
            yield self.env.timeout(inter_arrival_time)

class Customer:
    def __init__(self, env: simpy.Environment, customer_id, request_type, service_rate_router: float, service_rate_dept: float, router: simpy.Resource, agents_customer: simpy.Resource, agents_technical: simpy.Resource, agents_sales: simpy.Resource, num_customer: numberCustomer):
        self.env = env
        
        self.customerID = customer_id
        self.requestType = request_type  # 'CustomerService', 'TechnicalSupport', 'SalesBilling'
        self.service_rate_router = service_rate_router
        self.service_rate_dept = service_rate_dept
        
        self.router = router
        self.agents_customer = agents_customer
        self.agents_technical = agents_technical
        self.agents_sales = agents_sales
        
        self.num_customer = num_customer
        
    def serve_customer(self, departmentName):
        service_time = random.expovariate(self.service_rate_dept)
        logger.info(f"[Department {departmentName} Starts] Time {self.env.now}: {self.customerID} starts service in '{departmentName}'")
        yield self.env.timeout(service_time)
        logger.info(f"[Department {departmentName} Complete] Time {self.env.now}: {self.customerID} has completed service in '{departmentName}'")
        
        if (departmentName == 'CustomerService'):
            self.num_customer.num_customer_in_cus_dept -= 1
            logger.info(f"[Update {self.requestType}] Time {self.env.now}: Number of customer in customer dept is {self.num_customer.num_customer_in_cus_dept}")

        elif (departmentName == 'TechnicalSupport'):
            self.num_customer.num_customer_in_tech_dept -= 1
            logger.info(f"[Update {self.requestType}] Time {self.env.now}: Number of customer in technical dept is {self.num_customer.num_customer_in_tech_dept}")
        
        else:
            self.num_customer.num_customer_in_sale_dept -= 1
            logger.info(f"[Update {self.requestType}] Time {self.env.now}: Number of customer in sale dept is {self.num_customer.num_customer_in_sale_dept}")
        
        # Apply department-specific probability for repeat request
        if self.requestType != 'SalesBilling' and random.random() < 0.2:
            self.handle_switching_queue()

    def handle_switching_queue(self):
        original_request_type = self.requestType
        if original_request_type == 'CustomerService':
          new_request_type = 'TechnicalSupport'
        elif original_request_type == 'TechnicalSupport':
          new_request_type = 'SalesBilling'
        else:
          raise NotImplementedError("nah son")

        self.requestType = new_request_type

        logger.info(f"[Switching queue] Time {self.env.now}: {self.customerID} switches queue, changing request from '{original_request_type}' to '{new_request_type}'")

    def run(self):
        with self.router.request() as request:
            yield request
            
            logger.info(f"[Dequeue] Time {self.env.now}: {self.customerID} dequeued from 'MM1Queue'")
            self.num_customer.num_customer_in_router_queue -= 1
            logger.info(f"[Update router] Time {self.env.now}: Number of customer in queue of router is {self.num_customer.num_customer_in_router_queue}")
            
            service_time = random.expovariate(self.service_rate_router)
            yield self.env.timeout(service_time)
            logger.info(f"[Routed] Time {self.env.now}: {self.customerID} has been routed to '{self.requestType}'")
            
            self.num_customer.num_customer_in_router -= 1
            logger.info(f"[Update router] Time {self.env.now}: Number of customer in router is {self.num_customer.num_customer_in_router}")

            
        if (self.requestType == 'CustomerService'):
            logger.info(f"[Enqueue] Time {self.env.now}: {self.customerID} enqueued in 'CustomerServiceQueue'")
            
            self.num_customer.num_customer_in_cus_dept_queue += 1
            self.num_customer.num_customer_in_cus_dept += 1
            
            logger.info(f"[Update {self.requestType}] Time {self.env.now}: Number of customer in queue of customer dept is {self.num_customer.num_customer_in_cus_dept_queue}")
            logger.info(f"[Update {self.requestType}] Time {self.env.now}: Number of customer in customer dept is {self.num_customer.num_customer_in_cus_dept}")

            
            with self.agents_customer.request() as request:
                yield request
                logger.info(f"[Dequeue] Time {self.env.now}: {self.customerID} dequeued from 'CustomerServiceQueue'")
                
                self.num_customer.num_customer_in_cus_dept_queue -= 1
                logger.info(f"[Update {self.requestType}] Time {self.env.now}: Number of customer in queue of customer dept is {self.num_customer.num_customer_in_cus_dept_queue}")

                yield self.env.process(self.serve_customer(self.requestType))
            

        if (self.requestType == 'TechnicalSupport'):
            logger.info(f"[Enqueue] Time {self.env.now}: {self.customerID} enqueued in 'TechnicalSupportQueue'")

            self.num_customer.num_customer_in_tech_dept_queue += 1
            self.num_customer.num_customer_in_tech_dept += 1
            
            logger.info(f"[Update {self.requestType}] Time {self.env.now}: Number of customer in queue of technical dept is {self.num_customer.num_customer_in_tech_dept_queue}")
            logger.info(f"[Update {self.requestType}] Time {self.env.now}: Number of customer in technical dept is {self.num_customer.num_customer_in_tech_dept}")

            with self.agents_technical.request() as request:
                yield request
                logger.info(f"[Dequeue] Time {self.env.now}: {self.customerID} dequeued from 'TechnicalSupportQueue'")
                
                self.num_customer.num_customer_in_tech_dept_queue -= 1
                logger.info(f"[Update {self.requestType}] Time {self.env.now}: Number of customer in queue of technical dept is {self.num_customer.num_customer_in_tech_dept_queue}")

                yield self.env.process(self.serve_customer(self.requestType))
            
                
        if (self.requestType == 'SalesBilling'):
            logger.info(f"[Enqueue] Time {self.env.now}: {self.customerID} enqueued in 'SalesBillingQueue'")
            
            self.num_customer.num_customer_in_sale_dept_queue += 1
            self.num_customer.num_customer_in_sale_dept += 1
            
            logger.info(f"[Update {self.requestType}] Time {self.env.now}: Number of customer in queue of sale dept is {self.num_customer.num_customer_in_sale_dept_queue}")
            logger.info(f"[Update {self.requestType}] Time {self.env.now}: Number of customer in sale dept is {self.num_customer.num_customer_in_sale_dept}")


            with self.agents_sales.request() as request:
                yield request
                logger.info(f"[Dequeue] Time {self.env.now}: {self.customerID} dequeued from 'SalesBillingQueue'")
                
                self.num_customer.num_customer_in_sale_dept_queue -= 1
                logger.info(f"[Update {self.requestType}] Time {self.env.now}: Number of customer in queue of sale dept is {self.num_customer.num_customer_in_sale_dept_queue}")

                yield self.env.process(self.serve_customer(self.requestType))
        
                
        logger.info(f"[Leave system] Time {self.env.now}: {self.customerID} leaves the system")


# Main simulation function
def main(i):
    global logger
    log_path = f'log_tc1/local_{i}.log'
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open('log_tc1/local_{}.log'.format(i),'w') as file:
        pass
        
    logger = configure_logger(log_path)
    

    random.seed(42)
    env = simpy.Environment()

    arrival_rate = i
    service_rate_router = 30
    service_rate_dept = 4
    

    # Create number of customer in router
    num_customer_router = numberCustomer() 
    # Create ArrivalEvent
    generator = CustomerGenerator(env, arrival_rate, service_rate_router, service_rate_dept, num_customer_router)
    
    env.run(until=3000)

# Run the simulation
if __name__ == '__main__':
    # main(20)
    
    for i in range (1,31):
        main(i) 
        print("Done log " + str(i))