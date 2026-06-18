import csv
import os
'''FUNCIONES PRINCIPALES'''
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
    nombre_pais = pedir_nombre("Ingrese el nombre del nuevo país: \n")
    poblacion = pedir_entero_positivo("Ingrese el número de la población de ese país: \n")
    superficie = pedir_entero_positivo("Ingrese el número de la superficie de ese país: \n")
    continente = pedir_nombre("Ingrese el continente del nuevo país: \n")
    nuevo_pais = { #Crea diccionario del nuevo país con los datos ingresados por el usuario
            
        "nombre":nombre_pais,
        "poblacion":poblacion,
        "superficie":superficie,
        "continente":continente
    }
    lista_paises.append(nuevo_pais) #Agrega nuevo diccionario a la lista_paises
    print("Nuevo país agregado a la lista.")
    
def actualizar_pais(lista_paises):#Función para que el usuario actualice población y superficie de un país
    nombre = pedir_nombre("Ingrese el nombre del país que desea buscar: \n")
    encontrado = ciclo_de_busqueda(lista_paises, nombre) 
    if encontrado == False: #si la función retorna False, el país no fue encontrado y mostramos
        print("El pais no se encuentra en la lista.")
    else: #si lo encuentra pide datos para actualizar población y superficie 
        superficie = pedir_entero_positivo("Ingrese el nuevo valor de superficie: \n")
        poblacion = pedir_entero_positivo("Ingrese el nuevo valor de poblacion: \n")
        encontrado["superficie"] = superficie
        encontrado["poblacion"] = poblacion
        print(f"Pais actualizado, nueva superficie: {encontrado['superficie']}, nueva población: {encontrado['poblacion']}")

def buscar_pais(lista_paises):#Función para que el usuario busque un país en la lista
    nombre = pedir_nombre("Ingrese el nombre o parte del nombre del país que desea buscar: \n")
    encontrado = ciclo_de_busqueda(lista_paises, nombre) 
    if encontrado == False:
        print("El pais no se encuentra en la lista.")
    else:
        imprimir_datos_pais(encontrado)

def filtrar_por_continente(lista_paises): #Imprime por pantalla los datos de los países que pertenezcan al continente que ingrese el usuario
    continente = pedir_nombre("Ingrese el continente por el cual desea filtrar: ")
    contador = 0
    print(f"\nPaíses ubicados en {continente}:")
    for pais in lista_paises:#ciclo para recorrer la lista y mostrar las coincidencias con el ingreso del usuario
        if pais["continente"] == continente:
            imprimir_datos_pais(pais)
            contador += 1
    if contador == 0:
        print("No se encontraron resultados.")        

def filtrar_por_rango(lista_paises): #Imprime por pantalla los datos de los países en los cuales el valor evaluado se mantenga dentro del rango definido
    print("FILTRAR POR:\n1- POBLACIÓN\n2- SUPERFICIE\n")
    opcion = pedir_opcion(range(1, 3))    
    if opcion == 1:
        dato = 'poblacion' #dato: key del diccionario de país a la cual evaluar
    else:
        dato = 'superficie'
    minimo = pedir_entero_positivo(f"Ingrese la cantidad mínima de {dato}: ")
    maximo = pedir_entero_positivo(f"Ingrese la cantidad máxima de {dato}: ")
    contador = 0
    print(f"\nPaíses con {dato} entre {minimo} y {maximo}:")
    for pais in lista_paises:#ciclo para recorrer lista e imprimir resultados
        if pais[dato] >= minimo and pais[dato] <= maximo:
            imprimir_datos_pais(pais)
            contador += 1
    if contador == 0:
        print("No se encontraron resultados.")  

def mayor_poblacion(lista_paises): #Imprime por pantalla los datos del país con mayor población en la lista
    mayor = {}
    poblacion_maxima = 0
    for pais in lista_paises:#ciclo para buscar el pais con la mayor poblacion, pisando variable 'mayor' con el valor más grande
        if pais["poblacion"] > poblacion_maxima:
            mayor = pais
            poblacion_maxima = pais["poblacion"]
    print("\nPaís con mayor población:")
    imprimir_datos_pais(mayor)

def menor_poblacion(lista_paises): #Imprime por pantalla los datos del país con menor población en la lista
    menor = {}
    for i in range(len(lista_paises)):
        if i == 0: #en la primer iteración se guarda el primer diccionario para comparar a partir de la segunda iteración
            menor = lista_paises[i]
        elif lista_paises[i]["poblacion"] < menor["poblacion"]:
            menor = lista_paises[i]
    print("\nPaís con menor población:")
    imprimir_datos_pais(menor)

def promedio_dato(lista_paises): #Imprime por pantalla el promedio de dato en la lista
    print("INGRESE 1 PARA EL PROMEDIO DE POBLACION, O 2 PARA EL PROMEDIO DE SUPERFICIE")
    opcion = pedir_opcion(range(1, 3))
    if opcion == 1:
        dato = 'poblacion'
    else:
        dato = 'superficie'
    acumulador = 0
    #Cálculo para sacar el promedio
    for pais in lista_paises:
        acumulador += pais[dato]
    promedio = acumulador / len(lista_paises)
    print(f"\nEl promedio de {dato} es : {promedio}")

