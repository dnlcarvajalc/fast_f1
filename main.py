#!/usr/bin/env python3
"""
FastF1 Telemetry Analysis - Main Script
Análisis de telemetrías de Fórmula 1 usando FastF1

Este script proporciona funciones para analizar y comparar datos de telemetría
entre pilotos de Fórmula 1.
"""

import fastf1
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from pathlib import Path
import warnings

# Configuración
warnings.filterwarnings('ignore')
plt.style.use('seaborn-v0_8')
fastf1.Cache.enable_cache('cache')

# Crear directorio para gráficos
Path('plots').mkdir(exist_ok=True)

def setup_session(year=2024, event='Las Vegas', session_type='R'):
    """
    Configura y carga una sesión de F1

    Args:
        year (int): Año de la temporada
        event (str): Nombre del Gran Premio
        session_type (str): Tipo de sesión ('R'=Race, 'Q'=Qualifying, 'FP1', etc.)

    Returns:
        fastf1.core.Session: Sesión cargada
    """
    print(f"📡 Cargando sesión: {year} {event} - {session_type}")
    session = fastf1.get_session(year, event, session_type)
    session.load()
    print("✅ Sesión cargada exitosamente")
    return session

def get_driver_data(session, driver_codes):
    """
    Obtiene datos de telemetría para los pilotos especificados

    Args:
        session: Sesión de FastF1
        driver_codes (list): Lista de códigos de pilotos (ej: ['HAM', 'VER'])

    Returns:
        dict: Diccionario con datos de cada piloto
    """
    drivers_data = {}

    for driver in driver_codes:
        try:
            # Obtener vuelta más rápida del piloto
            fastest_lap = session.laps.pick_driver(driver).pick_fastest()
            if fastest_lap.empty:
                print(f"⚠️  No se encontraron datos para {driver}")
                continue

            # Obtener telemetría
            telemetry = fastest_lap.get_telemetry()

            drivers_data[driver] = {
                'lap': fastest_lap,
                'telemetry': telemetry,
                'lap_time': fastest_lap['LapTime'],
                'driver_info': session.get_driver(driver)
            }

            print(f"✅ Datos cargados para {driver} - Tiempo: {fastest_lap['LapTime']}")

        except Exception as e:
            print(f"❌ Error cargando datos de {driver}: {str(e)}")

    return drivers_data

def compare_fastest_laps(year=2024, event='Las Vegas', drivers=['HAM', 'VER']):
    """
    Compara las vueltas más rápidas entre pilotos
    """
    print(f"\n🏁 Comparando vueltas más rápidas: {' vs '.join(drivers)}")

    # Cargar sesión
    session = setup_session(year, event, 'Q')  # Qualifying para mejores tiempos

    # Obtener datos
    drivers_data = get_driver_data(session, drivers)

    if len(drivers_data) < 2:
        print("❌ No hay suficientes datos de pilotos para comparar")
        return

    # Crear gráfico de comparación de tiempos por vuelta
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle(f'Comparación de Telemetría - {event} {year}', fontsize=16, fontweight='bold')

    # Colores para cada piloto
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57']

    for i, (driver, data) in enumerate(drivers_data.items()):
        telemetry = data['telemetry']
        color = colors[i % len(colors)]

        # Velocidad vs Distancia
        axes[0, 0].plot(telemetry['Distance'], telemetry['Speed'], 
                       label=f"{driver} ({data['lap_time']})", 
                       color=color, linewidth=2)

        # Aceleración vs Distancia
        axes[0, 1].plot(telemetry['Distance'], telemetry['Throttle'], 
                       label=driver, color=color, linewidth=2)

        # Frenado vs Distancia
        axes[1, 0].plot(telemetry['Distance'], telemetry['Brake'], 
                       label=driver, color=color, linewidth=2)

        # RPM vs Distancia
        axes[1, 1].plot(telemetry['Distance'], telemetry['RPM'], 
                       label=driver, color=color, linewidth=2)

    # Configurar subgráficos
    axes[0, 0].set_title('Velocidad por Distancia')
    axes[0, 0].set_xlabel('Distancia (m)')
    axes[0, 0].set_ylabel('Velocidad (km/h)')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)

    axes[0, 1].set_title('Aceleración por Distancia')
    axes[0, 1].set_xlabel('Distancia (m)')
    axes[0, 1].set_ylabel('Aceleración (%)')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)

    axes[1, 0].set_title('Frenado por Distancia')
    axes[1, 0].set_xlabel('Distancia (m)')
    axes[1, 0].set_ylabel('Frenado (%)')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)

    axes[1, 1].set_title('RPM por Distancia')
    axes[1, 1].set_xlabel('Distancia (m)')
    axes[1, 1].set_ylabel('RPM')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'plots/fastest_laps_comparison_{event}_{year}.png', dpi=300, bbox_inches='tight')
    plt.show()

    print(f"💾 Gráfico guardado en plots/fastest_laps_comparison_{event}_{year}.png")

