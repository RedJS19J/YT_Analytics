"""
Script para generar un informe HTML con gráficas basado en los datos de youtube_analytics.csv
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from datetime import datetime

# --- CONFIGURACIÓN ---
CSV_FILE = 'youtube_analytics_7D.csv'
REPORT_FILE = 'youtube_analytics_report.html'

def load_and_prepare_data(csv_file_path):
    """Carga y prepara los datos del CSV para graficar."""
    if not os.path.exists(csv_file_path):
        raise FileNotFoundError(f"El archivo {csv_file_path} no se encontró. Ejecute main.py primero.")
    
    df = pd.read_csv(csv_file_path)
    
    # Convertir la columna 'Date' a tipo datetime para facilitar el filtrado y orden
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Ordenar por fecha para gráficos de series temporales
    df = df.sort_values(by='Date')
    
    print(f"Datos cargados. Total de registros: {len(df)}")
    print(f"Fechas disponibles: {df['Date'].min().date()} a {df['Date'].max().date()}")
    
    return df

def create_total_views_bar_chart(df):
    """Crea un gráfico de barras apiladas para vistas totales por canal y tipo."""
    # Agrupar por canal y sumar todas las vistas
    df_grouped = df.groupby('ChannelName').agg({
        'NORMAL_Views': 'sum',
        'SHORT_Views': 'sum',
        'LIVE_Views': 'sum'
    }).reset_index()
    
    # Usar Plotly Express para un gráfico de barras apiladas
    fig = px.bar(
        df_grouped,
        x='ChannelName',
        y=['NORMAL_Views', 'SHORT_Views', 'LIVE_Views'],
        title="Vistas Totales Acumuladas por Canal y Tipo de Video",
        labels={'value': 'Número de Vistas', 'variable': 'Tipo de Video'},
        color_discrete_map={
            'NORMAL_Views': '#636EFA', # Azul
            'SHORT_Views': '#EF553B',  # Rojo
            'LIVE_Views': '#00CC96'    # Verde
        }
    )
    
    fig.update_layout(
        xaxis_title="Canal",
        yaxis_title="Vistas Totales",
        legend_title_text='Tipo de Video',
        height=600
    )
    return fig

def create_avg_views_bar_chart(df):
    """Crea un gráfico de barras para el promedio de vistas por video por canal y tipo."""
    # Agrupar por canal y calcular el promedio ponderado
    df_grouped = df.groupby('ChannelName', group_keys=False).apply(
        lambda x: pd.Series({
            'NORMAL_Avg_Views_Per_Video': (x['NORMAL_Views'].sum() / x['NORMAL_Count'].sum()) if x['NORMAL_Count'].sum() > 0 else 0,
            'SHORT_Avg_Views_Per_Video': (x['SHORT_Views'].sum() / x['SHORT_Count'].sum()) if x['SHORT_Count'].sum() > 0 else 0,
            'LIVE_Avg_Views_Per_Video': (x['LIVE_Views'].sum() / x['LIVE_Count'].sum()) if x['LIVE_Count'].sum() > 0 else 0,
        }), include_groups=False
    ).reset_index()
    
    # Usar Plotly Express
    fig = px.bar(
        df_grouped,
        x='ChannelName',
        y=['NORMAL_Avg_Views_Per_Video', 'SHORT_Avg_Views_Per_Video', 'LIVE_Avg_Views_Per_Video'],
        title="Promedio de Vistas por Video por Canal y Tipo",
        labels={'value': 'Vistas Promedio por Video', 'variable': 'Tipo de Video'},
        color_discrete_map={
            'NORMAL_Avg_Views_Per_Video': '#636EFA',
            'SHORT_Avg_Views_Per_Video': '#EF553B',
            'LIVE_Avg_Views_Per_Video': '#00CC96'
        }
    )
    
    fig.update_layout(
        xaxis_title="Canal",
        yaxis_title="Vistas Promedio por Video",
        legend_title_text='Tipo de Video',
        height=600
    )
    return fig

def create_time_series_chart(df):
    """Crea un gráfico de líneas para la evolución de vistas por tipo a lo largo del tiempo."""
    # Agrupar por fecha y sumar todas las vistas de cada tipo
    df_time = df.groupby('Date').agg({
        'NORMAL_Views': 'sum',
        'SHORT_Views': 'sum',
        'LIVE_Views': 'sum'
    }).reset_index()
    
    # Usar Plotly Express
    fig = px.line(
        df_time,
        x='Date',
        y=['NORMAL_Views', 'SHORT_Views', 'LIVE_Views'],
        title="Evolución de Vistas Totales por Tipo de Video en el Tiempo",
        labels={'value': 'Número de Vistas', 'variable': 'Tipo de Video'},
        markers=True, # Añade marcadores a los puntos
        color_discrete_map={
            'NORMAL_Views': '#636EFA',
            'SHORT_Views': '#EF553B',
            'LIVE_Views': '#00CC96'
        }
    )
    
    fig.update_layout(
        xaxis_title="Fecha",
        yaxis_title="Vistas Totales",
        legend_title_text='Tipo de Video',
        height=600
    )
    return fig

def create_video_count_bar_chart(df):
    """Crea un gráfico de barras apiladas para la cantidad de videos por canal y tipo."""
    # Agrupar por canal y sumar todos los conteos
    df_grouped = df.groupby('ChannelName').agg({
        'NORMAL_Count': 'sum',
        'SHORT_Count': 'sum',
        'LIVE_Count': 'sum'
    }).reset_index()
    
    # Usar Plotly Express
    fig = px.bar(
        df_grouped,
        x='ChannelName',
        y=['NORMAL_Count', 'SHORT_Count', 'LIVE_Count'],
        title="Cantidad Total de Videos Subidos por Canal y Tipo",
        labels={'value': 'Número de Videos', 'variable': 'Tipo de Video'},
        color_discrete_map={
            'NORMAL_Count': '#636EFA',
            'SHORT_Count': '#EF553B',
            'LIVE_Count': '#00CC96'
        }
    )
    
    fig.update_layout(
        xaxis_title="Canal",
        yaxis_title="Cantidad de Videos",
        legend_title_text='Tipo de Video',
        height=600
    )
    return fig

def generate_html_report(figures, output_file):
    """Genera un archivo HTML que contiene todas las figuras."""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("<!DOCTYPE html>\n")
        f.write("<html>\n<head>\n")
        f.write("<title>Informe de Analítica de YouTube</title>\n")
        f.write("<style>\n")
        f.write("body { font-family: Arial, sans-serif; margin: 20px; }\n")
        f.write("h1, h2 { color: #333; }\n")
        f.write(".chart-container { margin-bottom: 40px; }\n")
        f.write("</style>\n")
        f.write("</head>\n<body>\n")
        f.write(f"<h1>Informe de Analítica de YouTube - Generado el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</h1>\n")
        
        # Cargar Plotly.js al inicio
        f.write("<script src='https://cdn.plot.ly/plotly-2.35.2.min.js'></script>\n")
        
        for i, (title, fig) in enumerate(figures):
            f.write(f"<div class='chart-container'>\n")
            f.write(f"<h2>{title}</h2>\n")
            # Convertir la figura directamente a HTML
            fig_html = fig.to_html(include_plotlyjs=False, full_html=False)
            f.write(fig_html)
            f.write("</div>\n")
        
        f.write("</body>\n</html>\n")
    
    print(f"Informe HTML generado: {output_file}")

def main():
    """Función principal para ejecutar el script."""
    print("Cargando datos...")
    df = load_and_prepare_data(CSV_FILE)
    
    if df.empty:
        print("No hay datos para generar el informe.")
        return

    print("Creando gráficos...")
    figures = []
    
    try:
        fig1 = create_total_views_bar_chart(df)
        figures.append(("Vistas Totales Acumuladas por Canal y Tipo de Video", fig1))
    except Exception as e:
        print(f"Error al crear el gráfico de vistas totales: {e}")

    try:
        fig2 = create_avg_views_bar_chart(df)
        figures.append(("Promedio de Vistas por Video por Canal y Tipo", fig2))
    except Exception as e:
        print(f"Error al crear el gráfico de vistas promedio: {e}")

    try:
        fig3 = create_time_series_chart(df)
        figures.append(("Evolución de Vistas Totales por Tipo de Video en el Tiempo", fig3))
    except Exception as e:
        print(f"Error al crear el gráfico de series temporales: {e}")

    try:
        fig4 = create_video_count_bar_chart(df)
        figures.append(("Cantidad Total de Videos Subidos por Canal y Tipo", fig4))
    except Exception as e:
        print(f"Error al crear el gráfico de conteo de videos: {e}")

    if not figures:
        print("No se pudieron crear gráficos.")
        return
        
    print("Generando informe HTML...")
    generate_html_report(figures, REPORT_FILE)
    print("¡Informe generado con éxito!")

if __name__ == "__main__":
    main()