# FastF1 Telemetry Analysis 🏁

Proyecto para explorar y analizar telemetrías de Fórmula 1 usando la librería FastF1.

## 🚀 Inicio Rápido

1. **Configurar el entorno:**
   ```bash
   make setup
   ```

2. **Ejecutar el análisis completo:**
   ```bash
   make run
   ```

3. **Ver los gráficos generados:**
   Los gráficos se guardan en la carpeta `plots/`

## 📋 Comandos Disponibles

| Comando | Descripción |
|---------|-------------|
| `make setup` | Crea el entorno virtual e instala dependencias |
| `make run` | Ejecuta el análisis completo |
| `make lap-comparison` | Compara vueltas más rápidas entre pilotos |
| `make telemetry-comparison` | Compara telemetría detallada |
| `make speed-analysis` | Análisis de velocidades |
| `make interactive` | Modo interactivo con IPython |
| `make download-data` | Descarga datos de ejemplo |
| `make clean` | Limpia archivos generados |
| `make clean-all` | Limpia todo incluyendo el entorno virtual |

## 📊 Tipos de Análisis

### 1. Comparación de Vueltas Más Rápidas
- Velocidad por distancia
- Aceleración vs distancia
- Frenado vs distancia  
- RPM vs distancia

### 2. Análisis de Telemetría Detallado
- Diferencias de velocidad entre pilotos
- Zonas donde cada piloto es más rápido
- Estadísticas comparativas

### 3. Análisis de Velocidades
- Velocidades máximas por piloto
- Velocidades promedio
- Distribución de velocidades

## 🛠️ Personalización

Puedes modificar los parámetros en `main.py`:

```python
# Configuración por defecto
year = 2024
event = 'Las Vegas'  # Cambiar por otro GP
drivers = ['VER', 'HAM', 'LEC']  # Códigos de pilotos
```

### Códigos de Pilotos Comunes
- VER - Max Verstappen
- HAM - Lewis Hamilton  
- LEC - Charles Leclerc
- SAI - Carlos Sainz
- NOR - Lando Norris
- PER - Sergio Pérez
- RUS - George Russell
- ALO - Fernando Alonso

### Eventos Disponibles (2024)
- Bahrain, Saudi Arabia, Australia, Japan, China
- Miami, Emilia Romagna, Monaco, Canada, Spain
- Austria, Britain, Hungary, Belgium, Netherlands
- Italy, Azerbaijan, Singapore, United States
- Mexico, Brazil, Las Vegas, Qatar, Abu Dhabi

## 📁 Estructura del Proyecto

```
fast_f1/
├── Makefile              # Comandos de automatización
├── main.py              # Script principal de análisis
├── requirements.txt     # Dependencias de Python
├── cache/              # Cache de datos de FastF1
└── plots/              # Gráficos generados
```

## 🔧 Requisitos

- Python 3.8+
- Conexión a internet (para descargar datos)
- ~500MB de espacio libre (para cache de datos)

## 💡 Consejos

1. **Primera ejecución**: Puede tardar varios minutos descargando datos
2. **Cache**: Los datos se almacenan en `cache/` para ejecuciones futuras
3. **Memoria**: Análisis de carreras completas pueden usar mucha RAM
4. **Internet**: Se requiere conexión para descargar nuevos datos

## 🐛 Solución de Problemas

### Error de conexión
```bash
# Descargar datos manualmente
make download-data
```

### Problemas de memoria
- Analiza qualifying en lugar de carrera
- Reduce el número de pilotos
- Usa menos puntos de datos

### Cache corrupto
```bash
make clean
make setup
```

## 📈 Ejemplos de Uso

### Comparar Hamilton vs Verstappen en Monaco
```python
compare_fastest_laps(year=2024, event='Monaco', drivers=['HAM', 'VER'])
```

### Análisis de velocidad de múltiples pilotos
```python
speed_analysis(year=2024, event='Monza', drivers=['VER', 'HAM', 'LEC', 'NOR'])
```

### Telemetría detallada
```python
compare_telemetry(year=2024, event='Silverstone', drivers=['RUS', 'HAM'])
```

## 📚 Recursos

- [FastF1 Documentation](https://docs.fastf1.dev/)
- [Matplotlib Gallery](https://matplotlib.org/stable/gallery/)
- [Formula 1 Official](https://www.formula1.com/)

---

¡Disfruta explorando los datos de F1! 🏎️💨