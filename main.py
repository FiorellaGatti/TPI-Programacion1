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



     
     