def compare_telemetry(year=2024, event='Las Vegas', drivers=['HAM', 'VER']):
    """
    Análisis detallado de telemetría entre pilotos
    """
    print(f"\n📊 Análisis detallado de telemetría: {' vs '.join(drivers)}")

    session = setup_session(year, event, 'Q')
    drivers_data = get_driver_data(session, drivers)

    if len(drivers_data) < 2:
        print("❌ No hay suficientes datos de pilotos para comparar")
        return

    # Crear gráfico de diferencias
    fig, ax = plt.subplots(figsize=(12, 8))

    # Tomar dos pilotos para comparación directa
    driver1, driver2 = list(drivers_data.keys())[:2]
    tel1 = drivers_data[driver1]['telemetry']
    tel2 = drivers_data[driver2]['telemetry']

    # Interpolar datos para que tengan la misma longitud
    min_distance = min(tel1['Distance'].max(), tel2['Distance'].max())
    distance_common = np.linspace(0, min_distance, 1000)

    speed1_interp = np.interp(distance_common, tel1['Distance'], tel1['Speed'])
    speed2_interp = np.interp(distance_common, tel2['Distance'], tel2['Speed'])

    # Diferencia de velocidad
    speed_diff = speed1_interp - speed2_interp

    # Crear gráfico
    ax.plot(distance_common, speed_diff, linewidth=3, color='red')
    ax.axhline(y=0, color='black', linestyle='--', alpha=0.5)
    ax.fill_between(distance_common, 0, speed_diff, 
                   where=(speed_diff > 0), alpha=0.3, color='green', 
                   label=f'{driver1} más rápido')
    ax.fill_between(distance_common, 0, speed_diff, 
                   where=(speed_diff < 0), alpha=0.3, color='red', 
                   label=f'{driver2} más rápido')

    ax.set_title(f'Diferencia de Velocidad: {driver1} vs {driver2}\n{event} {year}', 
                fontsize=14, fontweight='bold')
    ax.set_xlabel('Distancia (m)')
    ax.set_ylabel('Diferencia de Velocidad (km/h)')
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'plots/telemetry_comparison_{driver1}_vs_{driver2}_{event}_{year}.png', 
                dpi=300, bbox_inches='tight')
    plt.show()

    # Estadísticas
    print(f"\n📈 Estadísticas de comparación:")
    print(f"  {driver1}: {drivers_data[driver1]['lap_time']}")
    print(f"  {driver2}: {drivers_data[driver2]['lap_time']}")
    print(f"  Diferencia promedio de velocidad: {np.mean(np.abs(speed_diff)):.2f} km/h")
    print(f"  Máxima ventaja de {driver1}: {np.max(speed_diff):.2f} km/h")
    print(f"  Máxima ventaja de {driver2}: {np.abs(np.min(speed_diff)):.2f} km/h")

