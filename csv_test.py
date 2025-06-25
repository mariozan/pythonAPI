import pandas as pd # Libreria para analizar datos
import matplotlib.pyplot as plt # Libreria para pintar

# Leyendo el archivo
df = pd.read_csv('https://drive.google.com/uc?id=107Sqmt1sk6oGcKL_TwNVqz5wMJBavsoq&export=download')

# print(df.head()) # Imprime los primeros datos
# print(df.info()) # Imprime un resumen de los datos
# print(df.describe())

# Productos que valen menos de 100 dolares y que tengan menos de 200 en inventario
productos = df[(df["Price"] < 100) & (df["Stock"] < 200)]
print(productos[['Name', 'Price', 'Stock']])

# Obtener los productos de color blanco
# Color == "White"
color = df[df["Color"] == "White"]
print(color[["Name", "Color", "Brand"]])

# Promedio de precio por categoria ordenado de menor a mayor
promedioCategoria = df.groupby('Category')['Price'].mean().sort_values()
print(promedioCategoria)

# Promedio de inventario por marca
print("Promedio por marca", df.groupby('Brand')["Stock"].mean())

# Generando la grafica
promedioCategoria.plot()
plt.show()