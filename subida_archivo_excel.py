# import pandas as pd
# import mysql.connector
# from mysql.connector import Error

# def create_connection():
#     try:
#         connection = mysql.connector.connect(
#             host="localhost",  
#             user="root",  
#             password="",  
#             database="data_analys"  
#         )
#         if connection.is_connected():
#             print("Conexión exitosa a la base de datos")
#             return connection
#     except Error as e:
#         print(f"Error al conectar: {e}")
#         return None

# def close_connection(connection):
#     if connection and connection.is_connected():
#         connection.close()
#         print("Conexión cerrada.")

# def upload_data_from_excel(file_path):
#     df = pd.read_excel(file_path)

#     connection = create_connection()
#     if connection is None:
#         return

#     cursor = connection.cursor()

#     for index, row in df.iterrows():
#         try:
#             query = """
#                 INSERT INTO sales_data (numero_personas, generos, item_name, item_type, item_price, quantity, transaction_amount, transaction_type, date, time_of_sale)
#                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#             """
#             values = (
#                 row['numero personas'], 
#                 row['generos'],
#                 row['item_name'],
#                 row['item_type'],
#                 row['item_price'],
#                 row['quantity'],
#                 row['transaction_amount'],
#                 row['transaction_type'],
#                 row['date'],
#                 row['time_of_sale']
#             )
#             cursor.execute(query, values)
#             connection.commit()  

#             print(f"Fila {index + 1} insertada correctamente.")

#         except Error as e:
#             print(f"Error al insertar la fila {index + 1}: {e}")
#             connection.rollback()  

#     cursor.close()
#     close_connection(connection)

# if __name__ == "__main__":
#     file_path = 'Balaji-Fast-Food-Sales.xlsx'
#     upload_data_from_excel(file_path)