def speed_analysis(year=2024, event='Las Vegas', drivers=['HAM', 'VER', 'LEC']):
    """
    Análisis de velocidades máximas y mínimas
    """
    print(f"\n🏎️  Análisis de velocidades: {', '.join(drivers)}")

    session = setup_session(year, event, 'Q')
    drivers_data = get_driver_data(session, drivers)

    if not drivers_data:
        print("❌ No hay datos de pilotos disponibles")
        return

    # Recopilar estadísticas de velocidad
    speed_stats = []

    for driver, data in drivers_data.items():
        telemetry = data['telemetry']
        stats = {
            'Driver': driver,
            'Max_Speed': telemetry['Speed'].max(),
            'Min_Speed': telemetry['Speed'].min(),
            'Avg_Speed': telemetry['Speed'].mean(),
            'Lap_Time': str(data['lap_time'])
        }
        speed_stats.append(stats)

    # Crear DataFrame
    df_stats = pd.DataFrame(speed_stats)

    # Crear gráficos
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    # Velocidades máximas
    bars1 = axes[0].bar(df_stats['Driver'], df_stats['Max_Speed'], 
                       color=['#FF6B6B', '#4ECDC4', '#45B7D1'][:len(df_stats)])
    axes[0].set_title('Velocidad Máxima por Piloto')
    axes[0].set_ylabel('Velocidad (km/h)')

    # Añadir valores en las barras
    for bar, value in zip(bars1, df_stats['Max_Speed']):
        axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                    f'{value:.1f}', ha='center', va='bottom')

    # Velocidades promedio
    bars2 = axes[1].bar(df_stats['Driver'], df_stats['Avg_Speed'], 
                       color=['#FECA57', '#FF9FF3', '#54A0FF'][:len(df_stats)])
    axes[1].set_title('Velocidad Promedio por Piloto')
    axes[1].set_ylabel('Velocidad (km/h)')

    for bar, value in zip(bars2, df_stats['Avg_Speed']):
        axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                    f'{value:.1f}', ha='center', va='bottom')

    # Distribución de velocidades
    for i, (driver, data) in enumerate(drivers_data.items()):
        axes[2].hist(data['telemetry']['Speed'], alpha=0.6, 
                    label=driver, bins=30, color=['#FF6B6B', '#4ECDC4', '#45B7D1'][i])

    axes[2].set_title('Distribución de Velocidades')
    axes[2].set_xlabel('Velocidad (km/h)')
    axes[2].set_ylabel('Frecuencia')
    axes[2].legend()

    plt.tight_layout()
    plt.savefig(f'plots/speed_analysis_{event}_{year}.png', dpi=300, bbox_inches='tight')
    plt.show()

    # Mostrar tabla de estadísticas
    print(f"\n📊 Estadísticas de velocidad:")
    print(df_stats.to_string(index=False))

def main():
    """
    Función principal que ejecuta todos los análisis
    """
    print("🏁 FastF1 Telemetry Analysis")
    print("=" * 50)

    # Configuración por defecto
    year = 2024
    event = 'Las Vegas'  # Último GP del calendario 2024
    drivers = ['VER', 'HAM', 'LEC']  # Pilotos a comparar

    print(f"🎯 Configuración del análisis:")
    print(f"   Año: {year}")
    print(f"   Gran Premio: {event}")
    print(f"   Pilotos: {', '.join(drivers)}")
    print()

    try:
        # Ejecutar análisis
        compare_fastest_laps(year, event, drivers)
        compare_telemetry(year, event, drivers[:2])  # Solo dos para comparación directa
        speed_analysis(year, event, drivers)

        print("\n✅ Análisis completado exitosamente!")
        print("📁 Revisa la carpeta 'plots' para ver los gráficos generados")

    except Exception as e:
        print(f"❌ Error durante el análisis: {str(e)}")
        print("💡 Sugerencias:")
        print("   - Verifica tu conexión a internet")
        print("   - Prueba con un evento diferente")
        print("   - Asegúrate de que los códigos de pilotos sean correctos")

if __name__ == "__main__":
    main()