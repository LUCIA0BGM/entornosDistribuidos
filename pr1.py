import pygame
import random
import time
from concurrent.futures import ThreadPoolExecutor

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Variables globales
robot_pos = [100, 300]
orders = []
running = True

# FUNCIONES ____________________

def move_robot():
    global robot_pos
    while running:
        if orders:
            order = orders.pop(0)
            print(f"Robot entregando {order}")
            for _ in range(5):
                robot_pos[0] += 10 
                time.sleep(0.5)

def generate_orders():
    while running:
        table = random.randint(1, 10)
        orders.append(f"Pedido mesa {table}")
        print(f"Nuevo pedido para mesa {table}")
        time.sleep(random.randint(2, 5))

# Crear el ThreadPoolExecutor
executor = ThreadPoolExecutor(max_workers=2)
executor.submit(generate_orders)
executor.submit(move_robot)

# BUCLE PRINCIPAL ____________
while running:
    screen.fill((0, 0, 0))

    # Robot
    pygame.draw.circle(screen, (0, 255, 0), robot_pos, 20)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(30)

# Cierre del programa
pygame.quit()
executor.shutdown(wait=False)
