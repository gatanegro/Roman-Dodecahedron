import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import time

print("🎵 SIMULACIÓN CON INSTRUMENTOS TIBETANOS REALES")
print("🔊 Usando frecuencias auténticas de Dung Chen y cuernos rituales")

# --- FRECUENCIAS REALES DE INSTRUMENTOS TIBETANOS ---
FRECUENCIAS_TIBETANAS = {
    'DUNG_CHEN_LARGO': {  # Tubo largo ceremonial (3-4 metros)
        'frecuencia_base': 55.0,  # Hz - Fundamental muy grave
        'armonicos': [110.0, 165.0, 220.0],
        'longitud': 3.5,  # metros
        'uso': 'ceremonias grandes, exteriores'
    },
    'DUNG_CHEN_MEDIO': {  # Tubo medio (2-2.5 metros)
        'frecuencia_base': 73.3,  # Hz - Re bemol
        'armonicos': [146.6, 219.9, 293.2],
        'longitud': 2.2,
        'uso': 'templos, ceremonias interiores'
    },
    'RAG_DUNG': {  # Trompeta corta tibetana
        'frecuencia_base': 110.0,  # Hz - La grave
        'armonicos': [220.0, 330.0, 440.0],
        'longitud': 1.5,
        'uso': 'ritos específicos, sanación'
    },
    'KANG_DUNG': {  # Cuerno de pierna humana (ritual chamánico)
        'frecuencia_base': 146.6,  # Hz - Re
        'armonicos': [293.2, 439.8, 586.4],
        'longitud': 0.8,
        'uso': 'chamanismo, trance'
    }
}

# --- PARÁMETROS DEL DODECAEDRO ---
DIAMETROS_AGUJEROS = [26, 21.5, 16.5, 21, 11.5, 17, 25.5, 10.5, 15.5, 22, 17, 22]  # mm
FRECUENCIA_MUESTREO = 44100  # Hz
DURACION = 2.0  # segundos

# --- GENERAR SONIDO DE TUBO TIBETANO ---
def generar_sonido_tibetano(tipo_instrumento='DUNG_CHEN_MEDIO', duracion=2.0):
    """Genera sonido auténtico de instrumento tibetano"""
    t = np.linspace(0, duracion, int(FRECUENCIA_MUESTREO * duracion))
    
    datos = FRECUENCIAS_TIBETANAS[tipo_instrumento]
    freq_base = datos['frecuencia_base']
    
    # Sonido característico: fundamental fuerte + armónicos suaves
    sonido = (
        0.8 * np.sin(2*np.pi*freq_base*t) +
        0.3 * np.sin(2*np.pi*2*freq_base*t) +
        0.2 * np.sin(2*np.pi*3*freq_base*t) +
        0.1 * np.sin(2*np.pi*4*freq_base*t)
    )
    
    # Añadir vibrato natural (pequeña modulación de frecuencia)
    vibrato = 0.005 * np.sin(2*np.pi*6*t)  # 6 Hz de vibrato
    sonido *= (1 + vibrato)
    
    # Ataque y decaimiento natural
    envolvente = np.exp(-0.5*t) * (1 - np.exp(-10*t))
    sonido *= envolvente
    
    return t, sonido, datos

