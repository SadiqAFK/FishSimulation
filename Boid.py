import pygame
import numpy as np
import random

maxVelocity = 2

class Boid:

    #Initialize the boid position
    #Velocty is randomly assigned
    def __init__(self, x, y):

        self.pos = np.array([x,y])
        self.vel = [random.randint(1, 10) , random.randint(1, 10)]
        #self.vel = [2,2]
        self.image = pygame.image.load("boid_circle.png")
        self.original_image = pygame.image.load("boid_circle.png")

        self.seperation_factor = 5
        self.cohesion_factor = 100
        self.allignment_factor = 40



    #Function used to rotate iamge based on velocity vector
    def rotate(self):

        #Calculate the direction fo movement from velocity
        angle = np.degrees(np.arctan2(self.vel[1], self.vel[0]))

        # Rotate the image by the calculated angle
        self.image = pygame.transform.rotate(self.original_image, angle)
        print("Angle: ", angle)

  
        
    #Reutrn distance between boids
    def distance(self, boid):
        return np.linalg.norm((self.pos - boid.pos))


    #Acts as update funciton for Boid
    def move(self):
        print("Pos: ", self.pos)
        print("Vel: ",  self.vel)

        #Ensure boid is moving at safe speed
        if abs(self.vel[0]) > maxVelocity:
            self.vel[0] = maxVelocity/self.vel[0]
        
        if abs(self.vel[1]) > maxVelocity:
            self.vel[1] = maxVelocity/self.vel[1]
        
        #update position
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        #self.rotate()



    def avoid_obstacles(self, obstacles, min_distance):
        for obstacle in obstacles:

            #distance and vector between boid and obstacle
            dist_vec = self.pos - obstacle.pos
            distance = np.linalg.norm(dist_vec)

            #if the boid is within range of the obstacle
            if distance < min_distance:

                # calculate a force vector away from the obstacle
                force = dist_vec / distance**2

                # apply the force to the boid's velocity
                self.vel += force

                # limit the magnitude of the boid's velocity to maxVelocity
                speed = np.linalg.norm(self.vel)
                if speed > maxVelocity:
                    self.vel *= maxVelocity / speed


    def seperation(self, boids, minDistance):

        #Check if there are multiple boids or not
        if len(boids) < 1: 
            return

        distanceX = 0
        distanceY = 0
        numClose = 0

        for boid in boids:

            distance = self.distance(boid)

            #Check if boids are too close together
            if  distance < minDistance:
                numClose += 1

                #Check how far away boid is in each direction
                xdiff = (self.pos[0] - boid.pos[0])
                ydiff = (self.pos[1] - boid.pos[1]) 

                #boid is to the elft of self
                if xdiff >= 0:
                    xdiff = np.sqrt(minDistance) - xdiff
                #boid is to right of self
                elif xdiff < 0:
                    xdiff = -np.sqrt(minDistance) - xdiff

                #boid is under self
                if ydiff >= 0: 
                    ydiff = np.sqrt(minDistance) - ydiff
                #boid is over self
                elif ydiff < 0: 
                    ydiff = -np.sqrt(minDistance) - ydiff

                distanceX += xdiff
                distanceY += ydiff 

        if numClose == 0:
            return

        #5 is the factor for seperation, can be modififed for different behaviour
        self.vel[0] -= distanceX / self.seperation_factor
        self.vel[1] -= distanceY / self.seperation_factor

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

        # set our velocity towards the average
        distance = np.sqrt((avgX * avgX) + (avgY * avgY)) * -1.0

        #100 is cohesion factor which can be modified
        self.vel[0] -= (avgX / self.cohesion_factor)
        self.vel[1] -= (avgY / self.cohesion_factor)    


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
        self.vel[0] += (avgX / self.allignment_factor)
        self.vel[1] += (avgY / self.allignment_factor)