import pygame
import random
import time
from concurrent.futures import ThreadPoolExecutor

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Variables globales
robot_pos = [400, 50]  # Empieza en la cocina
robot_target = [400, 50]  # Destino inicial
orders = []
running = True


# CLASES
class Mesa:
    def __init__(self, numero, x, y):
        self.numero = numero
        self.posicion = (x, y)

class Restaurante:
    def __init__(self):
        self.mesas = [
            Mesa(1, 150, 200), Mesa(2, 300, 200),
            Mesa(3, 450, 200), Mesa(4, 600, 200),
            Mesa(5, 150, 400), Mesa(6, 300, 400),
            Mesa(7, 450, 400), Mesa(8, 600, 400)
        ]

    def get_posicion_mesa(self, numero):
        for mesa in self.mesas:
            if mesa.numero == numero:
                return mesa.posicion
        return None  # Si la mesa no existe

restaurante = Restaurante()


# FUNCIONES
def move_robot():
    global robot_target
    while running:
        if orders:
            mesa_numero = orders.pop(0)
            destino = restaurante.get_posicion_mesa(mesa_numero)
            if destino:
                print(f"Robot llevando pedido a la mesa {mesa_numero}")
                robot_target[:] = destino  # Asigna el destino al robot
                while robot_pos != list(robot_target):
                    time.sleep(0.05)  # Simulación de movimiento
                print(f"Pedido entregado a la mesa {mesa_numero}")
                time.sleep(1)  # Simula tiempo de entrega
                robot_target[:] = [400, 50]  # Regreso a la cocina


def generate_orders():
    while running:
        table = random.randint(1, len(restaurante.mesas))
        orders.append(table)
        print(f"Nuevo pedido para mesa {table}")
        time.sleep(random.randint(2, 5))


# Crear el ThreadPoolExecutor
executor = ThreadPoolExecutor(max_workers=2)
executor.submit(generate_orders)
executor.submit(move_robot)

# BUCLE PRINCIPAL
while running:
    screen.fill((50, 50, 50))

    # Dibujar mesas
    for mesa in restaurante.mesas:
        pygame.draw.rect(screen, (150, 75, 0), (mesa.posicion[0] - 30, mesa.posicion[1] - 20, 60, 40))
        font = pygame.font.Font(None, 24)
        text = font.render(str(mesa.numero), True, (255, 255, 255))
        screen.blit(text, (mesa.posicion[0] - 5, mesa.posicion[1] - 10))  # Número de mesa

    # Mover el robot suavemente hacia su destino
    if robot_pos[0] < robot_target[0]:
        robot_pos[0] += 2
    elif robot_pos[0] > robot_target[0]:
        robot_pos[0] -= 2

    if robot_pos[1] < robot_target[1]:
        robot_pos[1] += 2
    elif robot_pos[1] > robot_target[1]:
        robot_pos[1] -= 2

    # Dibujar robot
    pygame.draw.circle(screen, (0, 255, 0), robot_pos, 20)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(30)

# Cierre del programa
pygame.quit()
executor.shutdown(wait=False)
