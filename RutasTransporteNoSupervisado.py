"""
Creado por:
    IdBanner:100098659
    Nombre: Esperanza Castro Lombana 

    IdBanner:100096167
    Nombre: Jeison Valencia Sanchez

    Fecha: 2024-04-02, ©/ todos los derechos reservados
    Corporación Universitaria Iberoamericana

    Identifique y describa fuentes de datos relacionadas con el proyecto del transporte masivo propuesto en las actividades anteriores,
    con el fin de desarrollar modelos de aprendizaje no supervisado. En caso de no existir dichas fuentes de datos, desarrolle un dataset 
    con una muestra de dichos datos.
"""
# Bibliotecas utilizadas
import pandas as pd #Biblioteca manejo de dataframe
from sklearn.cluster import KMeans #Biblioteca para el modelo no supervisado
import matplotlib.pyplot as plt #Biblioteca para graficar los datos 


# Diccionario con datos de paradas del sistema de transporte público
paradas = {
    "Bello":    {"latitud": 6.330097700334223, "longitud": -75.55363508182953},
    "Madera":   {"latitud": 6.315876875242534, "longitud": -75.55532449039737},
    "Centromed":{"latitud": 6.247194543362567, "longitud": -75.56970340757249},
    "Poblado":  {"latitud": 6.212178340280529, "longitud": -75.5780956618959},
    "Itagui":   {"latitud": 6.1628939869412305, "longitud": -75.60686324893409},
    "Sabaneta": {"latitud": 6.157689019859837, "longitud": -75.61624238236156},
    "Estrella": {"latitud": 6.15278426423037, "longitud": -75.62636321936311}
}


# Funciona para anlizar los datos iniciales
def GraficaDatosIniciales():
    # Convertir diccionario a DataFrame
    paradas_df = pd.DataFrame(paradas).transpose()

    # Agregar columna de nombres para etiquetas
    paradas_df["Nombre"] = paradas_df.index

    # Graficar los puntos en un mapa
    plt.scatter(paradas_df["latitud"], paradas_df["longitud"])

    # Agregar etiquetas a los puntos
    for i in range(len(paradas_df)):
        plt.annotate(paradas_df["Nombre"][i], (paradas_df["latitud"][i], paradas_df["longitud"][i]))

    # Ajustar el título y los ejes
    plt.title("Mapa de paradas")
    plt.xlabel("Longitud")
    plt.ylabel("Latitud")

    # Mostrar el mapa
    plt.show()


# Convertir diccionario a DataFrame
df_paradas = pd.DataFrame(paradas).transpose()


# Elegir el número de clusters (rutas)
k = 3

# Aplicamos el algoritmo no supervisado de clusterización de Kmeans
kmeans = KMeans(n_clusters=k)
kmeans.fit(df_paradas)

# Etiquetas de las rutas para cada parada
etiquetas_rutas = kmeans.labels_

# funcion que grafica los clusters mas cercanos para el modelo
def GraficaModeloKmeans():
    colores = ["r", "g", "b"]

    for i in range(k):
        plt.scatter(df_paradas[etiquetas_rutas == i].iloc[:, 0], df_paradas[etiquetas_rutas == i].iloc[:, 1], c=colores[i], label="Ruta " + str(i+1))
    plt.legend()
    plt.show()


# Función para obtener la ruta para un origen y destino
def obtener_ruta(origen, destino):
    # Encontrar la ruta del origen
    ruta_origen = etiquetas_rutas[df_paradas.index == origen]

    # Encontrar la ruta del destino
    ruta_destino = etiquetas_rutas[df_paradas.index == destino]

    # Si las rutas son iguales, no hay cambio de ruta
    if ruta_origen == ruta_destino:
        return "Sin cambio de ruta"

    # Si las rutas son diferentes, encontrar la parada de intersección
    parada_interseccion = df_paradas[etiquetas_rutas == ruta_origen].index[0]
    for i in range(len(df_paradas)):
        if etiquetas_rutas[i] == ruta_destino and df_paradas.index[i] != parada_interseccion:
            parada_interseccion = df_paradas.index[i]
            break

    # Ruta: Origen -> Parada de intersección -> Destino
    return f"{origen} -> {parada_interseccion} -> {destino}"


# Le mostramos al usuario las estaciones disponibles del transporte masivo
print("""--==========Bienvenido Al Transporte Masivo BUSMED==========--
Actual mentes el transporte cuenta con las siguientes estaciones:""")
for Estaciones in df_paradas.index:
    print(f"Estacione: {Estaciones}")


print("\n")
# Validamos que el usuario ingrese las estaciones de origen y fin correctamente
while True:    
    EstacionA = str(input("Ingrese la estacion de inicio: "))
    EstacionB = str(input("Ingrese la estacion final: "))

    EstacionInicio = EstacionA.title().lstrip().rstrip()
    EstacionFinal = EstacionB.title().lstrip().rstrip()

    if EstacionInicio not in df_paradas.index:
        print ("La estacion de inicio no corresponde con una estacion valida del sistema BUSMED")  
    elif EstacionFinal not in df_paradas.index:
        print ("La estacion de destino no corresponde con una estacion valida del sistema BUSMED")            
    else:
        break

# Ejecutamos la funcion
ruta = obtener_ruta(EstacionInicio, EstacionFinal)

# Mostramos los datos graficos inciales
GraficaDatosIniciales()

# Ejecutamos los print para verificar por cuales estaciones se debe pasar para llegar desde punto inicial al punto final 
print("\n"f"""El camino mas corto desde la estacion: "{EstacionInicio}" hasta la estacion: "{EstacionFinal}" es:\n{ruta} """)

# Mostramos los graficos del modelo
GraficaModeloKmeans()