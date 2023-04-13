import pygame
import numpy as np
from Boid import Boid
from Obstacle import Obstacle
import random
import sys

pygame.init()

size = width, height = 1000, 1000


maxVelocity= 2 
numBoids = 5
boids = []
obstacles = []

screen = pygame.display.set_mode(size)



# create boids at random positions
for i in range(numBoids):
    boids.append(Boid(random.randint(0, width), random.randint(0, height)))
    #boids.append(Boid(100,100))   

paused = False

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        elif event.type ==  pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                new_obstacle = Obstacle(np.array(pygame.mouse.get_pos()))
                obstacles.append(new_obstacle)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused


    if not paused:

        #Compare each boid to eevry other boid
        for boid in boids:
            closeBoids = []
            for otherBoid in boids:
                if otherBoid == boid: continue
                distance = boid.distance(otherBoid)
                if distance < 200:
                    closeBoids.append(otherBoid)

            #4 behaviours to be considered
            boid.avoid_obstacles(obstacles, 100)  
            boid.cohesion(closeBoids)
            boid.allignment(closeBoids)
            boid.seperation(closeBoids, 50)
            

            # ensure they stay within the screen space
            border = 10
            #If at left border and  moving left
            if boid.pos[0] < border and boid.vel[0] < 0:
                boid.vel[0] = -boid.vel[0] * random.random()
            #if at right border and moving right
            if boid.pos[0] > width - border and boid.vel[0] > 0:
                boid.vel[0] = -boid.vel[0] * random.random()
            #if at top border and moving up
            if boid.pos[1] < border and boid.vel[1] < 0:
                boid.vel[1] = -boid.vel[1] * random.random()
            #if at bottom border and moving down
            if boid.pos[1] > height - border and boid.vel[1] > 0:
                boid.vel[1] = -boid.vel[1] * random.random()

            boid.move()

        screen.fill([135, 206, 235])
        #Drawing the boids
        for boid in boids:
            boidRect = pygame.Rect(boid.image.get_rect())
            boidRect.x = boid.pos[0]
            boidRect.y = boid.pos[1]
            screen.blit(boid.image, boidRect)

        #draw obstacles
        for obstacle in obstacles:
            obstacle.draw(screen)
        pygame.display.flip()

        pygame.time.delay(50)