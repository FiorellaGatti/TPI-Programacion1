import csv
def cargar_csv(nombre_archivo): #Función para leer el archivo csv y crear la lista de diccionarios
    try:
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:#abre el archivo en modo reader            
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
    while True: #Inicia ciclo While para volver a pedir si es necesario
        try:#verificaciones para cada ingreso del usuario. Valida campos vacíos, tipo de dato correcto y convierte en entero a los datos de superficie y población
            nombre_pais = input("Ingrese el nombre del nuevo país: \n").capitalize().strip()
            if nombre_pais == "": 
                raise ValueError("El nombre no puede estar vacío")
            poblacion = input("Ingrese el número de la población de ese país: \n").strip()
            if poblacion == "":
                raise ValueError("El campo no puede estar vacío")
            if not poblacion.isdigit(): 
                raise ValueError("Debe ingresar un número entero mayor a 0.")
            if poblacion == '0':
                    raise ValueError("Debe ingresar un número entero mayor a 0.")
            poblacion = int(poblacion)
            superficie = input("Ingrese el número de la superficie de ese país: \n").strip()
            if superficie == "":
                raise ValueError("El campo no puede estar vacío")
            if superficie == '0':
                    raise ValueError("Debe ingresar un número entero mayor a 0.")
            if not superficie.isdigit(): 
                raise ValueError("Debe ingresar un número entero mayor a 0.")
            superficie = int(superficie)
            continente = input("Ingrese el continente del nuevo país: \n").capitalize().strip()
            if continente == "":
                raise ValueError("El nombre no puede estar vacío")
            break
        except ValueError as e:
            print(f"Error: {e}")
    nuevo_pais = { #Crea diccionario del nuevo país con los datos ingresados por el usuario
           
        "nombre":nombre_pais,
        "poblacion":poblacion,
        "superficie":superficie,
        "continente":continente
    }
    lista_paises.append(nuevo_pais) #Agrega nuevo diccionario a la lista_paises
    print("Nuevo país agregado a la lista.")
    
def actualizar_pais(lista_paises):#Función para que el usuario actualice población y superficie de un país
    while True:
        try:
            nombre = input("Ingrese el nombre del país que desea buscar: \n").capitalize().strip()
            if nombre == "": 
                raise ValueError("El nombre no puede estar vacío")
            break
        except ValueError as e:
            print(f"Error: {e}")
    encontrado = False #declara bandera para verificar siel pais fue encontrada dentro de la lista y luego inicia ciclo for para recorrerla y buscarlo
    for fila in lista_paises:
        if nombre == fila['nombre'].capitalize().strip():
            encontrado = True#si encuentra el pais dentro de la lista, cambia bandera a true, la guarda en una nueva variable y rompe el ciclo para que no siga buscando innecesariamente
            pais_encontrado = fila
            break
    if encontrado: #si la bandera es True, pide datos para actualizar población y superficie
        while True:
            try:
                superficie = input("Ingrese el nuevo valor de superficie: \n").strip()
                if superficie == "":
                        raise ValueError("El campo no puede estar vacío")
                if superficie == '0':
                    raise ValueError("Debe ingresar un número entero mayor a 0.")
                if not superficie.isdigit(): 
                    raise ValueError("Debe ingresar un número entero mayor a 0.")
                superficie = int(superficie)
                poblacion = input("Ingrese el nuevo valor de poblacion: \n").strip()
                if poblacion == "":
                        raise ValueError("El campo no puede estar vacío")
                if poblacion == '0':
                    raise ValueError("Debe ingresar un número entero mayor a 0.")
                if not poblacion.isdigit(): 
                    raise ValueError("Debe ingresar un número entero mayor a 0.")
                poblacion = int(poblacion)
                break
            except ValueError as e:
                print(f"Error: {e}")
        pais_encontrado["superficie"] = superficie
        pais_encontrado["poblacion"] = poblacion
        print(f"Pais actualizado, nueva superficie: {pais_encontrado['superficie']}, nueva población: {pais_encontrado['poblacion']}")
    else:#De lo contrario, muestra que el pais no está en la lista.
                print("El pais no se encuentra en la lista.")

def buscar_pais(lista_paises):#Función para que el usuario busque un país en la lista
    while True:
        try:
            nombre = input("Ingrese el nombre o parte del nombre del país que desea buscar: \n").capitalize().strip()
            if nombre == "": 
                raise ValueError("El nombre no puede estar vacío")
            break
        except ValueError as e:
            print(f"Error: {e}")
    encontrado = False #declara bandera para verificar si el país fue encontrada dentro de la lista y luego inicia ciclo for para recorrerla y buscarlo
    for fila in lista_paises:
        if nombre in fila['nombre'].capitalize().strip():#si encuentra coincidencia parcial o exacta, las muestra y cambia bandera a True
            encontrado = True
            print(f"Resultado de la búsqueda: {fila}")
    if not encontrado:#De lo contrario, avisa que no se encontró
        print("El pais no se encuentra en la lista.")

