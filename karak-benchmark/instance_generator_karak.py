#Author: Anderson Zudio 
#Target: Python 3.8.5
#This tool will generate instances based on "The hybrid vehicle-drone routing problem for pick-up and delivery services" specification of Karak & Abdelghany.
#All floating point numbers writen with this tool only uses 1 decimal digit

#The article specify those important characteristics about the instances:
## Every instance is a square grid where the main unit is square miles
## Every instance is symmetric
## For every instance, the delivery/pickup up load of any customer is less than the drone capacity
## The distance between two stations DO NOT surpasses the drone's maximum flight range (does it now?)
## The above rule has been modified: for each client, there's at least one drone (based on highest range) that can visit it and go back to the station where it departed.

## Karak's variable parameters are: 
### A letter that describes the grid type
### Number of instances to generate with the stablished setup
### The grid dimension (square)
### Number of customers

## Karak's other parameters are: 
### Number of stations (excluding depot): ({SIZE}/5 + 1)^2 - 1
### Fixed number of drones: 2
### Drone homogeneous setup: (7 maximum range, 10 maximum capacity)
### Clients have delivery/pickup restriction in the range of [0.0 to 5.0]
### Stations are placed at grid intersections spaced of 5 miles [Ie coordinates (0,5), (5,0), (5,5), (5,10), (10,5), (10,10), and so on]
### The depot is fixed at coordinate (0,0)
### Vehicle operation cost of 1.0
### Drone operation cost of 2.0
### All arcs exist, the cost is the euclidean distance itself

##  Karak's default setup is as follows:
### GRID NAME (DIMENSION) // CUSTOMERS
### Grid A1 to A5 (5x5) // 6 
### Grid A6 to A10 (5x5) // 8
### Grid B1 to B10 (10x10) // 50
### Grid C1 to C10 (15x15) // 50
### Grid D1 to D10 (20x20) // 50
### Grid E1 to E10 (10x10) // 100
### Grid F1 to F10 (15x15) // 100
### Grid G1 to G10 (20x20) // 100
### If you want to follow this setup, you should use this script with the parameters writen above

#Every instance is generated based on the specification of input_format_hvdrp.md
#They're all symmetric

#Usage: python3 instance_generator_karak.py {NETWORK_LETTER_ID} {FIRST_INSTANCE_NUMBER} {LAST_INSTANCE_NUMBER} {SIZE} {N_CUSTOMERS}  
#Standard Input:  Nothing
#Stardard Output: Console information about each instance writen
#File output: {path_to_karak_benchmark}/{NETWORK_LETTER_ID}-{INSTANCE_NUMBER}.hvdrp.json
#Examples: 
##To generate the A network as describe above do (A1 to A5 with 6 customers) use:
##python3 instance_generator_karak.py A 1 5 5 6
##Then finish with the following (A6 to A10 with 8 customers):
##python3 instance_generator_karak.py A 6 10 5 8
##To generate the F network as describe above do (F1 to F10 with 100 customers)
##python3 instance_generator_karak.py F 1 10 15 100

import os
import sys
import math
import random
import json

#Globals
base_instance_dir = "" #Point this to your project instance directory.
karak_benchmark_dir = base_instance_dir + "karak_benchmark/";

