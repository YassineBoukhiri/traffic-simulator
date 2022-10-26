from model import Model
import json 
from enum import Enum

class Density(Enum):
    VERY_LOW = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    VERY_HIGH = 4


"""
{'way 1': {'cars': [{'id': 39, 'speed': 90, 'lane': 2}, {'id': 40, 'speed': 115, 'lane': 2}, {'id': 41, 'speed': 102, 'lane': 1}, {'id': 43, 'speed': 115, 'lane': 2}, {'id': 44, 'speed': 96, 'lane': 1}, {'id': 45, 'speed': 115, 'lane': 2}, {'id': 49, 'speed': 106, 'lane': 1}, {'id': 57, 'speed': 121, 'lane': 3}, {'id': 58, 'speed': 148, 'lane': 3}, {'id': 61, 'speed': 120, 'lane': 3}]}, 'timestamp': '2022-10-25 10:28:33', 'camera_id': 122}
"""


input_data = Model(**json.loads('{"way 1": {"cars": [{"id": 39, "speed": 90, "lane": 2}, {"id": 40, "speed": 115, "lane": 2}, {"id": 41, "speed": 102, "lane": 1}, {"id": 43, "speed": 115, "lane": 2}, {"id": 44, "speed": 96, "lane": 1}, {"id": 45, "speed": 115, "lane": 2}, {"id": 49, "speed": 106, "lane": 1}, {"id": 57, "speed": 121, "lane": 3}, {"id": 58, "speed": 148, "lane": 3}, {"id": 61, "speed": 120, "lane": 3}]}, "timestamp": "2022-10-25 10:28:33", "camera_id": 122}'))

number_lanes = 3
max_speed = 130

def get_average_speed_per_lane(input_data: Model) -> dict:
    """
    :param input_data: input data
    :return: average speed per lane
    """
    average_speed_per_lane = {k: [] for k in range(1, number_lanes + 1)}
    for car in input_data.way_1.cars:
        average_speed_per_lane[car.lane].append(car.speed)
    for lane in average_speed_per_lane:
        average_speed_per_lane[lane] = sum(average_speed_per_lane[lane]) / len(average_speed_per_lane[lane]) if len(average_speed_per_lane[lane]) > 0 else 0
    return average_speed_per_lane

def get_number_of_vehicules_per_lane(input_data: Model) -> dict:
    """
    :param input_data: input data
    :return: number of vehicules per lane
    """
    number_of_vehicules_per_lane = {k: 0 for k in range(1, number_lanes + 1)}
    for car in input_data.way_1.cars:
        number_of_vehicules_per_lane[car.lane] += 1
    return number_of_vehicules_per_lane

def get_traffic_density(input_data: Model) -> Density:
    """
    :param input_data: input data
    :return: traffic density per lane
    """
    average_speed_per_lane = get_average_speed_per_lane(input_data)
    number_of_vehicules_per_lane = get_number_of_vehicules_per_lane(input_data)
    speed_average = sum(average_speed_per_lane.values()) / len(average_speed_per_lane) if len(average_speed_per_lane) > 0 else 0
    print(speed_average)
    if (list(number_of_vehicules_per_lane.values()).count(0)) :
        return Density.VERY_LOW
    elif 0.9 * max_speed < speed_average  < 1.2 * max_speed:
        return Density.LOW
    elif 0.7 * max_speed < speed_average  < 0.9 * max_speed:    
        return Density.MEDIUM
    elif 0.5 * max_speed < speed_average  < 0.7 * max_speed:
        return Density.HIGH
    else:
        return Density.VERY_HIGH

print(get_average_speed_per_lane(input_data))
print(get_number_of_vehicules_per_lane(input_data))
print(get_traffic_density(input_data))