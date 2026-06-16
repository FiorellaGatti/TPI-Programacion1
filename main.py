import csv
import os
def cargar_csv(nombre_archivo): #Función para leer el archivo csv y crear la lista de diccionarios
    base_dir = os.path.dirname(os.path.abspath(__file__)) #Obtenemos ruta al directorio del archivo siendo ejecutado (main.py)
    ruta = os.path.join(base_dir, nombre_archivo) #Arma ruta hacia el archivo csv pasado por parámetro
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:#abre el archivo en modo reader            
            lector_archivo = csv.DictReader(archivo) #Con DictReader crea un diccionario con el contenido del csv
            lista_paises=[]
            for fila in lector_archivo:#itera con un for el diccionario creado
                pais = { #Cada fila del diccionario inicial será un nuevo diccionario por país
                    "nombre": fila["nombre"],
                    "poblacion": int(fila["poblacion"]),#convierte los elementos de población y superficie a entero para poder utilizarlos luego
                    "superficie": int(fila["superficie"]),
                    "continente": fila["continente"]
                }
                lista_paises.append(pais)#agrega a la nueva lista el nuevo diccionario
        return lista_paises
    except FileNotFoundError: #Manejo de errores por archivo inexistente o si algún dato no pudo convertirse a entero
            print("El archivo que intenta abrir no existe")
    except ValueError:
            print("Error de formato en el CSV")
           
def agregar_pais(lista_paises):#Función para que el usuario pueda agregar un nuevo país
    """ Pedimos y validamos:
        -Nombres para: País, Continente.
        -Cantidades para: Población, Superficie"""
    try:
        nombre_pais = pedir_nombre("Ingrese el nombre del nuevo país: \n")
        poblacion = pedir_entero_positivo("Ingrese el número de la población de ese país: \n")
        superficie = pedir_entero_positivo("Ingrese el número de la superficie de ese país: \n")
        continente = pedir_nombre("Ingrese el continente del nuevo país: \n")
    except ValueError as e:
        print(f"Error: {e}")
    else:
        nuevo_pais = { #Crea diccionario del nuevo país con los datos ingresados por el usuario
            
            "nombre":nombre_pais,
            "poblacion":poblacion,
            "superficie":superficie,
            "continente":continente
        }
        lista_paises.append(nuevo_pais) #Agrega nuevo diccionario a la lista_paises
        print("Nuevo país agregado a la lista.")
    
def actualizar_pais(lista_paises):#Función para que el usuario actualice población y superficie de un país
    try:
        nombre = pedir_nombre("Ingrese el nombre del país que desea buscar: \n")
    except ValueError as e:
        print(f"Error: {e}")
    encontrado = False #declara bandera para verificar siel pais fue encontrada dentro de la lista y luego inicia ciclo for para recorrerla y buscarlo
    for fila in lista_paises:
        if nombre == fila['nombre'].capitalize().strip():
            encontrado = True#si encuentra el pais dentro de la lista, cambia bandera a true, la guarda en una nueva variable y rompe el ciclo para que no siga buscando innecesariamente
            pais_encontrado = fila
            break
    if encontrado: #si la bandera es True, pide datos para actualizar población y superficie
        try:
            superficie = pedir_entero_positivo("Ingrese el nuevo valor de superficie: \n")
            poblacion = pedir_entero_positivo("Ingrese el nuevo valor de poblacion: \n")
        except ValueError as e:
            print(f"Error: {e}")
        pais_encontrado["superficie"] = superficie
        pais_encontrado["poblacion"] = poblacion
        print(f"Pais actualizado, nueva superficie: {pais_encontrado['superficie']}, nueva población: {pais_encontrado['poblacion']}")
    else:#De lo contrario, muestra que el pais no está en la lista.
        print("El pais no se encuentra en la lista.")

