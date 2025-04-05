import time
import math
from restaurante import Restaurante

robot_pos = [400, 50]  # Cocina
robot_target = [400, 50]
CAPACIDAD_MAXIMA = 3

pending_orders = []     # Pedidos en espera
prepared_orders = []    # Pedidos listos en cocina
delivering_orders = []  # Pedidos que el robot llevará en la siguiente ronda

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
    while True:
        if len(delivering_orders) == 0 and len(prepared_orders) > 0:
            print("🔄 Calculando la mejor ruta de entrega...")

            mover_robot([400, 50])  # Cocina
            print(f"📍 Robot llegó a la cocina. Pedidos listos: {prepared_orders}")

            if not prepared_orders:
                print("⚠️ No hay pedidos listos para recoger.")
                time.sleep(1)
                continue  # Salta la iteración si no hay pedidos listos

            while prepared_orders and len(delivering_orders) < CAPACIDAD_MAXIMA:
                pedido = prepared_orders.pop(0)
                delivering_orders.append(pedido)
                print(f"📦 Robot recoge pedido para mesa {pedido}")

            print(f"📦 Pedidos en reparto: {delivering_orders}")

            if not delivering_orders:
                print("⚠️ No hay pedidos en reparto.")
                time.sleep(1)
                continue

            ruta_optima = calcular_ruta_optima()
            print(f"🚀 Ruta óptima calculada: {ruta_optima}")

            for mesa_numero in ruta_optima:
                destino = restaurante.get_posicion_mesa(mesa_numero)
                if destino:
                    print(f"🏃‍♂️ Llevando pedido a la mesa {mesa_numero}...")
                    mover_robot(destino)
                    print(f"✅ Pedido entregado en mesa {mesa_numero}")
                    time.sleep(1)

            pedidos_entregados = delivering_orders.copy()
            delivering_orders.clear()
            print(f"📦 Pedidos entregados, lista vaciada. Anteriormente: {pedidos_entregados}")

            time.sleep(1)
            print("📦 Pedidos entregados, lista vaciada.")
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
