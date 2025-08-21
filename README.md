# YT_Analytics

Este proyecto está diseñado para recopilar y almacenar estadísticas diarias de canales de YouTube. Utiliza la API de YouTube Data v3 para obtener el número de reproducciones de videos subidos en los últimos días, diferenciando entre videos normales, "Shorts" y transmisiones en vivo.

## Características

- **Análisis Multi-Canal**: Permite configurar múltiples canales de YouTube para su análisis simultáneo.
- **Diferenciación de Tipos de Video**: Separa y cuenta visualizaciones para videos normales, YouTube Shorts y transmisiones en vivo.
- **Almacenamiento en CSV**: Guarda los resultados en un archivo CSV, añadiendo una nueva fila cada vez que se ejecuta el script.
- **Configuración por Variables de Entorno**: Utiliza un archivo `.env` para gestionar las claves de API y la configuración del análisis.
- **Optimización de Cuotas de API**: Implementa una estrategia eficiente para minimizar el consumo de cuotas de la API de Google.

## Requisitos Previos

- Python 3.6 o superior.
- Una clave de API de YouTube Data v3. Puedes obtener una siguiendo la [guía oficial de Google](https://developers.google.com/youtube/registering_an_application).

## Instalación

1. Clona este repositorio.
2. Crea un entorno virtual de Python:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Configuración

Crea un archivo llamado `.env` en el directorio raíz del proyecto con el siguiente contenido:

```env
# Clave de API de YouTube Data v3
YT_API = TU_CLAVE_DE_API_AQUI

# Mapa de canales a analizar en formato "nombre_canal1:ID_canal1,nombre_canal2:ID_canal2"
# El nombre del canal es un alias identificativo que tú defines.
YT_CHANNEL_MAP = "canal1:UCxxxxxxxxxxxxxxxxxxxxxx,canal2:UCyyyyyyyyyyyyyyyyyyyyyy"

# Número de días hacia atrás para analizar (por defecto es 1)
YT_DAYS_TO_ANALYZE = 1
```

**Ejemplo de archivo `.env`:**

```env
YT_API = 00000000000000000-aaaaaaaaaaaaaaa
YT_CHANNEL_MAP = "MiCanalFavorito:UC000000aaaaaa,OtroCanal:UC111111bbbbbbbbb"
YT_DAYS_TO_ANALYZE = 7
```

Para obtener el ID de un canal:
1. Ve a la página principal del canal en YouTube.
2. Haz clic con el botón derecho en el nombre del canal o en una zona vacía y selecciona "Ver código fuente de la página" o "Inspeccionar".
3. Busca "channelId" en el código fuente. El ID estará cerca, con el formato `UC...`.

## Uso

Ejecuta el script principal:

```bash
python main.py
```

El script realizará el análisis y agregará una nueva fila al archivo `youtube_analytics.csv` con la fecha actual y las estadísticas recopiladas.

## Estructura del Archivo de Salida (`youtube_analytics.csv`)

El archivo CSV generado tendrá las siguientes columnas:

- `Date`: Fecha de ejecución del análisis (formato YYYY-MM-DD).
- `ChannelName`: Nombre del canal (alias definido en `YT_CHANNEL_MAP`).
- `NORMAL_Count`: Número de videos normales subidos en el periodo analizado.
- `NORMAL_Views`: Suma total de reproducciones de los videos normales del periodo.
- `SHORT_Count`: Número de YouTube Shorts subidos en el periodo analizado.
- `SHORT_Views`: Suma total de reproducciones de los YouTube Shorts del periodo.
- `LIVE_Count`: Número de transmisiones en vivo subidas (como videos) en el periodo analizado.
- `LIVE_Views`: Suma total de reproducciones de las transmisiones en vivo del periodo.

## Dependencias

- `google-api-python-client`: Para interactuar con la API de YouTube.
- `pandas`: Para la manipulación y almacenamiento de datos en formato CSV.
- `python-dotenv`: Para cargar las variables de entorno desde el archivo `.env`.

## Licencia

Este proyecto es de código abierto y no tiene una licencia específica. Sentite libre de usarlo y modificarlo según tus necesidades.