def paises_por_continente(lista_paises): #Imprime por pantalla un listado con la cantidad de países correspondientes a cada continente
    continentes = {}
    for pais in lista_paises:
        if not pais["continente"] in continentes: #si el nombre del continente no existe como clave en el diccionario
            continentes[pais["continente"]] = 0 #creamos la clave y la inicializamos en 0
        continentes[pais["continente"]] += 1
    print("\nCantidad de países por continente:")
    for continente in continentes:
        print(f"{continente}: {continentes[continente]}")

def ordenar_paises(lista_paises):#funcion que ordena la lista por nombres, población, o superficie y además en criterio ascendente o descendente
    print("ORDENAR POR:\n1- NOMBRE\n2- POBLACIÓN\n3- SUPERFICIE\n") 
    opcion_criterio = pedir_opcion(range(1, 4))
    if opcion_criterio == 1: #dependiendo de la opción que eligió el usuario, define la variable criterio
        criterio = 'nombre'
    elif opcion_criterio == 2:
        criterio = 'poblacion'
    else:
        criterio = 'superficie'
    print("TIPO DE ORDEN:\n1- ASCENDENTE\n2- DESCENDENTE\n")
    opcion_orden = pedir_opcion(range(1, 3)) 
    if opcion_orden == 1:
        orden = True
    else:
        orden = False
    for i in range(len(lista_paises)):#ciclo anidado para aplicar metodo selection sort y ordenar la lista de manera ascendente 
        indice_minimo = i
        for j in range(i + 1, len(lista_paises)):
            if lista_paises[j][criterio] < lista_paises[indice_minimo][criterio]:#si el índice del criterio elegido por el usuario es menor al próximo índice, se guarda en indice_minimo
                indice_minimo = j
        if indice_minimo != i:
            lista_paises[i], lista_paises[indice_minimo] = lista_paises[indice_minimo], lista_paises[i]
    if not orden:#muestra la lista de manera descendente en el caso de que ascendente sea False
        lista_paises.reverse()
    print(F"\nLista de países ordenados por {criterio}\n")
    for pais in lista_paises:
        imprimir_datos_pais(pais)

'''FUNCIÓN MAIN'''
def main():
    lista_paises = cargar_csv("paises.csv")
    if lista_paises != None:
        while True:
            mostrar_menu()
            opcion = pedir_opcion(range(1, 9))
            if opcion == 1:
                agregar_pais(lista_paises)
            elif opcion == 2:
                actualizar_pais(lista_paises)
            elif opcion == 3:
                buscar_pais(lista_paises)
            elif opcion == 4:
                filtrar_por_continente(lista_paises)
            elif opcion == 5:
                filtrar_por_rango(lista_paises)
            elif opcion == 6:
                ordenar_paises(lista_paises)
            elif opcion == 7:
                mostrar_estadisticas(lista_paises)
            else:
                print("Gracias por utilizar el programa. Saliendo...")
                break
                

'''FUNCIONES AUXILIARES'''

def pedir_nombre(mensaje): #Pide el ingreso de un nombre al usuario, lo normaliza, valída que no esté vacío y si cumple con los requisitos lo retorna, sinó lo vuelve a pedir hasta que se ingrese uno válido
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

def pedir_entero_positivo(mensaje): #Pide el ingreso de un número al usuario, valída que no esté vacío que sea un entero y que sea positivo, si cumple con requisitos lo convierte a entero y lo retorna, sinó lo vuelve a pedir hasta que se ingrese uno válido
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
    
def mostrar_menu(): #Función que muestra el menú de opciones
    print("\n" + "="*40)
    print("   MENÚ DE OPCIONES")
    print("="*40)
    print(" 1. Agregar un país.")
    print(" 2. Actualizar datos de un país.")
    print(" 3. Buscar un país por nombre.")
    print(" 4. Filtrar por continente.")
    print(" 5. Filtrar por rango.")
    print(" 6. Ordenar países.")
    print(" 7. Mostrar estadísticas.")
    print(" 8. Salir.")
    print("-" * 40)

def pedir_opcion(opciones_validas): #Función para pedir ingreso de opciones al usuario y validar su rango
    while True:
        opcion = pedir_entero_positivo("Ingrese el número de la opción que desea: \n")
        if opcion in opciones_validas:
            break
        else:
            print("Error: debe ingresar un número dentro del rango de las opciones. Intente nuevamente.")
    return opcion

def mostrar_estadisticas(lista_paises):#Pide una opción al usuario y llama a la función correspondiente
    print("INGRESE EL NÚMERO CORRESPONDIENTE A LA ESTADÍSTICA QUE DESEA CONSULTAR:\n1- MAYOR POBLACIÓN\n2- MENOR POBLACIÓN\n3- PROMEDIOS\n4- PAISES POR CONTINENTE")
    opcion = pedir_opcion(range(1, 5))
    if opcion == 1:
        mayor_poblacion(lista_paises)
    elif opcion == 2:
        menor_poblacion(lista_paises)
    elif opcion == 3:
        promedio_dato(lista_paises)
    else:
        paises_por_continente(lista_paises)

def imprimir_datos_pais(diccionario_pais): #Imprime por pantalla los datos de el país pasado por parámetro
    print(f"Nombre: {diccionario_pais["nombre"]}  Población: {diccionario_pais["poblacion"]}  Superficie: {diccionario_pais["superficie"]} km2  Continente: {diccionario_pais["continente"]}")

def ciclo_de_busqueda(lista_paises, nombre):#Busca un país en la lista, si está lo retorna, sino retorna False
    for fila in lista_paises:
        if nombre in fila['nombre'].capitalize().strip():#si encuentra coincidencia parcial o exacta, las muestra y cambia bandera a True
            return fila
    return False



main()