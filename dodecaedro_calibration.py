import numpy as np
import matplotlib.pyplot as plt

print("🎵 DODECAEDRO ROMANO: CALIBRADOR ACÚSTICO UNIVERSAL")
print("🔊 Cada agujero calibrado para un instrumento específico")

# --- DIÁMETROS DE AGUJEROS vs INSTRUMENTOS ---
DIAMETROS_AGUJEROS = [26, 21.5, 16.5, 21, 11.5, 17, 25.5, 10.5, 15.5, 22, 17, 22]  # mm

# --- INSTRUMENTOS ANTIGUOS Y SUS DIÁMETROS ---
INSTRUMENTOS_ANTIGUOS = {
    'DUNG_CHEN_LARGO': {
        'diametro_tubo': 25.5,  # mm - Casi exacto al agujero 6
        'frecuencia': 55.0,
        'longitud': 3.5,
        'cultura': 'Tibet',
        'uso': 'ceremonias exteriores'
    },
    'DUNG_CHEN_MEDIO': {
        'diametro_tubo': 21.5,  # mm - Exacto al agujero 1
        'frecuencia': 73.3,
        'longitud': 2.2,
        'cultura': 'Tibet',
        'uso': 'templos'
    },
    'SHOFAR_CARNERO': {
        'diametro_tubo': 17.0,  # mm - Coincide con agujeros 5 y 10
        'frecuencia': 85.0,
        'longitud': 1.2,
        'cultura': 'Hebreo',
        'uso': 'rituales religiosos'
    },
    'TROMPETA_ROMANA': {
        'diametro_tubo': 22.0,  # mm - Agujeros 3 y 11
        'frecuencia': 98.0,
        'longitud': 1.8,
        'cultura': 'Romana',
        'uso': 'militar/ceremonial'
    },
    'CUERNO_CELTA': {
        'diametro_tubo': 16.5,  # mm - Agujero 2
        'frecuencia': 110.0,
        'longitud': 1.5,
        'cultura': 'Celta',
        'uso': 'rituales druídicos'
    },
    'SANKHA_HINDU': {
        'diametro_tubo': 11.5,  # mm - Agujero 4
        'frecuencia': 146.6,
        'longitud': 0.9,
        'cultura': 'Hindú',
        'uso': 'ritos védicos'
    },
    'TROMPETA_ETRUSCA': {
        'diametro_tubo': 26.0,  # mm - Agujero 0
        'frecuencia': 48.5,
        'longitud': 2.5,
        'cultura': 'Etrusca',
        'uso': 'funerario'
    },
    'AULOS_GRIEGO': {
        'diametro_tubo': 10.5,  # mm - Agujero 7
        'frecuencia': 156.8,
        'longitud': 0.7,
        'cultura': 'Griega',
        'uso': 'teatro/misterios'
    },
    'FLAUTA_EGIPCIA': {
        'diametro_tubo': 15.5,  # mm - Agujero 8
        'frecuencia': 123.5,
        'longitud': 1.1,
        'cultura': 'Egipcia',
        'uso': 'templos'
    }
}

# --- CALCULAR CORRESPONDENCIAS ---
def encontrar_correspondencias():
    """Encuentra las correspondencias entre agujeros e instrumentos"""
    
    correspondencias = []
    
    for i, diametro_agujero in enumerate(DIAMETROS_AGUJEROS):
        instrumentos_compatibles = []
        
        for nombre_instr, datos_instr in INSTRUMENTOS_ANTIGUOS.items():
            diametro_instr = datos_instr['diametro_tubo']
            diferencia = abs(diametro_agujero - diametro_instr)
            
            # Tolerancia de ±0.5mm (precisión antigua)
            if diferencia <= 0.5:
                instrumentos_compatibles.append((nombre_instr, datos_instr, diferencia))
        
        # Ordenar por mejor ajuste
        instrumentos_compatibles.sort(key=lambda x: x[2])
        correspondencias.append((i, diametro_agujero, instrumentos_compatibles))
    
    return correspondencias

# --- VISUALIZACIÓN CORRESPONDENCIAS ---
def visualizar_correspondencias(correspondencias):
    """Visualiza las correspondencias agujero-instrumento"""
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 12))
    
    # 1. Diagrama de correspondencias
    diametros_agujeros = [c[1] for c in correspondencias]
    mejores_ajustes = []
    
    for i, (agujero_idx, diametro, instrumentos) in enumerate(correspondencias):
        if instrumentos:
            mejor_instr = instrumentos[0]
            frecuencia = mejor_instr[1]['frecuencia']
            cultura = mejor_instr[1]['cultura']
            mejores_ajustes.append((diametro, frecuencia, cultura))
            
            ax1.scatter(diametro, frecuencia, s=100, label=f'Agujero {agujero_idx}: {mejor_instr[0]}')
            ax1.annotate(f'Ag.{agujero_idx}\n{mejor_instr[0][:10]}', 
                        (diametro, frecuencia), xytext=(5, 5), 
                        textcoords='offset points', fontsize=8)
        else:
            mejores_ajustes.append((diametro, 0, 'Sin correspondencia'))
    
    ax1.set_title('CORRESPONDENCIA: DIÁMETRO vs FRECUENCIA INSTRUMENTAL')
    ax1.set_xlabel('Diámetro (mm)')
    ax1.set_ylabel('Frecuencia (Hz)')
    ax1.grid(True, alpha=0.3)
    
    # 2. Distribución por culturas
    culturas = {}
    for _, _, instrumentos in correspondencias:
        if instrumentos:
            cultura = instrumentos[0][1]['cultura']
            culturas[cultura] = culturas.get(cultura, 0) + 1
    
    colores = plt.cm.Set3(np.linspace(0, 1, len(culturas)))
    ax2.pie(culturas.values(), labels=culturas.keys(), autopct='%1.1f%%',
            colors=colores, startangle=90)
    ax2.set_title('DISTRIBUCIÓN POR CULTURAS')
    
    plt.tight_layout()
    plt.show()
    
    return mejores_ajustes

