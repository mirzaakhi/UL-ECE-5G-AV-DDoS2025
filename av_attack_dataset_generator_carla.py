"""
Simulation script for generating AV DDoS dataset using CARLA.
Generates 5000 samples with 14 features.
Output: regenerated_raw_av_DDoSattack_dataset.csv
"""
# Import Libraries
import time
import random
random.seed(42)
import csv
import math
import os
import sys

# If the CARLA module is not accessible, make sure to add its .egg file path to PYTHONPATH
# Example (uncomment and update as needed):
# sys.path.append('/path/to/carla-0.9.14-py3.7-win-amd64.egg')


import carla
print("CARLA module imported successfully!")

# Connect to CARLA Simulator
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)
world = client.get_world()

# Load world and get blueprint library
blueprint_library = world.get_blueprint_library()

# Vehicle
vehicle_bp = blueprint_library.filter('model3')[0]
spawn_points = world.get_map().get_spawn_points()
vehicle = world.try_spawn_actor(vehicle_bp, random.choice(spawn_points))

# Attach GPS sensor
gps_bp = blueprint_library.find('sensor.other.gnss')
gps_transform = carla.Transform(carla.Location(x=0, y=0, z=2))
gps_sensor = world.spawn_actor(gps_bp, gps_transform, attach_to=vehicle)

# Attach IMU sensor for speed and acceleration
imu_bp = blueprint_library.find('sensor.other.imu')
imu_transform = carla.Transform(carla.Location(x=0, y=0, z=2))
imu_sensor = world.spawn_actor(imu_bp, imu_transform, attach_to=vehicle)

# Create CSV file 
csv_file = open("regenerated_raw_av_DDoSattack_dataset.csv", "w", newline="")
csv_writer = csv.writer(csv_file)
csv_writer.writerow([
    "Timestamp", "Latitude", "Longitude", "Speed", "Acceleration",
    "Throttle", "Steering", "Brake",
    "Network_Latency", "Packet_Loss", "Throughput", "Jitter", "Bandwidth_Utilization",
    "Attack_Type"
])



# Attack parameters
attack_types = ["Normal", "DoS_Attack", "Hijacked"]
gps_attack_active = False
control_attack_active = False
speed = 0
acceleration = 0
latitude = 0
longitude = 0

def gps_callback(data):
    global gps_attack_active, latitude, longitude
    latitude, longitude = data.latitude, data.longitude

    if gps_attack_active:
        latitude += random.uniform(-0.0005, 0.0005)
        longitude += random.uniform(-0.0005, 0.0005)

gps_sensor.listen(lambda data: gps_callback(data))

def imu_callback(data):
    global acceleration
    acceleration = math.sqrt(data.accelerometer.x**2 + data.accelerometer.y**2)

imu_sensor.listen(lambda data: imu_callback(data))

# Network metric simulator
def simulate_network_metrics(attack_type):
    if attack_type == "DoS_Attack":
        latency = random.uniform(100, 300)              # ms
        packet_loss = random.uniform(5, 20)             # %
        throughput = random.uniform(0.5, 2.0)           # Mbps
        jitter = random.uniform(10, 50)                 # ms
        bandwidth_util = random.uniform(80, 100)        # %
    elif attack_type == "Hijacked":
        latency = random.uniform(70, 200)
        packet_loss = random.uniform(2, 10)
        throughput = random.uniform(1.0, 5.0)
        jitter = random.uniform(5, 25)
        bandwidth_util = random.uniform(60, 90)
    else:
        latency = random.uniform(20, 60)
        packet_loss = random.uniform(0, 1)
        throughput = random.uniform(5.0, 10.0)
        jitter = random.uniform(1, 5)
        bandwidth_util = random.uniform(20, 50)
    return latency, packet_loss, throughput, jitter, bandwidth_util

try:
    for i in range(5000):
        control = vehicle.get_control()
        velocity = vehicle.get_velocity()
        speed = math.sqrt(velocity.x**2 + velocity.y**2)

        # Random attack choice
        attack = random.choice(attack_types)
        if attack == "DoS_Attack":
            gps_attack_active = True 
        elif attack == "Hijacked":
            control.steer = random.uniform(-1, 1)
            control.throttle = random.uniform(0, 1)
            control.brake = random.uniform(0, 0.5)
            control_attack_active = True
        else:
            gps_attack_active = False
            control_attack_active = False

        # Apply control
        vehicle.apply_control(control)

        # Simulate network metrics
        net_latency, pkt_loss, throughput, jitter, bw_util = simulate_network_metrics(attack)

        # Log all data
        csv_writer.writerow([
            time.time(), latitude, longitude, speed, acceleration,
            control.throttle, control.steer, control.brake,
            net_latency, pkt_loss, throughput, jitter, bw_util, attack
        ])

        time.sleep(0.1)

finally:
    csv_file.close()
    gps_sensor.destroy()
    imu_sensor.destroy()
    vehicle.destroy()
    print("Simulation complete, dataset saved!")
