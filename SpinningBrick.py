import os
from math import cos, sin
import pygame
import colorsys

white = (255, 255, 255)
black = (0, 0, 0)
hue = 0

os.environ['SDL_VIDEO_CENTERED'] = '1'
res = width, height = 800, 800
fps = 60

pixelWidth = 20
pixelHeight = 20
xPixel = 0
yPixel = 0

screenWidth = width // pixelWidth
screenHeight = height // pixelHeight
screenSize = screenWidth * screenHeight

A, B = 0, 0

thetaSpacing = 10
phiSpacing = 3

chars = ".,-~:;=!*#$@"

r1 = 10
r2 = 20
k2 = 200
k1 = screenHeight * k2 * 3 / (8 * (r1 + r2))


pygame.init()

screen = pygame.display.set_mode(res)
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 20, bold = True)

def hsv2rgb(h, s, v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))


def text_display(char, x, y):
    text = font.render(str(char), True, hsv2rgb(hue, 1, 1))
    text_rect = text.get_rect(center = (x, y))
    screen.blit(text, text_rect)

k = 0

paused = False
running = True

while running:
    clock.tick(fps)
    pygame.display.set_caption("FPS: {:.2f}".format(clock.get_fps()))

    screen.fill(black)

    output = [' '] * screenSize
    zBuffer = [0] * screenSize

    for theta in range(0, 628, thetaSpacing):
        for phi in range(0, 628, phiSpacing):

            cosA = cos(A)
            sinA = sin(A)
            cosB = cos(B)
            sinB = sin(B)

            cosTheta = cos(theta)
            sinTheta = sin(theta)
            cosPhi = cos(phi)
            sinPhi = sin(phi)

            circleX = r2 + r1 * cosTheta
            circleY = r1 * sinTheta

            x = circleX * (cosB * cosPhi + sinA * sinB * sinPhi) - circleY * cosA * sinB
            y = circleX * (sinB * cosPhi - sinA * cosB * sinPhi) + circleY * cosA * cosB
            z = k2 + cosA * circleX * sinPhi + circleY * sinA
            ooz = 1 / z

            xp = int(screenWidth / 2 + k1 * ooz * x)
            yp = int(screenHeight / 2 - k1 * ooz * y)

            position = xp + screenWidth * yp

            luminance = cosPhi * cosTheta * sinB - cosA * cosTheta * sinPhi - sinA * sinTheta + cosB * (cosA * sinTheta - cosTheta * sinA * sinPhi)

            if ooz > zBuffer[position]:
                zBuffer[position] = ooz
                luminanceIndex = int(luminance * 8)
                output[position] = chars[luminanceIndex if luminanceIndex > 0 else 0]

    for i in range(screenHeight):
        yPixel += pixelHeight
        for j in range(screenWidth):
            xPixel += pixelWidth
            text_display(output[k], xPixel, yPixel)
            k += 1
        xPixel = 0
    yPixel = 0
    k = 0

    A += 0.15
    B += 0.035

    hue += 0.005

    if not paused:
        pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:
                paused = not paused