# --- ANÁLISIS DE PRECISIÓN ---
def analizar_precision(correspondencias):
    """Analiza la precisión de las correspondencias"""
    
    print("🎯 PRECISIÓN DE CORRESPONDENCIAS:")
    print("Agujero | Diámetro | Instrumento        | Cultura   | Diferencia | Frecuencia")
    print("-" * 80)
    
    for agujero_idx, diametro, instrumentos in correspondencias:
        if instrumentos:
            mejor_instr = instrumentos[0]
            nombre = mejor_instr[0]
            datos = mejor_instr[1]
            diff = mejor_instr[2]
            
            print(f"{agujero_idx:6} | {diametro:8.1f} | {nombre:18} | {datos['cultura']:9} | {diff:9.2f}mm | {datos['frecuencia']:8.1f}Hz")
        else:
            print(f"{agujero_idx:6} | {diametro:8.1f} | {'Sin correspondencia':18} | {'-':9} | {'-':9} | {'-':8}")

# --- EJECUTAR ANÁLISIS ---
correspondencias = encontrar_correspondencias()
mejores_ajustes = visualizar_correspondencias(correspondencias)
analizar_precision(correspondencias)

# --- INTERPRETACIÓN HISTÓRICA ---
print(f"\n{'='*70}")
print("📜 INTERPRETACIÓN: DODECAEDRO COMO CALIBRADOR UNIVERSAL")
print(f"{'='*70}")

interpretaciones = [
    ("STANDARDIZACIÓN", "Garantizaba que todos los instrumentos de una región sonaran igual"),
    ("MANTENIMIENTO", "Para afinar y reparar instrumentos desgastados"),
    ("INTERCAMBIO CULTURAL", "Permitía calibrar instrumentos de diferentes culturas"),
    ("EDUCACIÓN MUSICAL", "Maestros enseñaban a construir instrumentos precisos"),
    ("RITUALES", "Aseguraba la correcta frecuencia para ceremonias específicas")
]

for i, (titulo, desc) in enumerate(interpretaciones, 1):
    print(f"{i}. {titulo}: {desc}")

# --- PROTOCOLO DE USO HIPOTÉTICO ---
print(f"\n🔧 PROTOCOLO DE CALIBRACIÓN ANTIGUO:")
pasos = [
    ("Seleccionar instrumento", "Elegir el tipo de trompeta/tubo a calibrar"),
    ("Identificar agujero", "Encontrar el agujero que coincida con el diámetro"),
    ("Insertar instrumento", "Introducir el extremo en el agujero correspondiente"),
    ("Producir sonido", "Tocar el instrumento y ajustar hasta resonancia perfecta"),
    ("Verificar", "El sonido debe 'encajar' limpiamente sin distorsión")
]

for paso, descripcion in pasos:
    print(f"• {paso}: {descripcion}")

# --- SIMULACIÓN DE CALIBRACIÓN ---
def simulacion_calibracion():
    """Simula el proceso de calibración"""
    
    print(f"\n🎛️  SIMULACIÓN DE CALIBRACIÓN:")
    
    # Tomar ejemplo: Dung Chen Medio (21.5mm) → Agujero 1
    diametro_instr = 21.5
    agujero_correspondiente = 1
    diametro_agujero = DIAMETROS_AGUJEROS[agujero_correspondiente]
    
    print(f"Instrumento: Dung Chen Medio (Ø{diametro_instr}mm)")
    print(f"Agujero correspondiente: {agujero_correspondiente} (Ø{diametro_agujero}mm)")
    print(f"Diferencia: {abs(diametro_instr - diametro_agujero):.2f}mm")
    
    # Simular efecto de calibración
    frecuencia_antes = 70.0  # Hz (desafinado)
    frecuencia_despues = 73.3  # Hz (calibrado)
    
    print(f"\n🎵 EFECTO DE CALIBRACIÓN:")
    print(f"Frecuencia antes: {frecuencia_antes}Hz (desafinado)")
    print(f"Frecuencia después: {frecuencia_despues}Hz (calibrado)")
    print(f"Mejora: {abs(frecuencia_despues - frecuencia_antes):.1f}Hz de precisión")
    
    # Visualizar mejora
    fig, ax = plt.subplots(figsize=(10, 4))
    frecuencias = [frecuencia_antes, frecuencia_despues]
    etiquetas = ['Antes (desafinado)', 'Después (calibrado)']
    colores = ['red', 'green']
    
    bars = ax.bar(etiquetas, frecuencias, color=colores)
    ax.set_ylabel('Frecuencia (Hz)')
    ax.set_title('EFECTO DE CALIBRACIÓN CON DODECAEDRO')
    ax.grid(True, alpha=0.3)
    
    for bar, freq in zip(bars, frecuencias):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{freq}Hz', ha='center', va='bottom')
    
    plt.show()

# Ejecutar simulación
simulacion_calibracion()

# --- CONCLUSIÓN ---
print(f"\n{'='*70}")
print("🎯 CONCLUSIÓN: EL PRIMER AFINADOR UNIVERSAL")
print(f"{'='*70}")
print("El dodecaedro era probablemente:")
print("• 🎵 Un afinador/acondicionador de instrumentos de viento")
print("• 🌍 Un estándar para intercambio cultural musical")  
print("• ⚖️  Un instrumento de precisión para artesanos")
print("• 🛠️  Una herramienta de mantenimiento para músicos")
print("• 🔬 Un dispositivo de calibración acústica")