def buscar_pais(lista_paises):#Función para que el usuario busque un país en la lista
    try:
        nombre = pedir_nombre("Ingrese el nombre o parte del nombre del país que desea buscar: \n")
    except ValueError as e:
        print(f"Error: {e}")
    encontrado = False #declara bandera para verificar si el país fue encontrada dentro de la lista y luego inicia ciclo for para recorrerla y buscarlo
    for fila in lista_paises:
        if nombre in fila['nombre'].capitalize().strip():#si encuentra coincidencia parcial o exacta, las muestra y cambia bandera a True
            encontrado = True
            print(f"Resultado de la búsqueda:")
            imprimir_datos_pais(fila)
    if not encontrado:#De lo contrario, avisa que no se encontró
        print("El pais no se encuentra en la lista.")

def filtrar_por_continente(lista_paises): #Imprime por pantalla los datos de los países que pertenezcan al continente que ingrese el usuario
    continente = pedir_nombre("Ingrese el continente por el cual desea filtrar: ")
    contador = 0
    print(f"\nPaíses ubicados en {continente}:")
    for pais in lista_paises:
        if pais["continente"] == continente:
            imprimir_datos_pais(pais)
            contador += 1
    if contador == 0:
        print("No se encontraron resultados.")        

def filtrar_por_rango(lista,dato): #Imprime por pantalla los datos de los países en los cuales el valor evaluado se mantenga dentro del rango definido
    """lista: lista a recorrer para ser filtrada
       dato: key del diccionario de país a la cual evaluar"""
    try:
        minimo = pedir_entero_positivo(f"Ingrese la cantidad mínima de {dato}: ")
        maximo = pedir_entero_positivo(f"Ingrese la cantidad máxima de {dato}: ")
    except ValueError as e:
        print(f"Error: {e}")
    contador = 0
    print(f"\nPaíses con {dato} entre {minimo} y {maximo}:")
    for pais in lista:
        if pais[dato] >= minimo and pais[dato] <= maximo:
            imprimir_datos_pais(pais)
            contador += 1
    if contador == 0:
        print("No se encontraron resultados.")  

def mayor_poblacion(lista): #Imprime por pantalla los datos del país con mayor población en la lista
    mayor = {}
    poblacion_maxima = 0
    for pais in lista:
        if pais["poblacion"] > poblacion_maxima:
            mayor = pais
            poblacion_maxima = pais["poblacion"]
    imprimir_datos_pais(mayor)

def menor_poblacion(lista): #Retorna el nombre del país con menor poblacion en la lista de diccionarios
    nombre_pais = ""
    poblacion_minima = 0
    for i in range(len(lista)):
        if i == 0:
            nombre_pais = lista[i]["nombre"]
            poblacion_minima = lista[i]["poblacion"]
        elif lista[i]["poblacion"] < poblacion_minima:
            nombre_pais = lista[i]["nombre"]
            poblacion_minima = lista[i]["poblacion"]
    return nombre_pais

def promedio_dato(lista, dato): #Retorna el promedio del dato en los paises de la lista de dicts recibida por parámetro
    acumulador = 0
    for pais in lista:
        acumulador += pais[dato]
    promedio = acumulador / len(lista)
    return promedio

def paises_por_continente(lista):
    pass

def imprimir_datos_pais(diccionario_pais):
    print(f"Nombre: {diccionario_pais["nombre"]}  Población: {diccionario_pais["poblacion"]}  Superficie: {diccionario_pais["superficie"]} km2  Continente: {diccionario_pais["continente"]}")

def pedir_nombre(mensaje):
    while True:
        try:
            nombre = input(mensaje).strip().capitalize()
            if nombre == "":
                raise ValueError("el nombre ingresado no puede estar vacío, intente nuevamente.")
        except ValueError as e:
            print(f"Error: {e}")
        else:
            break
    return nombre

def pedir_entero_positivo(mensaje):
    while True:
        try:
            numero = input(mensaje).strip()
            if numero == "":
                raise ValueError("el campo no puede estar vacío, intente nuevamente.")
            if not numero.isdigit():
                raise ValueError("debe ingresar un número entero positivo, intente nuevamente.")
        except ValueError as e:
            print(f"Error: {e}")
        else:
            break
    return int(numero)

lista_paises = cargar_csv("paises.csv")
mayor_poblacion(lista_paises)