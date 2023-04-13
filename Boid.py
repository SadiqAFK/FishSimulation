import pygame
import numpy as np
import random

maxVelocity = 2

class Boid:
    def __init__(self, x, y):

        self.pos = np.array([x,y])
        self.vel = [random.randint(1, 10) , random.randint(1, 10)]
        #self.vel = [2,2]
        self.image = pygame.image.load("boid_circle.png")
        self.original_image = pygame.image.load("boid_circle.png")




    def rotate(self):

        #Calculate the direction fo movement from velocity
        angle = np.degrees(np.arctan2(self.vel[1], self.vel[0]))

        # Rotate the image by the calculated angle
        self.image = pygame.transform.rotate(self.original_image, angle)
        print("Angle: ", angle)

  
        

    def distance(self, boid):
        return np.linalg.norm((self.pos - boid.pos))

    def move(self):
        print("Pos: ", self.pos)
        print("Vel: ",  self.vel)
        if abs(self.vel[0]) > maxVelocity:
            self.vel[0] = maxVelocity/self.vel[0]
        
        if abs(self.vel[1]) > maxVelocity:
            self.vel[1] = maxVelocity/self.vel[1]
        
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        #self.rotate()

    def avoid_obstacles(self, obstacles, min_distance):
        for obstacle in obstacles:
            dist_vec = self.pos - obstacle.pos
            distance = np.linalg.norm(dist_vec)

            if distance < min_distance:
                # calculate a force vector away from the obstacle
                force = dist_vec / distance**2

                # apply the force to the boid's velocity
                self.vel += force

                # limit the magnitude of the boid's velocity to max_speed
                max_speed = 5
                speed = np.linalg.norm(self.vel)
                if speed > max_speed:
                    self.vel *= max_speed / speed


    def seperation(self, boids, minDistance):

        #Check if there are multiple boids or not
        if len(boids) < 1: 
            return

        distanceX = 0
        distanceY = 0
        numClose = 0

        for boid in boids:

            distance = self.distance(boid)
            if  distance < minDistance:
                numClose += 1
                xdiff = (self.pos[0] - boid.pos[0])
                ydiff = (self.pos[1] - boid.pos[1]) 

                if xdiff >= 0:
                    xdiff = np.sqrt(minDistance) - xdiff
                elif xdiff < 0:
                    xdiff = -np.sqrt(minDistance) - xdiff

                if ydiff >= 0: 
                    ydiff = np.sqrt(minDistance) - ydiff
                elif ydiff < 0: 
                    ydiff = -np.sqrt(minDistance) - ydiff

                distanceX += xdiff
                distanceY += ydiff 

        if numClose == 0:
            return

        self.vel[0] -= distanceX / 5
        self.vel[1] -= distanceY / 5

    def cohesion(self, boids):
        if len(boids) < 1: return

        # calculate the average distances from the other boids
        avgX = 0
        avgY = 0
        for boid in boids:
            if boid.pos[0] == self.pos[0] and boid.pos[1] == self.pos[1]:
                continue

            avgX += (self.pos[0] - boid.pos[0])
            avgY += (self.pos[1] - boid.pos[1])

        avgX /= len(boids)
        avgY /= len(boids)

        # set our velocity towards the others
        distance = np.sqrt((avgX * avgX) + (avgY * avgY)) * -1.0

        self.vel[0] -= (avgX / 100)
        self.vel[1] -= (avgY / 100)    


    def allignment(self, boids):
        if len(boids) < 1: return
        # calculate the average velocities of the other boids
        avgX = 0
        avgY = 0

        for boid in boids:
            avgX += boid.vel[0]
            avgY += boid.vel[1]

        avgX /= len(boids)
        avgY /= len(boids)

        # set our velocity towards the others
        self.vel[0] += (avgX / 40)
        self.vel[1] += (avgY / 40)