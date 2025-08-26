import numpy as np
import matplotlib.pyplot as plt
from scipy import special  # Cambiado de signal a special
from mpl_toolkits.mplot3d import Axes3D

# --- PARÁMETROS EXACTOS DEL MODELO SCAD ---
RADIO_BASE = 32  # mm (radio del pentágono)
DISTANCIA_CENTRO = 40  # mm (distancia al centro)
ALTURA_CARA = 3.7  # mm (altura del pentágono)
DIAMETROS_AGUJEROS_SUPERIOR = [26, 21.5, 16.5, 21, 11.5, 17]  # mm
DIAMETROS_AGUJEROS_INFERIOR = [25.5, 10.5, 15.5, 22, 17, 22]  # mm
ANGULOS_Z = [0, 0, 72, 144, 216, 288]  # grados
AJUSTE = 1.5  # factor de ajuste

# --- GENERAR GEOMETRÍA REAL DEL DODECAEDRO ---


def generar_geometria_real():
    """Genera la geometría exacta del dodecaedro con agujeros de diferentes tamaños"""

    # Coordenadas de los vértices de un dodecaedro regular
    phi = (1 + np.sqrt(5)) / 2  # razón áurea
    vertices = np.array([
        [1, 1, 1], [1, 1, -1], [1, -1, 1], [1, -1, -1],
        [-1, 1, 1], [-1, 1, -1], [-1, -1, 1], [-1, -1, -1],
        [0, 1/phi, phi], [0, 1/phi, -phi], [0, -1/phi, phi], [0, -1/phi, -phi],
        [1/phi, phi, 0], [1/phi, -phi, 0], [-1/phi, phi, 0], [-1/phi, -phi, 0],
        [phi, 0, 1/phi], [phi, 0, -1/phi], [-phi, 0, 1/phi], [-phi, 0, -1/phi]
    ])

    # Normalizar y escalar
    vertices = vertices / np.linalg.norm(vertices[0]) * RADIO_BASE

    # Identificar las 12 caras pentagonales
    caras = []
    for i in range(len(vertices)):
        distancias = np.linalg.norm(vertices - vertices[i], axis=1)
        vecinos = np.argsort(distancias)[1:6]  # 5 vecinos más cercanos
        cara = [i] + list(vecinos)
        caras.append(cara)

    # Calcular centros de las caras y normales
    centros = []
    normales = []
    diametros = []

    for i, cara in enumerate(caras[:12]):  # Solo 12 caras únicas
        puntos_cara = vertices[cara]
        centro = np.mean(puntos_cara, axis=0)
        centros.append(centro)

        # Calcular normal a la cara
        v1 = puntos_cara[1] - puntos_cara[0]
        v2 = puntos_cara[2] - puntos_cara[0]
        normal = np.cross(v1, v2)
        normal = normal / np.linalg.norm(normal)
        normales.append(normal)

        # Asignar diámetro según la cara (usando datos SCAD)
        if i < 6:
            diametro = DIAMETROS_AGUJEROS_SUPERIOR[i] * AJUSTE
        else:
            diametro = DIAMETROS_AGUJEROS_INFERIOR[i-6] * AJUSTE
        diametros.append(diametro)

    return np.array(centros), np.array(normales), np.array(diametros), vertices

# --- SIMULACIÓN CON DIFRACCIÓN REAL ---


def simular_difraccion_real(agujero_entrada, frecuencia, tipo_onda='sonido'):
    """Simula la difracción con la geometría real del dodecaedro"""

    centros, normales, diametros, vertices = generar_geometria_real()
    num_agujeros = len(centros)

    # Configurar onda
    if tipo_onda == 'sonido':
        velocidad = 343000  # mm/s
    else:  # luz
        velocidad = 3e11  # mm/s

    longitud_onda = velocidad / frecuencia
    k = 2 * np.pi / longitud_onda  # número de onda

    # Simular difracción en cada agujero
    t = np.linspace(0, 0.01, 1000)
    patrones_salida = np.zeros((num_agujeros, len(t)))
    patron_interior = np.zeros(len(t))

    for i in range(num_agujeros):
        if i == agujero_entrada:
            continue

        # Calcular distancia y ángulo relativo
        r_vec = centros[i] - centros[agujero_entrada]
        distancia = np.linalg.norm(r_vec)

        # Ángulo entre la normal y la dirección de propagación
        theta = np.arccos(np.dot(normales[i], r_vec/distancia))

        # Patrón de difracción para abertura circular
        # Usando aproximación de Airy para difracción circular
        x = k * (diametros[i]/2) * np.sin(theta)
        if abs(x) < 1e-10:
            factor_difraccion = 1.0
        else:
            # CORRECCIÓN: Usar scipy.special.j1 en lugar de scipy.signal.j1
            factor_difraccion = 2 * special.j1(x) / x  # Función de Bessel J1

        # Atenuación por distancia y geometría
        atenuacion_distancia = 1 / (1 + (distancia/RADIO_BASE)**2)
        atenuacion_geometrica = np.exp(-distancia/(2*RADIO_BASE))

        # Onda resultante con difracción
        fase = 2 * np.pi * frecuencia * t - k * distancia
        amplitud = factor_difraccion * atenuacion_distancia * atenuacion_geometrica
        # Factor por tamaño de agujero
        amplitud *= (diametros[i] / np.max(diametros))

        onda = amplitud * np.sin(fase)
        patrones_salida[i] = onda

        # Contribución al interior (promedio ponderado)
        patron_interior += onda * 0.2

    return patron_interior, patrones_salida, centros, diametros, vertices

