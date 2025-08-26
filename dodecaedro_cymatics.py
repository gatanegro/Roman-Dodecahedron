import numpy as np
import matplotlib.pyplot as plt
from scipy import special

# --- SIMULACIÓN DE EFECTOS CIMÁTICOS ---


def simular_patrones_cimaticos(dodecaedro, frecuencia, medio='arena'):
    """Simula patrones cimáticos generados por el dodecaedro"""

    # Propiedades del medio según material (CORREGIDO: resonancia como tupla)
    propiedades = {
        'arena': {'densidad': 1.6, 'resonancia': (50, 200)},
        'agua': {'densidad': 1.0, 'resonancia': (20, 500)},
        'piedra_polvo': {'densidad': 2.4, 'resonancia': (100, 1000)},
        'metal_fundido': {'densidad': 7.8, 'resonancia': (200, 2000)}
    }

    prop = propiedades[medio]

    # Generar patrones basados en geometría dodecaédrica
    x = np.linspace(-2, 2, 1000)
    y = np.linspace(-2, 2, 1000)
    X, Y = np.meshgrid(x, y)

    # Patrón de interferencia dodecaédrica
    R = np.sqrt(X**2 + Y**2)
    Theta = np.arctan2(Y, X)

    # 12 puntas (como los 12 agujeros)
    patron = np.zeros_like(X)
    for n in range(12):
        angulo = n * np.pi/6
        patron += np.cos(12*(Theta - angulo)) * np.exp(-R**2/0.5)

    # Modulación por frecuencia
    modulacion_frecuencia = np.sin(2*np.pi*frecuencia*R/10)
    patron *= modulacion_frecuencia

    # Efectos de resonancia (CORREGIDO: acceder a tupla)
    if frecuencia > prop['resonancia'][0] and frecuencia < prop['resonancia'][1]:
        patron *= 2.0  # Amplificación por resonancia

    return X, Y, patron

# --- VISUALIZACIÓN PATRONES CIMÁTICOS ---


def visualizar_cimatica(dodecaedro, frecuencias, medio='arena'):
    """Visualiza patrones cimáticos para diferentes frecuencias"""

    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()

    for i, freq in enumerate(frecuencias):
        X, Y, patron = simular_patrones_cimaticos(dodecaedro, freq, medio)

        im = axes[i].contourf(X, Y, patron, levels=50, cmap='viridis')
        axes[i].set_title(f'Frecuencia: {freq} Hz\nMedio: {medio}')
        axes[i].set_aspect('equal')

        # Dibujar silueta del dodecaedro
        circle = plt.Circle((0, 0), 1.0, fill=False,
                            color='red', linestyle='--')
        axes[i].add_patch(circle)

    plt.colorbar(im, ax=axes, shrink=0.8)
    plt.suptitle(
        f'PATRONES CIMÁTICOS DEL DODECAEDRO EN {medio.upper()}', fontsize=16)
    plt.tight_layout()
    plt.show()

# --- SIMULACIÓN CONSTRUCCIÓN MEGALÍTICA ---


def simular_construccion_megalitica(dodecaedro, frecuencia=432):
    """Simula cómo el dodecaedro podría usarse en construcción megalítica"""

    print("🧱 SIMULACIÓN CONSTRUCCIÓN MEGALÍTICA")
    print("=" * 50)

    # Frecuencias de resonancia para diferentes materiales de construcción
    materiales = {
        'granito': {'frecuencia_resonancia': 320, 'densidad': 2.7},
        'caliza': {'frecuencia_resonancia': 280, 'densidad': 2.5},
        'arenisca': {'frecuencia_resonancia': 240, 'densidad': 2.3},
        'arcilla': {'frecuencia_resonancia': 180, 'densidad': 1.8}
    }

    resultados = []

    for material, props in materiales.items():
        # Calcular acoplamiento acústico
        acoplamiento = frecuencia / props['frecuencia_resonancia']
        eficiencia = np.exp(-abs(1 - acoplamiento)**2)

        # Calcular fuerza de levitación acústica estimada
        # F = ρ * A * a^2 * ω^2 / (2 * c^2) [aproximación]
        fuerza = props['densidad'] * 0.1 * \
            (0.01)**2 * (2*np.pi*frecuencia)**2 / (2 * (343)**2)
        fuerza *= eficiencia * 1000  # Escalar para visualización

        resultados.append({
            'material': material,
            'acoplamiento': acoplamiento,
            'eficiencia': eficiencia,
            'fuerza_estimada': fuerza
        })

        print(f"{material:10} | Acoplamiento: {acoplamiento:.2f} | Eficiencia: {eficiencia:.2%} | Fuerza: {fuerza:.4f} N")

    return resultados

# --- ANALIZAR CONEXIÓN CON HIPOGEO DE MALTA ---


