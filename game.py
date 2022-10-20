# Simple pygame program

# Import and initialize the pygame library
import pygame
from time import sleep
import random
import gc

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

    def __init__(self, speed, lane=1):
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

        self.y = (SCREEN_HEIGHT * 3)//2
        self.rect.center = (self.x, self.y)
        while(any(car.rect.colliderect(self.rect) for car in Car.cars)):
            self.y = self.y + 20
            self.rect.center = (self.x, self.y)

        self.surf.fill((get_random_int(0,255),get_random_int(0,255),get_random_int(0,255)))
        self.initial_speed = speed
        self.speed = speed
        self.speed_game = self.speed * 5 / 200






        self.id = Car.id
        Car.id += 1
        Car.cars.append(self)
        
    def update(self, key):
        pygame.font.init()
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        font2 = pygame.font.SysFont('Comic Sans MS', 15)
        car_ahead = self.get_nearest_car_ahead()
        if (car_ahead and self.speed > car_ahead.speed):
            self.speed = car_ahead.speed
            speed = self.get_nearest_car_ahead().speed_game
            self.surf.fill((255, 0, 0))
            self.surf.blit(myfont.render(str(self.get_nearest_car_ahead().id), True, (0, 0, 0)), (20, 20))
            ##write in surface

        else :
            speed = self.speed_game
            #self.update_speed(self.initial_speed)
            self.speed = self.initial_speed
            self.surf.fill((0, 255, 0))
        self.surf.blit(myfont.render(str(self.id), True, (0, 0, 0)), (0, 0))
        self.surf.blit(font2.render("actual:"+str(self.speed), True, (0, 0, 0)), (0, 30))
        self.surf.blit(font2.render("initial:"+str(self.initial_speed), True, (0, 0, 0)), (0, 40))
        self.surf.blit(myfont.render("y :"+str(self.y), True, (0, 0, 0)), (0, 60))
        if key == K_UP:
            self.rect.move_ip(0, -speed)
        if key == K_DOWN:
            self.rect.move_ip(0, speed)
        if key == K_LEFT:
            self.rect.move_ip(-speed, 0)
        if key == K_RIGHT:
            self.rect.move_ip(speed, 0)
        '''if self.rect.left <)
    
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT'''
        self.y = self.rect.center[1]
    def get_nearest_car_ahead(self):
        if Car.cars_lane[self.lane] and Car.cars_lane[self.lane][-1] != self:
            return Car.cars_lane[self.lane][-1]
    # def update_speed(self, speed):
    #     if not(self.is_blocked):
    #         self.speed = speed
    #     else:
    #         self.speed = self.initial_speed
    #     self.speed_game = self.speed * 5 / 200
    #     self.is_blocked = not(self.is_blocked)

    def __del__(self):
        Car.cars.remove(self)
        Car.cars_lane[self.lane].remove(self)
        #self.car_in_back.car_in_front = None
        

def get_random_int(x,y):
    return random.randint(x,y)

def create_cars(n):
    for i in range(n):
        Car(get_random_int(90,200), get_random_int(1,3))


create_cars(5)


clock=pygame.time.Clock()

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
    if (time%100 == 0):
        create_cars(3)

    
    for car in Car.cars:

        car.update(K_UP)
        screen.blit(car.surf, car.rect)
        if car.rect.bottom <= 0:
            Car.cars.remove(car)
            del(car)
    
        
    # Flip the display
    #screen.blit(player.surf, player.rect)

    pygame.display.flip()
    clock.tick(30)
