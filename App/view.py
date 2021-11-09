"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """



from model import compareDurations
from model import compareDates
import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

sightingsfile = "UFOS-utf8-small.csv"

def printMenu():
    print("Bienvenido")
    print("1- Inicializar")
    print("2- Cargar información en el catálogo")
    print("3- Contar avistamientos en una ciudad")
    print("4- Contar avistamientos por duracion")
    print("5- Contar avistamientos por horas / minutos")
    print("6- Contar avistamientos en un rango de fechas")
    print("7- Contar avistamientos en una zona geografica")
    print("0- Salir")

def crearTop(resultado, comparacion):
    print("\nSe encontraron " + str(lt.size(resultado)) + " avistamientos\n")
    print("\nLos primeros y ultimos 3 avistamientos se muestran a continuacion: ")
    if lt.size(resultado) >= 6:
        top = lt.newList(cmpfunction=comparacion)
        for i in range(0,3):
            lt.addLast(top, lt.firstElement(resultado))
            lt.removeFirst(resultado)
        i = 2
        while i >= 0:
            lt.addLast(top, lt.getElement(resultado, lt.size(resultado)-i))
            lt.deleteElement(resultado, lt.size(resultado)- i)
            i -= 1
        printAvistamiento(top)
    
    else: 
        printAvistamiento(resultado)

def printAvistamiento(resultado):
    for i in range(1, lt.size(resultado) +1):
        info = lt.getElement(resultado, i)
        for fecha in info.keys():
            print("+"+"-"*50+"+")
            print("Fecha: " + fecha +"\n")
            print("Informacion encontrada: " + str(info[fecha]) +"\n")
            print("+"+"-"*50+"+")
    print("+"+"-"*50+"+\n")


catalog = None
    
    

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Inicializando...")
        cont = controller.init()

    elif int(inputs[0]) == 2:
        print("\nCargando informacion de avistamientos...")

        controller.loadData(cont, sightingsfile, "city")

        print('Avistamientos cargados: ' + str(controller.sightingsSize(cont)))
        print('Altura del arbol: ' + str(controller.indexHeight(cont)))
        print('Elementos en el arbol: ' + str(controller.indexSize(cont)))
        print('Menor Llave: ' + str(controller.minKey(cont)))
        print('Mayor Llave: ' + str(controller.maxKey(cont)))
        cont = controller.init()

    elif int(inputs[0]) == 3:
        print("\nRecuperando informacion...")
        controller.loadData(cont, sightingsfile, "city")
        city = input("\nCiudad a buscar: \n>")
        print("\nCargando ciudades...")
        resultado = controller.getSightingsbyCity(cont, city)
        crearTop(resultado, compareDates)
        cont = controller.init()

    elif int(inputs[0]) == 4:
        print("\nRecuperando informacion...")
        controller.loadData(cont, sightingsfile, "duration (seconds)")
        limin = float(input("Ingrese un limite inferior: "))
        limsup = float(input("Ingrese limite superior: " ))
        print("\nCargando avistamientos por duracion...")
        resultado, max = controller.sightingsbyDuration(cont, limsup, limin)
        crearTop(resultado, compareDurations)
        print("\nEl avistamiento mas largo registrado tiene una duracion de " + str(max) +" segundos")
        cont = controller.init()

    elif int(inputs[0]) == 5:
        print("\nRecuperando informacion...")
        controller.loadData(cont, sightingsfile, "datetime")
        limin = input("Ingrese un limite inferior: ")
        limsup =input("Ingrese limite superior: " )
        print("\nCargando avistamientos por hora...")
        resultado, max = controller.latestSighting(cont, limsup, limin)
        crearTop(resultado, compareDurations)
        print("\nEl avistamiento mas tarde ocurrio a las " + str(max))
        cont = controller.init()

    
    else:
        sys.exit(0)


    
sys.exit(0)
