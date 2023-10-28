import numpy as np

D = {
    'red1': [[180, 255, 255], [159, 50, 70]], 
    'red2': [[9, 255, 255], [0, 50, 70]], 
    'green': [[89, 255, 255], [36, 50, 70]], 
    'blue': [[128, 255, 255], [90, 50, 70]], 
    'yellow': [[35, 255, 255], [25, 50, 70]], 
    'orange': [[24, 255, 255], [10, 50, 70]], 
    'purple': [[158, 255, 255], [129, 50, 70]],
    'brown': [[10, 100, 20], [20, 255, 200]],
    'gray': [[180, 18, 230], [0, 0, 40]],
    'black': [[180, 255, 30], [0, 0, 0]], 
    'white': [[180, 18, 255], [0, 0, 231]], 
     
}

def generate_random_number_within_range(mu, sigma, lower_bound, upper_bound):
    while True:
        random_number = np.random.normal(mu, sigma)
        if lower_bound <= random_number <= upper_bound:
            return random_number
        
for i in range(20):
    x = np.random.randint(120, 122)
    print(x)