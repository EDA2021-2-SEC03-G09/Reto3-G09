"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
import datetime
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newAnalyzer():

    analyzer = {"sightings": None,
                "dateIndex": None}

    analyzer["sightings"] = lt.newList("SINGLE_LINKED", compareCities)
    analyzer["dateIndex"] = om.newMap(omaptype="RBT",
                                      comparefunction=compareDates)
    return analyzer
# Funciones para agregar informacion al catalogo

def addSighting(analyzer, sighting, categoria):
    lt.addLast(analyzer["sightings"], sighting)
    updateDateIndex(analyzer["dateIndex"], sighting, categoria)
    return analyzer

def updateDateIndex(map, sighting, categoria):
    date = sighting["datetime"]
    sightingdate = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, sightingdate.date())
    if entry is None:
        datentry =  newDataEntry(sighting, categoria)
        om.put(map,sightingdate.date(), datentry)
    else:
        datentry = me.getValue(entry)
    addDateIndex(datentry, sighting, categoria)
    return map



def addDateIndex(datentry, sighting, categoria):
    lst = datentry["lstsightings"]
    lt.addLast(lst, sighting)
    categoriaIndex = datentry[categoria+"Index"]
    entry = mp.get(categoriaIndex, sighting["categoria"])
    if (entry is None):
        entry = newCategoryEntry(sighting[categoria], sighting)
        lt.addLast(entry["lstcities"], sighting)
        mp.put(categoriaIndex, sighting[categoria], entry)
    else:
        entry = me.getValue(entry)
        lt.addLast(entry["lstcities"], sighting)
    return datentry

def newDataEntry(sighting):
    entry = {"cityIndex": None, "lstsightings": None}
    entry["cityIndex"] = mp.newMap(numelements=10,
                                      maptype = "PROBING",
                                      comparefunction=comparePlaces)
    entry["lstsightings"] = lt.newList("SINGLE_LINKED", compareDates)
    return entry

def newCategoryEntry(city, sighting):
    centry = {"city": None, "lstcities": None}
    centry["city"] = city
    centry["lstcities"] = lt.newList("SINGLELINKED", comparePlaces) 
    return centry


def minKey(analyzer):
    """
    Llave mas pequena
    """
    return om.minKey(analyzer['dateIndex'])


def maxKey(analyzer):
    """
    Llave mas grande
    """
    return om.maxKey(analyzer['dateIndex'])


# Funciones para creacion de datos

# Funciones de consulta
def sightingssize(analyzer):
    return lt.size(analyzer["sightings"])

def indexHeight(analyzer):
    return om.height(analyzer["dateIndex"])

def indexSize(analyzer):
    return om.size(analyzer["dateIndex"])


def getSightingsbyCity(analyzer, city):
    totalsightings = lt.newList(cmpfunction=compareDates)
    sightingDatesPair = om.keySet(analyzer["dateIndex"])
    for i in range(1, lt.size(sightingDatesPair)+1):
        
        date = (lt.getElement(sightingDatesPair, i))
        sightingdate = om.get(analyzer["dateIndex"], date)
        sightingmap = me.getValue(sightingdate)["cityIndex"]

        info = mp.get(sightingmap, city)
        if info is not None:
            lstsightings = me.getValue(info)["lstcities"]
            for i in range(1, lt.size(lstsightings)+1):
                sightinginfo = lt.getElement(lstsightings, i)
                informacion = {"Ciudad": "", "Pais": "", "Duracion": 0, "Forma": 0}
                
            
                informacion["Ciudad"] = sightinginfo["city"]
                informacion["Pais"] = sightinginfo["country"] 
                informacion["Duracion"] = sightinginfo["duration (seconds)"]
                informacion["Forma"] =  sightinginfo["shape"]


                sighting = {sightinginfo["datetime"]: informacion}
                lt.addLast(totalsightings, sighting)
    return totalsightings
 


    


# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento

def compareCities(city1, city2):
    if (city1 == city2):
        return 0
    elif (city1 > city2):
        return 1
    else:
        return -1

def compareDates(date1, date2):
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1

def comparePlaces(city1, city2):
    city = me.getKey(city2)
    if (city1 == city):
        return 0
    elif (city1 > city):
        return 1
    else:
        return -1

def compareDurations(duration1, duration2):
    if (duration1 == duration2):
        return 0
    elif (duration1 > duration2):
        return 1
    else:
        return -1