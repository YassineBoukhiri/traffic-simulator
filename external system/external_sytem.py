# Simple pygame program

# Import and initialize the pygame library
import pygame
from time import sleep
import random
from datetime import datetime
import json
import requests
import math


# Comment to show the pygame window
# import os
# os.environ["SDL_VIDEODRIVER"] = "dummy"


pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([500, 500])

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
# Initialize pygame
pygame.init()

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)
font2 = pygame.font.SysFont('Comic Sans MS', 15)

# Variable to keep the main loop running
running = True

# Fill the screen with white
screen.fill((255, 255, 255))    

# Create a surface and pass in a tuple containing its length and width
#surf = pygame.Surface((50, 50))

# Give the surface a color to separate it from the background


#cars = []

class Car(pygame.sprite.Sprite):
    id = 1
    cars = []
    cars_lane = {1: [], 2: [], 3: []}

    def __init__(self, speed, lane=1, y=(SCREEN_HEIGHT)):
        super(Car, self).__init__()
        self.surf = pygame.Surface((75, 100))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.lane = lane
        if (lane == 1):
            self.x = SCREEN_WIDTH/3 *2 + SCREEN_WIDTH/3/2
            Car.cars_lane[1].append(self)
        elif (lane == 2):
            self.x = SCREEN_WIDTH/3 + SCREEN_WIDTH/3/2
            Car.cars_lane[2].append(self)
        elif (lane == 3):
            self.x = SCREEN_WIDTH/3/2
            Car.cars_lane[3].append(self)
        self.y = y
        if (Car.cars_lane[self.lane]):
            self.y = max([car.y for car in Car.cars_lane[self.lane]]) + 200
        self.rect.center = (self.x, self.y)
        # while(any(car.rect.colliderect(self.rect) for car in Car.cars_lane[self.lane])):
        #     self.y = self.y + 100
        #     self.rect.center = (self.x, self.y)
        self.rect.center = (self.x, self.y)
        self.surf.fill((get_random_int(0,255),get_random_int(0,255),get_random_int(0,255)))
        self.initial_speed = speed
        self.speed = speed
        self.speed_game = self.speed * 5 / 200



        self.surf.blit(myfont.render(str(self.id), True, (0, 0, 0)), (20, 20))
        ahead = self.get_nearest_car_ahead()
        if ahead: 
             
            self.surf.blit(font2.render(str(ahead.id), True, (0, 0, 0)), (40, 20))

        self.is_over_taking = False
        self.is_half_over_taking_done = False
        self.is_shutdown = False
        


        self.id = Car.id
        Car.id += 1
        Car.cars.append(self)
        
    def update(self, key):
        if (self.is_shutdown):
            return
        car_ahead = self.get_nearest_car_ahead()
        if (car_ahead):
            if (self.speed > car_ahead.speed and abs(self.y - car_ahead.y) < 150):
                if (car_ahead.is_over_taking):
                    self.update_speed(car_ahead.speed*0.65)
                else :
                    self.update_speed(car_ahead.speed)
                self.surf.fill((255, 0, 0))
        else :
            speed = self.update_speed(self.initial_speed)
            #self.update_speed(self.initial_speed)
            self.surf.fill((0, 255, 0))
        self.surf.blit(font2.render("acl "+str(self.speed), True, (0, 0, 0)), (20, 60))
        self.surf.blit(font2.render("ini "+str(self.initial_speed), True, (0, 0, 0)), (20, 70))
        speed = self.speed_game
        if key == K_UP:
            self.rect.move_ip(0, -speed)
        if key == K_DOWN:
            self.rect.move_ip(0, speed)
        if key == K_LEFT:
            if (self.can_over_take() and not(self.is_over_taking)):
                print("XXXXXXXXXXXXXXXXX OVER TAKING XXXXXXXXXXXXXXXXXXXXXXX")
                self.is_over_taking = True
        if key == K_RIGHT:
            self.rect.move_ip(speed, 0)
        self.y = self.rect.center[1]


    def update_over_taking(self) : 
        if (self.is_shutdown):
            return
        pygame.draw.line(screen, (255, 0, 0), (self.x, self.y), (self.x - SCREEN_WIDTH/3, self.y - SCREEN_WIDTH/3), 1)
        speed = self.speed_game
        print("x", self.x)
        if (self.is_over_taking):
            print("I am ",self.id," over taking and screen width is ", SCREEN_WIDTH//3)
            self.rect.move_ip(-math.sin(math.radians(45))*speed, -math.cos(math.radians(45))*speed)
            self.y = self.rect.center[1]
            self.x = self.rect.center[0]
            L = SCREEN_WIDTH//3
            #if (self.x == SCREEN_WIDTH//3 or self.x == SCREEN_WIDTH//3*2):
            if ((0.95*L < self.x < 1.05*L or 0.95*L*2 < self.x < 1.05*L*2) and not(self.is_half_over_taking_done)):
                self.is_half_over_taking_done = True
                self.surf.fill((255, 255, 255))
                print(self.lane)
                Car.cars_lane[self.lane].remove(self)
                self.lane = self.lane + 1
                print(self.lane)
                Car.cars_lane[self.lane].append(self)
            d1, d2 = SCREEN_WIDTH//3 + SCREEN_WIDTH//3//2,  SCREEN_WIDTH//3//2
            #if (0.95*d1 <= self.x <= 1.05*d1 or 0.95*d2 <= self.x <= 1.05*d2):
            if (0.95*d1<self.x<1.05*d1 or 0.95*d2 < self.x < 1.05*d2 and self.is_half_over_taking_done):
                print("YYYYYYYYYYYYYYYYYYYYY ENDED OVER TAKING YYYYYYYYYYYYYYYYYYYYY")
                self.is_over_taking = False

    def get_nearest_car_ahead(self):
        cars_ahead = [car for car in Car.cars_lane[self.lane] if car.y < self.y]
        if cars_ahead:
            return max(cars_ahead, key=lambda car: car.y)
        else:
            return None
    def update_speed(self, speed):
        self.speed = speed
        self.speed_game = self.speed * 5 / 200
    
    def remove(self):
        Car.cars.remove(self)
        Car.cars_lane[self.lane].remove(self)

    def can_over_take(self):
        if (self.lane==3):
            return False
        d = SCREEN_WIDTH/3 / math.cos(math.radians(45))
        for car in Car.cars_lane[self.lane+1]:
            d_car = abs(car.y - self.y) + SCREEN_WIDTH/3 * math.tan(math.radians(45))
            if (self.speed ==0 or car.speed == 0):
                return False
            if (d_car / car.speed < d / self.speed):
                return False
        return True        

    def go_forward(self):
        self.update(K_UP) 

    def over_take(self):
        self.update(K_LEFT)

        

def get_random_int(x,y):
    return random.randint(x,y)

def create_cars(n):
    for i in range(n):
        lane = get_random_int(1,3)
        if (lane == 1):
            Car(get_random_int(90,120), lane)
        elif (lane == 2):
            if (get_random_int(0,1)):
                Car(get_random_int(90,120), lane)
            else : 
                Car(get_random_int(120,132), lane)
        elif (lane == 3):
            if (get_random_int(0,1)):
                Car(get_random_int(120,132), lane)
            else : 
                Car(get_random_int(132,150), lane)

def detect_accident():
    for car in Car.cars:
        for car2 in Car.cars:
            if (car != car2):
                if (car.rect.colliderect(car2.rect)):
                    print("accident")
                    print(car.id)
                    print(car2.id)
                    img = pygame.image.load('explosion.png')
                    img = pygame.transform.scale(img, (100, 100))
                    #center of collision
                    x = (car.rect.center[0] + car2.rect.center[0])/2
                    y = (car.rect.center[1] + car2.rect.center[1])/2
                    screen.blit(img, (x, y))


                    car.is_shutdown = True
                    car2.is_shutdown = True
                    car.speed = 0
                    car2.speed = 0
                    return True
    return False

def remove_accident_cars():
    for car in Car.cars:
        for car2 in Car.cars:
            if (car != car2):
                if (car.rect.colliderect(car2.rect)):
                    car.remove()
                    car2.remove()
                    return True
       


# create_cars(5)


clock=pygame.time.Clock()




def get_payload():
    ts = datetime.now()
    payload = {
        "way 1": {
            "cars": []
        },
        "timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
        "camera_id": 122
    }
    for car in Car.cars:
        if 0 < car.rect.bottom < SCREEN_HEIGHT:
            payload["way 1"]["cars"].append({
                "id": car.id,
                "speed": car.speed,
                "lane": car.lane
            })
    return payload

Car(150,2)
#Car(100,2)
# Car(150,3)
# Car(120,2)
# Car(120,3)
# Car(132,1)
# Car(132,3)



# Main loop
time = 0

while running:
    # Look at every event in the queue
    for event in pygame.event.get():
        #screen.blit(player.surf, player.rect)
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False

            elif event.key == K_LEFT:
                remove_accident_cars()
                

        # Did the user click the window close button? If so, stop the loop.
        elif event.type == QUIT:
            running = False
        
    
    # Drawing the map
    screen.fill((0, 0, 0))
    surf = pygame.Surface((30, 70))
    surf.fill((255, 255, 255))
    for i in range(10) : 
        screen.blit(surf, (SCREEN_WIDTH/3, i*100))
        screen.blit(surf, (SCREEN_WIDTH/3*2, i*100))

    sleep(0.01)
    time += 1
    # if (time%100 == 0):
    #     create_cars(3)
        
    
    # if (time%20 == 0):
    #     for car in Car.cars:
    #         if (get_random_int(0,1)):
    #             print("over taking")
    #             car.over_take()

    for car in Car.cars:
        car.over_take()


    #if (time%100 == 0):
    #    requests.post("http://localhost:8001/traffic", json=get_payload())

    
    for car in Car.cars:


        if (car.can_over_take()):
            car.surf.fill((255, 255, 0))
        
        car.go_forward()

        # elif car.id == 2:
        #     car.update(K_LEFT)
        screen.blit(car.surf, car.rect)
        if car.rect.bottom <= 0:
            car.remove()
        car.update_over_taking()

    detect_accident()

    pygame.display.flip()
    clock.tick(30)
