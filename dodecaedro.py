import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from mpl_toolkits.mplot3d import Axes3D

# --- PARÁMETROS DEL DODECAEDRO ---
NUM_AGUJEROS = 12
DIAMETRO_AGUJEROS = 2.5  # cm
RADIO_ESFERA = 8.0       # cm

# --- GENERAR GEOMETRÍA DODECAÉDRICA ---


def generar_posiciones_agujeros():
    """Genera las posiciones de los 12 agujeros en un dodecaedro"""
    # Coordenadas de los vértices de un dodecaedro (simplificado)
    phi = (1 + np.sqrt(5)) / 2  # razón áurea
    vertices = []

    for i in [-1, 1]:
        for j in [-1, 1]:
            for k in [-1, 1]:
                vertices.append([i, i, i])
                vertices.append([0, j*phi, k/phi])
                vertices.append([j*phi, k/phi, 0])
                vertices.append([k/phi, 0, j*phi])

    # Normalizar y seleccionar 12 puntos para agujeros
    vertices = np.unique(vertices, axis=0)[:12]
    return vertices * RADIO_ESFERA

# --- SIMULAR PROPAGACIÓN DE ONDAS ---


def simular_propagacion_onda(agujero_entrada, frecuencia, tipo_onda='sonido'):
    """Simula la propagación de ondas dentro del dodecaedro"""

    posiciones = generar_posiciones_agujeros()

    # Configurar onda de entrada
    if tipo_onda == 'sonido':
        velocidad = 34300  # cm/s (sonido en aire)
        longitud_onda = velocidad / frecuencia
    else:  # luz
        velocidad = 3e10   # cm/s (luz)
        longitud_onda = velocidad / frecuencia

    # Simular interferencias
    patron_interior = np.zeros(1000)
    patron_salida = np.zeros((NUM_AGUJEROS, 1000))

    for i in range(NUM_AGUJEROS):
        if i == agujero_entrada:
            continue  # Saltar agujero de entrada

        # Calcular distancia relativa
        dist = np.linalg.norm(posiciones[i] - posiciones[agujero_entrada])

        # Simular onda que llega a este agujero
        t = np.linspace(0, 0.01, 1000)
        onda = np.sin(2 * np.pi * frecuencia * t -
                      2 * np.pi * dist / longitud_onda)

        # Atenuar por distancia y geometría
        atenuacion = 1 / (1 + dist**2 / RADIO_ESFERA**2)
        patron_salida[i] = onda * atenuacion

        # Contribución al patrón interior
        patron_interior += onda * atenuacion * 0.3

    return patron_interior, patron_salida, posiciones

# --- VISUALIZAR RESULTADOS ---


def visualizar_patrones(agujero_entrada=0, frecuencia=1000, tipo_onda='sonido'):
    """Genera visualización completa"""

    patron_int, patron_sal, posiciones = simular_propagacion_onda(
        agujero_entrada, frecuencia, tipo_onda)

    # Crear figura 3D
    fig = plt.figure(figsize=(15, 10))

    # 1. Visualización 3D de agujeros
    ax1 = fig.add_subplot(221, projection='3d')
    ax1.scatter(posiciones[:, 0], posiciones[:, 1],
                posiciones[:, 2], s=100, c='blue')
    ax1.scatter(posiciones[agujero_entrada, 0],
                posiciones[agujero_entrada, 1],
                posiciones[agujero_entrada, 2], s=200, c='red', marker='X')
    ax1.set_title('Posiciones de agujeros (Rojo: entrada)')

    # 2. Patrón interior
    ax2 = fig.add_subplot(222)
    t = np.linspace(0, 0.01, 1000)
    ax2.plot(t, patron_int)
    ax2.set_title('Patrón de interferencia INTERIOR')
    ax2.set_xlabel('Tiempo (s)')
    ax2.set_ylabel('Amplitud')

    # 3. Patrones de salida
    ax3 = fig.add_subplot(212)
    for i in range(NUM_AGUJEROS):
        if i != agujero_entrada:
            ax3.plot(t, patron_sal[i] + i*2, label=f'Agujero {i}')
    ax3.set_title('PATRONES DE SALIDA por cada agujero')
    ax3.set_xlabel('Tiempo (s)')
    ax3.set_ylabel('Amplitud (desplazada)')
    ax3.legend()

    plt.tight_layout()
    plt.savefig(
        f'dodecaedro_entrada_{agujero_entrada}_freq_{frecuencia}_{tipo_onda}.png', dpi=300)
    plt.show()

    return patron_int, patron_sal


# --- EJECUTAR SIMULACIÓN ---
print("🎵 SIMULANDO DODECAEDRO COMO CÁMARA DE RESONANCIA")
print("🔊 Entrada: Agujero 0 | Frecuencia: 1000 Hz (Sonido)")

patron_interior, patron_salida = visualizar_patrones(
    agujero_entrada=0,
    frecuencia=1000,
    tipo_onda='sonido'
)

# --- ANÁLISIS DE RESULTADOS ---
print("\n📊 RESULTADOS OBTENIDOS:")
print(f"• Agujero entrada: 0")
print(f"• Frecuencia: 1000 Hz")
print(f"• Patrones salida generados: {len(patron_salida)}")

# Calcular diferencias entre agujeros
diferencias = []
for i in range(len(patron_salida)):
    for j in range(i+1, len(patron_salida)):
        if i != 0 and j != 0:  # Excluir agujero entrada
            diff = np.mean(np.abs(patron_salida[i] - patron_salida[j]))
            diferencias.append(diff)

print(f"• Diferencia promedio entre salidas: {np.mean(diferencias):.4f}")
print(f"• Máxima diferencia: {np.max(diferencias):.4f}")
print(f"• Mínima diferencia: {np.min(diferencias):.4f}")

# --- GENERAR ARCHIVO DE DATOS ---
np.savez('patrones_dodecaedro.npz',
         interior=patron_interior,
         salida=patron_salida,
         posiciones=generar_posiciones_agujeros())

print("\n💾 Datos guardados en 'patrones_dodecaedro.npz'")
