import random
import gc

class Car:
    id = 1
    def __init__(self, speed):
        self.x = -get_random_int(0,50)
        self.speed = speed
        self.lane = get_random_int(1,3)
        self.id = Car.id
        Car.id += 1

    def move(self):
        if (self.get_nearest_car_ahead()):
            self.x += float(str(round(self.get_nearest_car_ahead().speed/3.6)))
        else :
            self.x += float(str(round(self.speed/3.6, 2)))
        if 0<=self.x<=150 :
            print("Car", self.id, "is in lane", self.lane, "at position", self.x, "with speed", self.speed, "km/h")
            if (self.get_nearest_car_ahead()):
                print("Car", self.id, "is following car", self.get_nearest_car_ahead().id)
            else:
                print("Car", self.id, "is the line",self.lane,"leader")

    def get_nearest_car_ahead(self):
        cars = []
        for obj in gc.get_objects():
            if isinstance(obj, Car) and obj.lane == self.lane and obj.x > self.x:
                cars.append(obj)
        cars_ahead = []
        for car in cars:
            if car.lane == self.lane and car.x > self.x:
                cars_ahead.append(car)
        if(cars_ahead):
            return min(cars_ahead, key=lambda x: x.x)
        
            

    

def get_random_int(x,y):
    return random.randint(x,y)

cars = []
def create_cars(n):
    for i in range(n):
        cars.append(Car(get_random_int(80,120)))

def move_cars():
    for car in cars:
        car.move()
        car.move()
        car.move()
        car.move()
        car.move()

create_cars(10)
move_cars()