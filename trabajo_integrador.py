import os
import csv

# nombre del archivo 
ARCHIVO_CSV = "paises.csv"

def inicializar_csv():
    """Crea el archivo CSV con datos iniciales si no existe."""
    if not os.path.exists(ARCHIVO_CSV):
        datos_iniciales = [
            ["nombre", "poblacion", "superficie", "continente"],
            ["Argentina", "45376763", "2780400", "América"],
            ["Japón", "125800000", "377975", "Asia"],
            ["Brasil", "213993437", "8515767", "América"],
            ["Alemania", "83149300", "357022", "Europa"],
            ["Canadá", "38250000", "9984670", "América"],
            ["Australia", "25690000", "7692024", "Oceanía"],
            ["Egipto", "104258327", "1002450", "África"]
        ]
        try:
            with open(ARCHIVO_CSV, mode="w", encoding="utf-8", newline="") as archivo:
                writer = csv.writer(archivo)
                writer.writerows(datos_iniciales)
        except Exception as e:
            print(f"Error al inicializar el archivo CSV: {e}")

def cargar_paises():
    """Lee el archivo CSV y retorna una lista de diccionarios con los países."""
    paises = []
    if not os.path.exists(ARCHIVO_CSV):
        inicializar_csv()
    
    try:
        with open(ARCHIVO_CSV, mode="r", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                try:
                    # Parseo y validación básica de tipos
                    pais = {
                        "nombre": fila["nombre"].strip(),
                        "poblacion": int(fila["poblacion"].strip()),
                        "superficie": int(fila["superficie"].strip()),
                        "continente": fila["continente"].strip()
                    }
                    paises.append(pais)
                except (ValueError, KeyError):
                    # Control de errores de formato en filas corruptas del CSV
                    continue
    except Exception as e:
        print(f"Error al leer el archivo CSV: {e}")
    
    return paises

def guardar_paises(paises):
    """Guarda la lista completa de países en el archivo CSV."""
    try:
        with open(ARCHIVO_CSV, mode="w", encoding="utf-8", newline="") as archivo:
            campos = ["nombre", "poblacion", "superficie", "continente"]
            escritor = csv.DictWriter(archivo, fieldnames=campos)
            escritor.writeheader()
            for pais in paises:
                escritor.writerow(pais)
    except Exception as e:
        print(f"Error al guardar en el archivo CSV: {e}")

def agregar_pais(paises):
    """Agrega un nuevo país validando que no haya campos vacíos y que los valores numéricos sean válidos."""
    print("\n--- AGREGAR NUEVO PAÍS ---")
    
    # Nombre
    while True:
        nombre = input("Ingrese el nombre del país: ").strip()
        if nombre:
            # Verificar si ya existe
            if any(p["nombre"].lower() == nombre.lower() for p in paises):
                print("¡Error! El país ya se encuentra registrado.")
                return
            break
        print("El campo no puede estar vacío.")

    # Población
    while True:
        try:
            poblacion = int(input("Ingrese la población (número entero): "))
            if poblacion > 0:
                break
            print("La población debe ser mayor a 0.")
        except ValueError:
            print("Por favor, ingrese un número entero válido.")

    # Superficie
    while True:
        try:
            superficie = int(input("Ingrese la superficie en km² (número entero): "))
            if superficie > 0:
                break
            print("La superficie debe ser mayor a 0.")
        except ValueError:
            print("Por favor, ingrese un número entero válido.")

    # Continente
    while True:
        continente = input("Ingrese el continente: ").strip()
        if continente:
            break
        print("El campo no puede estar vacío.")

    nuevo = {
        "nombre": nombre.capitalize(),
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente.capitalize()
    }
    
    paises.append(nuevo)
    guardar_paises(paises)
    print(f"¡País '{nuevo['nombre']}' agregado con éxito!")

def actualizar_pais(paises):
    """Actualiza la población y superficie de un país existente."""
    print("\n--- ACTUALIZAR DATOS DE UN PAÍS ---")
    if not paises:
        print("No hay países cargados en el sistema.")
        return

    busqueda = input("Ingrese el nombre del país a actualizar: ").strip().lower()
    encontrados = [p for p in paises if busqueda in p["nombre"].lower()]

    if not encontrados:
        print("No se encontró ningún país con ese nombre.")
        return

    print("\nCoincidencias encontradas:")
    for i, p in enumerate(encontrados):
        print(f"{i + 1}. {p['nombre']} ({p['continente']})")

    seleccion = input("Seleccione el número del país que desea actualizar: ")
    if not seleccion.isdigit() or int(seleccion) < 1 or int(seleccion) > len(encontrados):
        print("Selección inválida.")
        return

    pais_seleccionado = encontrados[int(seleccion) - 1]

    # Actualizar población
    while True:
        try:
            nueva_pobl = input(f"Nueva población [Actual: {pais_seleccionado['poblacion']}]: ").strip()
            if nueva_pobl == "":
                poblacion = pais_seleccionado["poblacion"]
                break
            poblacion = int(nueva_pobl)
            if poblacion > 0:
                break
            print("Debe ser mayor a 0.")
        except ValueError:
            print("Ingrese un número válido.")

    # Actualizar superficie
    while True:
        try:
            nueva_sup = input(f"Nueva superficie [Actual: {pais_seleccionado['superficie']}]: ").strip()
            if nueva_sup == "":
                superficie = pais_seleccionado["superficie"]
                break
            superficie = int(nueva_sup)
            if superficie > 0:
                break
            print("Debe ser mayor a 0.")
        except ValueError:
            print("Ingrese un número válido.")

    # Aplicar cambios en la lista principal
    for p in paises:
        if p["nombre"].lower() == pais_seleccionado["nombre"].lower():
            p["poblacion"] = poblacion
            p["superficie"] = superficie
            break

    guardar_paises(paises)
    print(f"¡Datos de '{pais_seleccionado['nombre']}' actualizados correctamente!")

def buscar_pais(paises):
    """Busca un país por coincidencia parcial o exacta en el nombre."""
    print("\n--- BUSCAR PAÍS ---")
    if not paises:
        print("No hay países cargados.")
        return

    query = input("Ingrese el nombre o parte del nombre a buscar: ").strip().lower()
    resultados = [p for p in paises if query in p["nombre"].lower()]

    if resultados:
        print(f"\nSe encontraron {len(resultados)} resultado(s):")
        print(f"{'Nombre':<15} | {'Población':<12} | {'Superficie (km²)':<16} | {'Continente':<15}")
        print("-" * 65)
        for p in resultados:
            print(f"{p['nombre']:<15} | {p['poblacion']:<12,d} | {p['superficie']:<16,d} | {p['continente']:<15}")
    else:
        print("No se encontraron países que coincidan con la búsqueda.")

def filtrar_paises(paises):
    """Filtra países por continente, rango de población o rango de superficie."""
    print("\n--- FILTRAR PAÍSES ---")
    if not paises:
        print("No hay países cargados.")
        return

    print("1. Filtrar por Continente")
    print("2. Filtrar por Rango de Población")
    print("3. Filtrar por Rango de Superficie")
    opcion = input("Elija una opción de filtro (1-3): ").strip()

    resultados = []
    if opcion == "1":
        continente = input("Ingrese el continente: ").strip().capitalize()
        resultados = [p for p in paises if p["continente"].lower() == continente.lower()]
    elif opcion == "2":
        try:
            min_p = int(input("Población mínima: "))
            max_p = int(input("Población máxima: "))
            resultados = [p for p in paises if min_p <= p["poblacion"] <= max_p]
        except ValueError:
            print("Error: Los valores numéricos ingresados no son válidos.")
            return
    elif opcion == "3":
        try:
            min_s = int(input("Superficie mínima (km²): "))
            max_s = int(input("Superficie máxima (km²): "))
            resultados = [p for p in paises if min_s <= p["superficie"] <= max_s]
        except ValueError:
            print("Error: Los valores numéricos ingresados no son válidos.")
            return
    else:
        print("Opción inválida.")
        return

    if resultados:
        print(f"\nResultados del filtro ({len(resultados)} encontrados):")
        print(f"{'Nombre':<15} | {'Población':<12} | {'Superficie (km²)':<16} | {'Continente':<15}")
        print("-" * 65)
        for p in resultados:
            print(f"{p['nombre']:<15} | {p['poblacion']:<12,d} | {p['superficie']:<16,d} | {p['continente']:<15}")
    else:
        print("No hay países que cumplan con los criterios especificados.")

def ordenar_paises(paises):
    """Ordena y muestra los países por nombre, población o superficie (ascendente/descendente)."""
    print("\n--- ORDENAR PAÍSES ---")
    if not paises:
        print("No hay países cargados.")
        return

    print("1. Ordenar por Nombre")
    print("2. Ordenar por Población")
    print("3. Ordenar por Superficie")
    criterio_op = input("Elija el criterio (1-3): ").strip()

    if criterio_op not in ["1", "2", "3"]:
        print("Opción inválida.")
        return

    print("1. Ascendente (A-Z / Menor a Mayor)")
    print("2. Descendente (Z-A / Mayor a Menor)")
    orden_op = input("Elija el orden (1-2): ").strip()

    reverso = True if orden_op == "2" else False

    if criterio_op == "1":
        copia_ordenada = sorted(paises, key=lambda x: x["nombre"], reverse=reverso)
    elif criterio_op == "2":
        copia_ordenada = sorted(paises, key=lambda x: x["poblacion"], reverse=reverso)
    elif criterio_op == "3":
        copia_ordenada = sorted(paises, key=lambda x: x["superficie"], reverse=reverso)

    print(f"\nPaíses ordenados:")
    print(f"{'Nombre':<15} | {'Población':<12} | {'Superficie (km²)':<16} | {'Continente':<15}")
    print("-" * 65)
    for p in copia_ordenada:
        print(f"{p['nombre']:<15} | {p['poblacion']:<12,d} | {p['superficie']:<16,d} | {p['continente']:<15}")

def mostrar_estadisticas(paises):
    """Muestra estadísticas clave del dataset."""
    print("\n--- ESTADÍSTICAS DEL SISTEMA ---")
    if not paises:
        print("No hay países cargados.")
        return

    # Mayor y menor población
    pais_mayor_poblacion = max(paises, key=lambda x: x["poblacion"])
    pais_menor_poblacion = min(paises, key=lambda x: x["poblacion"])

    # Promedios
    total_poblacion = sum(p["poblacion"] for p in paises)
    total_superficie = sum(p["superficie"] for p in paises)
    cant_paises = len(paises)

    prom_poblacion = total_poblacion / cant_paises
    prom_superficie = total_superficie / cant_paises

    # Cantidad de países por continente
    continentes = {}
    for p in paises:
        cont = p["continente"]
        continentes[cont] = continentes.get(cont, 0) + 1

    print(f"• País con mayor población: {pais_mayor_poblacion['nombre']} ({pais_mayor_poblacion['poblacion']:,d} hab.)")
    print(f"• País con menor población: {pais_menor_poblacion['nombre']} ({pais_menor_poblacion['poblacion']:,d} hab.)")
    print(f"• Promedio de población: {prom_poblacion:,.2f} habitantes")
    print(f"• Promedio de superficie: {prom_superficie:,.2f} km²")
    print("\n• Cantidad de países por continente:")
    for cont, cantidad in continentes.items():
        print(f"   - {cont}: {cantidad} país(es)")

def main():
    """Función principal que controla el flujo del menú en consola."""
    paises = cargar_paises()
    
    while True:
        print("\n==============================================")
        print("      SISTEMA DE GESTIÓN DE DATOS DE PAÍSES   ")
        print("==============================================")
        print("1. Agregar un país")
        print("2. Actualizar datos de un país (Población y Superficie)")
        print("3. Buscar un país por nombre")
        print("4. Filtrar países (Continente, Población, Superficie)")
        print("5. Ordenar países")
        print("6. Mostrar estadísticas")
        print("7. Salir")
        
        opcion = input("\nSeleccione una opción (1-7): ").strip()
        
        if opcion == "1":
            agregar_pais(paises)
        elif opcion == "2":
            actualizar_pais(paises)
        elif opcion == "3":
            buscar_pais(paises)
        elif opcion == "4":
            filtrar_paises(paises)
        elif opcion == "5":
            ordenar_paises(paises)
        elif opcion == "6":
            mostrar_estadisticas(paises)
        elif opcion == "7":
            print("\n¡Gracias por usar el sistema! Saliendo...")
            break
        else:
            print("\nOpción inválida. Por favor, elija un número entre 1 y 7.")

if __name__ == "__main__":
    main()