def analizar_compatibilidad_hipogeo():
    """Analiza si el dodecaedro podría haber sido usado en el hipogeo"""

    # Usar los diámetros reales del modelo SCAD
    DIAMETROS_AGUJEROS_SUPERIOR = [26, 21.5, 16.5, 21, 11.5, 17]
    DIAMETROS_AGUJEROS_INFERIOR = [25.5, 10.5, 15.5, 22, 17, 22]
    diametros_todos = DIAMETROS_AGUJEROS_SUPERIOR + DIAMETROS_AGUJEROS_INFERIOR

    frecuencia_hipogeo = 110  # Hz (frecuencia de resonancia medida)

    print("🔍 ANALIZANDO CONEXIÓN CON HIPOGEO DE HAL SAFLIENI (Malta)")
    print("=" * 60)
    print("Agujeros que resonarían en el Hipogeo (110 Hz):")
    print("Índice | Diámetro (mm) | Frecuencia natural | Diferencia")
    print("-" * 65)

    mejores_ajustes = []

    for i, diametro in enumerate(diametros_todos):
        # Frecuencia natural aproximada para abertura circular
        # f ≈ c / (2 * d) para modo fundamental
        freq_natural = 343000 / (2 * diametro)  # mm/s / mm = Hz
        diferencia = abs(freq_natural - frecuencia_hipogeo)

        if diferencia < 50:  # ±50 Hz de tolerancia
            estrella = "★"
            mejores_ajustes.append((i, diametro, freq_natural, diferencia))
        else:
            estrella = ""

        print(
            f"{i:6} | {diametro:13.1f} | {freq_natural:17.1f} Hz | {diferencia:8.1f} Hz {estrella}")

    return mejores_ajustes


# --- EJECUTAR SIMULACIONES ---
print("🌀 SIMULANDO APLICACIONES CIMÁTICAS MEGALÍTICAS")
print("📍 Conexión con templos malteses y stonehenge")

# 1. Patrones cimáticos en diferentes medios
frecuencias_test = [64, 128, 256, 432, 528, 864]
visualizar_cimatica(None, frecuencias_test, 'arena')
visualizar_cimatica(None, frecuencias_test, 'agua')
visualizar_cimatica(None, frecuencias_test, 'piedra_polvo')

# 2. Simulación construcción megalítica
resultados = simular_construccion_megalitica(None, frecuencia=432)

# 3. Visualización fuerzas de levitación
fig, ax = plt.subplots(figsize=(10, 6))
materiales = [r['material'] for r in resultados]
fuerzas = [r['fuerza_estimada'] for r in resultados]

bars = ax.bar(materiales, fuerzas, color=[
              '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
ax.set_ylabel('Fuerza de levitación estimada (N)')
ax.set_title('EFECTO LEVITACIÓN ACÚSTICA POR MATERIAL\n(Frecuencia 432 Hz)')
ax.set_yscale('log')

for bar, resultado in zip(bars, resultados):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height * 1.05,
            f'{resultado["eficiencia"]:.1%}',
            ha='center', va='bottom')

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 4. Análisis específico para el Hipogeo de Malta
mejores_ajustes = analizar_compatibilidad_hipogeo()

print(f"\n🎯 MEJORES AJUSTES PARA HIPOGEO (110 Hz):")
for i, diametro, freq, diff in mejores_ajustes:
    print(
        f"Agujero {i}: Ø{diametro}mm → {freq:.1f}Hz (diferencia: {diff:.1f}Hz)")

# 5. Protocolo de construcción hipotético
print("\n🔨 PROTOCOLO DE CONSTRUCCIÓN MEGALÍTICA HIPOTÉTICO:")
print("1. Identificar frecuencia de resonancia de la piedra (ej: 110Hz para maltesa)")
print("2. Seleccionar agujero del dodecaedro que resuene a esa frecuencia")
print("3. Generar tono con instrumento primitivo (cuerno/trompeta/voz)")
print("4. Dirigir sonido through agujero seleccionado hacia la piedra")
print("5. Observar patrones cimáticos en polvo de piedra para afinar")
print("6. Aplicar sonido resonante continuo para 'ablandar' la piedra")
print("7. Mover/posicionar la piedra con menor esfuerzo")

# 6. Predicciones y experimento propuesto
print("\n🧪 EXPERIMENTO CRUCIAL PARA VALIDAR:")
print("• Medir resonancia real de réplicas del dodecaedro")
print("• Testear reducción de dureza en piedra por exposición acústica")
print("• Buscar correlación entre frecuencias de dodecaedros y sitios megalíticos")
print("• Recrear patrones cimáticos con geometría dodecaédrica")

# 7. Evidencia circunstancial
print("\n📖 EVIDENCIA CIRCUNSTANCIAL:")
print("• Dodecaedros encontrados cerca de sitios megalíticos")
print("• Tradiciones de 'piedras que cantan' en múltiples culturas")
print("• Precisión acústica inexplicable en construcciones antiguas")
print("• Conocimiento geométtico-musical avanzado en escuelas de misterio")