#Will generate a json with the instance. 
class KarakGenerator:
    #Fixed parameters given by Karak
    n_drone = 2
    drone_maximum_range = 7.0
    drone_maximum_load = 10.0
    drone_operation_cost = 2.0
    vehicle_operation_cost = 1.0
    depot_coordinate = [0, 0] #stays at the botton left corner of the grid
    client_delivery = [0.0, 5.0] #will be reandonly chosen in this range
    client_pickup = [0.0, 5.0] #will be randonly chosen in this range
    distance_between_station = 5.0 #stations are located in the grid intersections. These intersection are spaced following this param
    drone_specification = []
    drone_highest_range = 0.0 #denotes the highest range drone. It is used to guarantee that each client is reacheable from at least one station

    def __init__(self):
        #filling the fixed parameters
        for i in range(self.n_drone): 
            drone = { "id": i, "range": self.drone_maximum_range, "weight": self.drone_maximum_load, "cost": self.drone_operation_cost}
            self.drone_specification.append(drone)
        self.drone_highest_range = self.drone_maximum_range

    #will return the dict of stationCoordinates given the grid_size
    def stationCoordinates(self, grid_size):
        station_coordinates = []
        n_stations = int((grid_size/5 +1)*(grid_size/5 +1) - 1) #calculating how many stations based on the grid_size
        coordinate = [self.depot_coordinate[0] + self.distance_between_station, self.depot_coordinate[1]]
        for i in range(1, n_stations+1):
            station_coordinates.append({"label": i, "x": coordinate[0], "y": coordinate[1]})
            coordinate[0] += self.distance_between_station
            if coordinate[0] > grid_size:
                coordinate[0] = 0.0
                coordinate[1] += self.distance_between_station
        return station_coordinates

    #will return the clients coordinates. Wiill make sure the client is reacheable
    def clientCoordinates(self, n_customer, station_coordinates):
        client_coordinates = [] #will contain the return value
        used_coordinates = [] #to make sure no two clients has the same coordinate
        for i in range(len(station_coordinates)+1, n_customer+len(station_coordinates)+1):
            found = False
            coordinate = [0, 0] #the actual client coordinate
            while not found: #will stop iterating once a client with unique coordinates has been found. Also, the client must be recheable with the highest range drone
                coordinate[0] = round(random.uniform(0.0, float(grid_size)), 1)
                coordinate[1] = round(random.uniform(0.0, float(grid_size)), 1)
                found = True
                for coord in used_coordinates: #checking if the actual client will have the same coordinate as other
                    if coordinate == coord:
                        found = False
                        break
                if found: #checking if the client is reacheable from some station with the highest range drone
                    found = False
                    for station_coordinate in station_coordinates:
                        x = station_coordinate["x"]
                        y = station_coordinate["y"]
                        dist = math.sqrt((coordinate[0] - x)**2 + (coordinate[1] - y)**2)
                        if dist <= self.drone_highest_range/2:
                            found = True
                            break

            delivery = round(random.uniform(self.client_delivery[0], self.client_delivery[1]), 1) #client delivery value
            pickup = round(random.uniform(self.client_pickup[0], self.client_pickup[1]), 1) #client pickup value
            used_coordinates.append([coordinate[0], coordinate[1]]) #mark this coordinate as used
            client_coordinates.append({"label": i, "x": coordinate[0], "y": coordinate[1], "delivery": delivery, "pickup": pickup})            
        return client_coordinates

    #networkd_id is the instance letter. 
    #number is the instance number.
    #the instance name will be {NETWORK_LETTER_ID}-{NUMBER}
    #grid_size should be the size of the square grid
    #n_customer will dictate how many clients this instance will have. 
    def generate(self, network_id, number, grid_size, n_customer):
        instance_name = network_id.upper() + '-' + str(number)
        station_coordinates = self.stationCoordinates(grid_size)
        client_coordinates = self.clientCoordinates(n_customer, station_coordinates)
        
        #setting up the json based on the input_format located at the /doc/ folder
        instance_dict = { 
            "name": instance_name,
            "symmetric": {
                "droneSpecification": self.drone_specification,
                "vehicleCost": self.vehicle_operation_cost,
                "depotCoordinates": { "x": self.depot_coordinate[0], "y": self.depot_coordinate[1] },
                "stationCoordinates": station_coordinates,
                "clientCoordinates": client_coordinates
            }
        }
        return instance_dict

#Reading the parameters
network_id = sys.argv[1]
first_instance = int(sys.argv[2])
last_instance = int(sys.argv[3])
grid_size = int(sys.argv[4])
n_customer = int(sys.argv[5])
print("Generating network " + network_id + " from " + str(first_instance) + " to " + str(last_instance) + " with grid size " + str(grid_size) + " and " + str(n_customer) + " customers")
karak_generator = KarakGenerator()

#creating the directory
if not os.path.exists(karak_benchmark_dir):
    print("Creating the follwing directory: " + karak_benchmark_dir)
    os.mkdir(karak_benchmark_dir)

#generating each instance
for i in range(first_instance, last_instance+1):
    print("Generation of instance "  + str(i))
    file = open(karak_benchmark_dir + network_id.upper() + '-' + str(i) + '.hvdrp.json', "w")
    instance = karak_generator.generate(network_id, i, grid_size, n_customer)
    
    print("Writing instance " + instance["name"])
    file.write(json.dumps(instance, indent = 4))
    
    print("Closing file")
    file.close()
print("All instances done")