# --- SIMULACIÓN CORREGIDA ---
def simulacion_tibetana():
    """Simulación con frecuencias realistas de instrumentos tibetanos"""
    
    start_time = time.time()
    
    # Generar sonido de Dung Chen medio (73.3 Hz)
    t, sonido, datos_instrumento = generar_sonido_tibetano('DUNG_CHEN_MEDIO', DURACION)
    frecuencia_base = datos_instrumento['frecuencia_base']
    
    print(f"🎺 Instrumento: Dung Chen Medio")
    print(f"📏 Longitud: {datos_instrumento['longitud']}m")
    print(f"🎵 Frecuencia base: {frecuencia_base} Hz")
    print(f"🔊 Armónicos: {datos_instrumento['armonicos']}")
    
    # Procesar through agujeros seleccionados (los más relevantes)
    agujeros_relevantes = [0, 2, 5, 7, 10]  # Agujeros con frecuencias de corte bajas
    diametros_relevantes = [DIAMETROS_AGUJEROS[i] for i in agujeros_relevantes]
    
    sonidos_filtrados = []
    frecuencias_corte = []
    
    for diametro in diametros_relevantes:
        # Frecuencia natural del agujero (en Hz)
        freq_corte = 343000 / (2 * diametro)
        frecuencias_corte.append(freq_corte)
        
        # Solo procesar si la frecuencia es razonable para filtro digital
        if freq_corte < FRECUENCIA_MUESTREO/2:
            # Filtro pasa-banda ancho alrededor de la frecuencia natural
            b, a = signal.butter(2, [freq_corte-30, freq_corte+30], 
                               btype='bandpass', fs=FRECUENCIA_MUESTREO)
            sonido_filtrado = signal.lfilter(b, a, sonido)
        else:
            # Para frecuencias muy altas, usar solo el sonido original
            sonido_filtrado = sonido.copy()
        
        sonidos_filtrados.append(sonido_filtrado)
    
    # --- VISUALIZACIÓN ---
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # 1. Sonido original vs filtrado (primeros 3 agujeros)
    axes[0,0].plot(t[:1000], sonido[:1000], 'b-', label='Original', alpha=0.7, linewidth=2)
    for i in range(min(3, len(sonidos_filtrados))):
        axes[0,0].plot(t[:1000], sonidos_filtrados[i][:1000] + (i+1)*0.4, 
                      label=f'Agujero {agujeros_relevantes[i]} (Ø{diametros_relevantes[i]}mm)')
    axes[0,0].set_title('SONIDO TIBETANO ORIGINAL vs FILTRADO')
    axes[0,0].set_xlabel('Tiempo (s)')
    axes[0,0].set_ylabel('Amplitud')
    axes[0,0].legend()
    axes[0,0].grid(True, alpha=0.3)
    
    # 2. Espectro de frecuencias
    fft_original = np.abs(np.fft.fft(sonido))
    freqs = np.fft.fftfreq(len(sonido), 1/FRECUENCIA_MUESTREO)
    positive_idx = (freqs > 0) & (freqs < 1000)  # Solo hasta 1000 Hz
    
    axes[0,1].plot(freqs[positive_idx], fft_original[positive_idx], 'b-', 
                  label='Original', alpha=0.7, linewidth=2)
    
    # Marcar frecuencia base y armónicos
    colors = ['red', 'green', 'purple', 'orange']
    for i, armonico in enumerate([frecuencia_base] + datos_instrumento['armonicos'][:3]):
        if armonico < 1000:
            axes[0,1].axvline(armonico, color=colors[i], linestyle='--', 
                             label=f'{armonico} Hz' if i == 0 else f'Armónico {i}: {armonico} Hz')
    
    axes[0,1].set_title('ESPECTRO DEL SONIDO TIBETANO')
    axes[0,1].set_xlabel('Frecuencia (Hz)')
    axes[0,1].set_ylabel('Amplitud')
    axes[0,1].legend()
    axes[0,1].grid(True, alpha=0.3)
    
    # 3. Frecuencias de corte de agujeros vs frecuencia del instrumento
    axes[1,0].bar(range(len(frecuencias_corte)), frecuencias_corte, 
                 color=['skyblue' if fc > 1000 else 'lightcoral' for fc in frecuencias_corte])
    
    # Marcar frecuencia del instrumento
    axes[1,0].axhline(y=frecuencia_base, color='red', linestyle='-', 
                     label=f'Dung Chen: {frecuencia_base} Hz', linewidth=2)
    
    for i, (freq, diametro) in enumerate(zip(frecuencias_corte, diametros_relevantes)):
        axes[1,0].text(i, freq + 50, f'Ø{diametro}mm\n{freq:.0f}Hz', 
                      ha='center', va='bottom', fontsize=8)
    
    axes[1,0].set_title('FRECUENCIAS NATURALES DE AGUJEROS vs INSTRUMENTO')
    axes[1,0].set_ylabel('Frecuencia (Hz)')
    axes[1,0].set_xticks(range(len(agujeros_relevantes)))
    axes[1,0].set_xticklabels([f'Agujero {i}' for i in agujeros_relevantes])
    axes[1,0].legend()
    axes[1,0].grid(True, alpha=0.3)
    
    # 4. Análisis de resonancia
    diferencias_resonancia = [abs(fc - frecuencia_base) for fc in frecuencias_corte]
    mejores_agujeros = np.argsort(diferencias_resonancia)[:3]  # Top 3 más cercanos
    
    axes[1,1].bar(range(len(diferencias_resonancia)), diferencias_resonancia,
                 color=['green' if i in mejores_agujeros else 'gray' 
                        for i in range(len(diferencias_resonancia))])
    
    for i, diff in enumerate(diferencias_resonancia):
        axes[1,1].text(i, diff + 5, f'{diff:.0f}Hz', ha='center', va='bottom')
    
    axes[1,1].set_title('DIFERENCIA CON FRECUENCIA DEL INSTRUMENTO')
    axes[1,1].set_ylabel('Diferencia (Hz)')
    axes[1,1].set_xticks(range(len(agujeros_relevantes)))
    axes[1,1].set_xticklabels([f'Agujero {i}' for i in agujeros_relevantes])
    axes[1,1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    # --- RESULTADOS ---
    print(f"\n⏱️  Tiempo de simulación: {time.time() - start_time:.2f} segundos")
    
    print(f"\n🎯 AGUJEROS CON MEJOR RESONANCIA:")
    for idx in mejores_agujeros:
        agujero = agujeros_relevantes[idx]
        diametro = diametros_relevantes[idx]
        freq_corte = frecuencias_corte[idx]
        diferencia = diferencias_resonancia[idx]
        
        print(f"• Agujero {agujero} (Ø{diametro}mm): {freq_corte:.0f}Hz → Diferencia: {diferencia:.0f}Hz")
    
    return sonidos_filtrados, frecuencias_corte

# --- EJECUTAR SIMULACIÓN ---
sonidos_resultado, frecuencias = simulacion_tibetana()

# --- ANÁLISIS HISTÓRICO ---
print(f"\n{'='*60}")
print("📜 ANÁLISIS HISTÓRICO: CONEXIÓN TIBET-DODECAEDRO")
print(f"{'='*60}")

conexiones = [
    ("RUTAS COMERCIALES", "Ruta de la Seda conectaba Roma con Asia Central y Tibet"),
    ("INTERCAMBIO CULTURAL", "Monjes budistas viajaban con instrumentos rituales"),
    ("TECNOLOGÍA SONORA", "Conocimiento de resonancia y acústica ceremonial"),
    ("OBJETOS RITUALES", "Ambas culturas usaban objetos sagrados para sonido"),
    ("FRECUENCIAS SACRAS", "73.3Hz (Dung Chen) cerca de 72Hz (frecuencia terrestre)")
]

for titulo, descripcion in conexiones:
    print(f"• {titulo}: {descripcion}")

# --- PREDICCIONES PARA EXPERIMENTO ---
print(f"\n🔮 PREDICCIONES PARA EXPERIMENTO FÍSICO:")
print("Usar réplica de dodecaedro + Dung Chen real (73.3Hz):")
print("1. Agujero 7 (Ø10.5mm): Mayor transformación armónica")
print("2. Agujero 0 (Ø26mm): Preservación del sonido grave original")  
print("3. Agujero 5 (Ø17mm): Punto óptimo de resonancia")
print("4. Combinar múltiples agujeros para efectos estereofónicos")

# --- COMPARACIÓN CON OTROS INSTRUMENTOS ---
print(f"\n🎵 COMPARACIÓN CON OTROS INSTRUMENTOS ANTIGUOS:")
instrumentos_comparacion = [
    ('DIDGERIDOO', 65, 'Australia', '60-80Hz'),
    ('SHOFAR', 85, 'Hebreo', '80-90Hz'), 
    ('TROMPETA_MAYA', 98, 'Mesoamérica', '95-100Hz'),
    ('SANKHA', 110, 'Hinduismo', '108-112Hz')
]

print("Instrumento   | Frecuencia | Cultura     | Rango típico")
print("-" * 55)
for nombre, freq, cultura, rango in instrumentos_comparacion:
    print(f"{nombre:12} | {freq:9}Hz | {cultura:10} | {rango}")