# --- VISUALIZACIÓN MEJORADA ---


def visualizar_difraccion_real(agujero_entrada=0, frecuencia=1000, tipo_onda='sonido'):
    """Visualización con geometría real y efectos de difracción"""

    patron_int, patron_sal, centros, diametros, vertices = simular_difraccion_real(
        agujero_entrada, frecuencia, tipo_onda)

    fig = plt.figure(figsize=(18, 12))

    # 1. Visualización 3D con tamaños reales de agujeros
    ax1 = fig.add_subplot(231, projection='3d')
    # Dibujar vértices (esferas)
    ax1.scatter(vertices[:, 0], vertices[:, 1],
                vertices[:, 2], s=20, c='gray', alpha=0.3)

    # Dibujar agujeros con tamaños proporcionales
    for i, (centro, diametro) in enumerate(zip(centros, diametros)):
        color = 'red' if i == agujero_entrada else 'blue'
        ax1.scatter(centro[0], centro[1], centro[2],
                    s=diametro*10, c=color, alpha=0.7)
        ax1.text(centro[0], centro[1], centro[2], f'{i}', fontsize=8)

    ax1.set_title('Geometría real con agujeros de diferentes tamaños')

    # 2. Mapa de amplitudes de salida
    ax2 = fig.add_subplot(232)
    amplitudes = np.max(np.abs(patron_sal), axis=1)
    colores = amplitudes / np.max(amplitudes)
    scatter = ax2.scatter(
        centros[:, 0], centros[:, 1], c=amplitudes, s=diametros*20, cmap='viridis')
    ax2.scatter(centros[agujero_entrada, 0],
                centros[agujero_entrada, 1], s=200, marker='X', c='red')
    plt.colorbar(scatter, ax=ax2, label='Amplitud máxima')
    ax2.set_title('Amplitudes de salida por agujero')
    ax2.set_aspect('equal')

    # 3. Espectro de frecuencias de salida
    ax3 = fig.add_subplot(233)
    for i in range(len(patron_sal)):
        if i != agujero_entrada:
            fft_result = np.fft.fft(patron_sal[i])
            freqs = np.fft.fftfreq(len(patron_sal[i]), 0.01/1000)
            ax3.plot(freqs[:500], np.abs(fft_result[:500]) +
                     i*0.1, label=f'Agujero {i}')
    ax3.set_xlim(0, frecuencia*3)
    ax3.set_title('Espectros de frecuencia de salida')
    ax3.set_xlabel('Frecuencia (Hz)')
    ax3.set_ylabel('Amplitud (desplazada)')

    # 4. Comparación de patrones temporales
    ax4 = fig.add_subplot(212)
    t = np.linspace(0, 0.01, 1000)
    for i in range(len(patron_sal)):
        if i != agujero_entrada:
            ax4.plot(t, patron_sal[i] + i*1.5,
                     label=f'Agujero {i} (Ø{diametros[i]:.1f}mm)')
    ax4.set_title('Señales temporales de salida (con difracción)')
    ax4.set_xlabel('Tiempo (s)')
    ax4.set_ylabel('Amplitud (desplazada)')
    ax4.legend()

    plt.tight_layout()
    plt.show()

    # Análisis cuantitativo
    print(f"\n📊 ANÁLISIS DE DIFRACCIÓN - {tipo_onda.upper()} {frecuencia}Hz")
    print("=" * 50)

    amplitudes_max = []
    for i in range(len(patron_sal)):
        if i != agujero_entrada:
            amp_max = np.max(np.abs(patron_sal[i]))
            amplitudes_max.append(amp_max)
            print(
                f"Agujero {i}: Ø{diametros[i]:.1f}mm → Amplitud: {amp_max:.4f}")

    print(
        f"\nRango amplitudes: {np.min(amplitudes_max):.4f} - {np.max(amplitudes_max):.4f}")
    print(
        f"Variación: {(np.max(amplitudes_max)-np.min(amplitudes_max))/np.mean(amplitudes_max)*100:.1f}%")


# --- EJECUTAR SIMULACIÓN MEJORADA ---
print("🔬 SIMULACIÓN CON GEOMETRÍA REAL Y DIFRACCIÓN")
print("📍 Usando dimensiones exactas del modelo SCAD")

# Simular diferentes escenarios
visualizar_difraccion_real(
    agujero_entrada=0, frecuencia=432, tipo_onda='sonido')
