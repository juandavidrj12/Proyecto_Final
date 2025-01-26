from flask import Flask, render_template
import mysql.connector
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

app = Flask(__name__)

def create_connection():
    return mysql.connector.connect(
        host="bfzxn4mib0ktpcc7g7d3-mysql.services.clever-cloud.com",  
        user="uem55h8erytdyetb",  
        password="WtXJpm6f4zhb5Y2rnyXW",  
        database="bfzxn4mib0ktpcc7g7d3" 
    )

# Función para obtener los datos de la base de da   tos
def get_sales_data():
    connection = create_connection()
    query = "SELECT * FROM sales_data" 
    df = pd.read_sql(query, connection)
    connection.close()
    return df

@app.route('/')
def index():
    # Obtener los datos de ventas
    df = get_sales_data()

    # Gráfico 1: Comparar ventas de "Fastfood" y "Beverages"
    sales_comparison = df.groupby('item_type')['transaction_amount'].sum().reset_index()
    fig1 = px.bar(
        sales_comparison,
        x='transaction_amount',
        y='item_type',
        orientation='h',
        title='Ventas por Tipo de Producto',
        labels={'transaction_amount': 'Monto de Transacción', 'item_type': 'Tipo de Producto'}
    )

    # Gráfico 2: Ventas por nombre de producto
    item_sales = df.pivot_table(
        values='transaction_amount',
        index='item_type',
        columns='item_name',
        aggfunc='sum'
    ).fillna(0)  # Rellenar valores nulos con 0
    fig2 = go.Figure()

    for item in item_sales.columns:
        fig2.add_trace(go.Bar(
            x=item_sales.index,
            y=item_sales[item],
            name=item
        ))

    fig2.update_layout(
        barmode='stack',
        title="Ventas por Nombre de Producto",
        xaxis_title="Tipo de Producto",
        yaxis_title="Monto de Transacción",
        legend_title="Nombre de Producto"
    )

    # Gráfico 3: Ventas por Tipo de Transacción
    transaction_sales = df.groupby('transaction_type')['transaction_amount'].sum().reset_index()
    fig3 = px.bar(
        transaction_sales,
        x='transaction_amount',
        y='transaction_type',
        orientation='h',
        title='Ventas por Tipo de Transacción',
        labels={'transaction_amount': 'Monto de Transacción', 'transaction_type': 'Tipo de Transacción'}
    )

    # Calcular el tipo de transacción más usado (Cash o Online)
    most_used_transaction = df['transaction_type'].value_counts().idxmax()

    # Calcular Total de Ventas
    total_sales = df['transaction_amount'].sum()

    # Calcular los productos más vendidos
    top_selling_products = df.groupby('item_name')['transaction_amount'].sum().sort_values(ascending=False).head(3)
    top_selling_products_str = ', '.join(top_selling_products.index)

    # Convertir gráficos a HTML
    graph1_html = pio.to_html(fig1, full_html=False)
    graph2_html = pio.to_html(fig2, full_html=False)
    graph3_html = pio.to_html(fig3, full_html=False)

    # Pasar datos a la plantilla
    return render_template(
        'index.html', 
        graph1=graph1_html, 
        graph2=graph2_html,
        graph3=graph3_html,
        total_sales=total_sales, 
        top_selling_products=top_selling_products_str,
        most_used_transaction=most_used_transaction  # Añadir el tipo de transacción más usado
    )

@app.route("/genero")
def genero():
    # Conectar a la base de datos y obtener datos agrupados por género
    connection = create_connection()

    # Consulta para proporción de géneros
    gender_count_query = "SELECT generos AS gender, SUM(numero_personas) AS count FROM sales_data GROUP BY generos"
    df_gender_count = pd.read_sql(gender_count_query, connection)

    # Consulta para ventas totales por género
    gender_sales_query = """
        SELECT generos AS gender, SUM(transaction_amount) AS total_sales 
        FROM sales_data 
        GROUP BY generos
    """
    df_gender_sales = pd.read_sql(gender_sales_query, connection)

    # Consulta para gráfico de burbujas
    bubble_query = """
        SELECT generos AS gender, SUM(transaction_amount) AS total_sales, SUM(numero_personas) AS total_people 
        FROM sales_data 
        GROUP BY generos
    """
    df_bubble = pd.read_sql(bubble_query, connection)

    # Consulta para gráfico de líneas (ventas por hora y género)
    line_query = """
        SELECT time_of_sale, generos AS gender, SUM(transaction_amount) AS total_sales 
        FROM sales_data 
        GROUP BY time_of_sale, generos 
        ORDER BY time_of_sale
    """
    df_line = pd.read_sql(line_query, connection)

    connection.close()

    # Gráfico 1: Proporción de género (Gráfico de pastel)
    fig1 = px.pie(
        df_gender_count,
        names='gender',
        values='count',
        title="Proporción de Géneros",
        color_discrete_sequence=px.colors.sequential.RdBu
    )

    # Gráfico 2: Ventas totales por género (Gráfico de barras)
    fig2 = px.bar(
        df_gender_sales,
        x='gender',
        y='total_sales',
        title="Ventas Totales por Género",
        labels={'gender': 'Género', 'total_sales': 'Monto Total de Ventas'},
        color='gender'
    )

    # Gráfico 3: Gráfico de burbujas
    fig3 = px.scatter(
        df_bubble,
        x='gender',
        y='total_sales',
        size='total_people',
        color='gender',
        title="Relación de Ventas y Personas por Género",
        labels={'gender': 'Género', 'total_sales': 'Monto Total de Ventas', 'total_people': 'Número de Personas'}
    )

    # Gráfico 4: Gráfico de líneas (usando `time_of_sale`)
    fig4 = px.line(
        df_line,
        x='time_of_sale',
        y='total_sales',
        color='gender',
        title="Tendencias de Ventas por Género a lo Largo del Día",
        labels={'time_of_sale': 'Hora de la Venta', 'total_sales': 'Monto Total de Ventas', 'gender': 'Género'}
    )

    # Convertir gráficos a HTML
    graph1_html = pio.to_html(fig1, full_html=False)
    graph2_html = pio.to_html(fig2, full_html=False)
    graph3_html = pio.to_html(fig3, full_html=False)
    graph4_html = pio.to_html(fig4, full_html=False)

    # Renderizar la plantilla con los gráficos
    return render_template(
        'genero.html',
        graph1=graph1_html,
        graph2=graph2_html,
        graph3=graph3_html,
        graph4=graph4_html
    )

if __name__ == '__main__':
    app.run(debug=True)
