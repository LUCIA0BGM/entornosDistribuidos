import pygame
import random
import time
from concurrent.futures import ThreadPoolExecutor
import math
from mesa import Mesa
from restaurante import Restaurante
from robot import move_robot


pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Variables globales
robot_pos = [400, 50]  # Cocina
robot_target = [400, 50]
CAPACIDAD_MAXIMA = 3

pending_orders = []     # Pedidos en espera
prepared_orders = []    # Pedidos listos en cocina
delivering_orders = []  # Pedidos que el robot llevará en la siguiente ronda

running = True
font = pygame.font.Font(None, 24)

# CLASES
"""""
class Mesa:
    def __init__(self, numero, x, y):
        self.numero = numero
        self.posicion = (x, y)
        self.width = 60
        self.height = 40

    def get_rect(self):
        return pygame.Rect(self.posicion[0] - self.width // 2, self.posicion[1] - self.height // 2, self.width, self.height)

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
        return None
"""
restaurante = Restaurante()

def distancia(p1, p2):
    """Calcula la distancia entre dos puntos"""
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def calcular_ruta_optima():
    """Ordena las entregas por proximidad con algoritmo Greedy"""
    global delivering_orders
    ruta = []
    origen = robot_pos  # La cocina o donde esté el robot

    while delivering_orders:
        # Busca la mesa más cercana
        siguiente_mesa = min(delivering_orders, key=lambda mesa: distancia(origen, restaurante.get_posicion_mesa(mesa)))
        delivering_orders.remove(siguiente_mesa)
        ruta.append(siguiente_mesa)
        origen = restaurante.get_posicion_mesa(siguiente_mesa)  # Actualiza la posición actual

    return ruta

def move_robot():
    global robot_target
    while running:
        if len(delivering_orders) == 0 and len(prepared_orders) > 0:
            print("🔄 Calculando la mejor ruta de entrega...")

            # Asegurar que el robot va a la cocina antes de recoger pedidos
            mover_robot([400, 50])
            print(f"📍 Robot llegó a la cocina. Pedidos listos: {prepared_orders}")

            # Verificar si hay pedidos listos
            if not prepared_orders:
                print("⚠️ No hay pedidos listos para recoger.")
                time.sleep(1)
                continue  # Salta la iteración si no hay pedidos listos

            # Cargar pedidos listos hasta la capacidad máxima
            while prepared_orders and len(delivering_orders) < CAPACIDAD_MAXIMA:
                pedido = prepared_orders.pop(0)
                delivering_orders.append(pedido)
                print(f"📦 Robot recoge pedido para mesa {pedido}")

            print(f"📦 Pedidos en reparto: {delivering_orders}")

            # Si no hay pedidos en reparto, no hacer nada
            if not delivering_orders:
                print("⚠️ No hay pedidos en reparto.")
                time.sleep(1)
                continue

            # Ordenar los pedidos por la mejor ruta
            ruta_optima = calcular_ruta_optima()
            print(f"🚀 Ruta óptima calculada: {ruta_optima}")

            # Moverse siguiendo la ruta optimizada
            for mesa_numero in ruta_optima:
                destino = restaurante.get_posicion_mesa(mesa_numero)
                if destino:
                    print(f"🏃‍♂️ Llevando pedido a la mesa {mesa_numero}...")
                    mover_robot(destino)
                    print(f"✅ Pedido entregado en mesa {mesa_numero}")
                    time.sleep(1)

            # Vaciar pedidos entregados
            pedidos_entregados = delivering_orders.copy()
            delivering_orders.clear()
            print(f"📦 Pedidos entregados, lista vaciada. Anteriormente: {pedidos_entregados}")

            # Esperar un poco para que se vea en la pantalla antes de vaciar
            time.sleep(1)
            print("📦 Pedidos entregados, lista vaciada.")

            # Regresar a la cocina
            print("🔙 Volviendo a la cocina")
            mover_robot([400, 50])



def mover_robot(destino):
    """Mueve el robot en línea recta (sin evitar obstáculos)"""
    global robot_pos
    while robot_pos[0] != destino[0]:
        robot_pos[0] += 2 if destino[0] > robot_pos[0] else -2
        time.sleep(0.02)

    while robot_pos[1] != destino[1]:
        robot_pos[1] += 2 if destino[1] > robot_pos[1] else -2
        time.sleep(0.02)

def generate_orders():
    while running:
        table = random.randint(1, len(restaurante.mesas))
        pending_orders.append(table)
        print(f"📝 Nuevo pedido para mesa {table}")

        time.sleep(random.randint(3, 5))

        if table in pending_orders:
            pending_orders.remove(table)
            prepared_orders.append(table)
            print(f"🍽️ Pedido para mesa {table} está listo en la cocina.")

executor = ThreadPoolExecutor(max_workers=2)
executor.submit(generate_orders)
executor.submit(move_robot)

# BUCLE PRINCIPAL
while running:
    screen.fill((50, 50, 50))

    for mesa in restaurante.mesas:
        pygame.draw.rect(screen, (150, 75, 0), (mesa.posicion[0] - 30, mesa.posicion[1] - 20, 60, 40))
        text = font.render(str(mesa.numero), True, (255, 255, 255))
        screen.blit(text, (mesa.posicion[0] - 5, mesa.posicion[1] - 10))

    pygame.draw.circle(screen, (0, 255, 0), robot_pos, 20)

    screen.blit(font.render("📝 Pedidos en espera:", True, (255, 255, 255)), (20, 20))
    for i, pedido in enumerate(pending_orders):
        screen.blit(font.render(f"Mesa {pedido}", True, (255, 255, 255)), (20, 40 + i * 20))

    screen.blit(font.render("🍽️ Pedidos listos en cocina:", True, (255, 255, 255)), (220, 20))
    for i, pedido in enumerate(prepared_orders):
        screen.blit(font.render(f"Mesa {pedido}", True, (255, 255, 255)), (220, 40 + i * 20))

    screen.blit(font.render("📦 Pedidos en reparto:", True, (255, 255, 255)), (420, 20))
    for i, pedido in enumerate(delivering_orders):
        screen.blit(font.render(f"Mesa {pedido}", True, (255, 255, 255)), (420, 40 + i * 20))


    print(f"📦 Pedidos en reparto en pantalla: {delivering_orders}")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
executor.shutdown(wait=False)
