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
    entry = om.get(map, sightingdate)
    if entry is None:
        datentry =  newDataEntry(sighting, categoria)
        om.put(map,sightingdate, datentry)
    else:
        datentry = me.getValue(entry)
    addDateIndex(datentry, sighting, categoria)
    return map



def addDateIndex(datentry, sighting, categoria):
    lst = datentry["lstsightings"]
    lt.addLast(lst, sighting)
    categoriaIndex = datentry[categoria+"Index"]
    entry = mp.get(categoriaIndex, sighting[categoria])

    if (entry is None):
        entry = newCategoryEntry(sighting[categoria], sighting, categoria)

        lt.addLast(entry["lst"], sighting)
        mp.put(categoriaIndex, sighting[categoria], entry)
    else:
        entry = me.getValue(entry)
        lt.addLast(entry["lst"], sighting)
    return datentry

def newDataEntry(sighting, categoria):
    entry = {categoria+"Index": None, "lstsightings": None}
    entry[categoria+"Index"] = mp.newMap(numelements=30,
                                      maptype = "PROBING",
                                      comparefunction=comparePlaces)
    entry["lstsightings"] = lt.newList("SINGLE_LINKED", compareDates)
    return entry

def newCategoryEntry(categoria, sighting, categorianombre):

    centry = {categorianombre: None, "lst": None}
    centry[categorianombre] = categoria
    centry["lst"] = lt.newList("SINGLELINKED", comparePlaces) 
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

def agregarInfo(info, totalsightings, coords):
   
    if info is not None:
        lstsightings = me.getValue(info)["lst"]
        for i in range(1, lt.size(lstsightings)+1):
            sightinginfo = lt.getElement(lstsightings, i)
            informacion = {"Ciudad": "", "Pais": "", "Duracion": 0, "Forma": ""}
            informacion["Ciudad"] = sightinginfo["city"]
            informacion["Pais"] = sightinginfo["country"] 
            informacion["Duracion"] = sightinginfo["duration (seconds)"]
            informacion["Forma"] =  sightinginfo["shape"]
            if coords:
                informacion["Longitud"] = round(float(sightinginfo["longitude"]), 3)
                informacion["Latitud"] = round(float(sightinginfo["latitude"]), 4)
            sighting = {sightinginfo["datetime"]: informacion}
            lt.addLast(totalsightings, sighting)

    return totalsightings


def getSightingsbyCity(analyzer, city):
    totalsightings = lt.newList(cmpfunction=compareDates)
    sightingDatesPair = om.keySet(analyzer["dateIndex"])
    for i in range(1, lt.size(sightingDatesPair)+1):
        date = (lt.getElement(sightingDatesPair, i))
        sightingdate = om.get(analyzer["dateIndex"], date)
        sightingmap = me.getValue(sightingdate)["cityIndex"]

        info = mp.get(sightingmap, city)
        
        totalsightings = agregarInfo(info, totalsightings, False)
    return totalsightings
 

def sightingsbyDuration(analyzer, limsup, limin):
    max = 0
    totalsightings = lt.newList(cmpfunction=compareDurations)
    sightingDatesPair = om.keySet(analyzer["dateIndex"])
    for i in range(1, lt.size(sightingDatesPair)+1):
        date = (lt.getElement(sightingDatesPair, i))
        sightingdate = om.get(analyzer["dateIndex"], date)
        
        sightingmap = me.getValue(sightingdate)["duration (seconds)Index"]
        duracion = lt.firstElement(mp.keySet(sightingmap))
        if float(duracion) > max:
            max = float(duracion)
        if float(duracion) >= limin and float(duracion) <= limsup:
            info = mp.get(sightingmap, duracion)
            totalsightings = agregarInfo(info, totalsightings, False)
    return(totalsightings, max)  
    
def latestSightings(analyzer, limsup, limin):
    max = datetime.datetime.strptime("00:00:00", "%X")
    totalsightings = lt.newList(cmpfunction=compareDurations)
    sightingDatesPair = om.keySet(analyzer["dateIndex"])
    limsup = datetime.datetime.strptime(limsup, "%X")
    limin = datetime.datetime.strptime(limin, "%X")
    for i in range(1, lt.size(sightingDatesPair)+1):
        date = (lt.getElement(sightingDatesPair, i))
        sightingdate = om.get(analyzer["dateIndex"], date)
        sightingmap = me.getValue(sightingdate)["datetimeIndex"]
        duracion = lt.firstElement(mp.keySet(sightingmap))    
        duracionprov = datetime.datetime.strptime(duracion, "%Y-%m-%d %H:%M:%S")
        if str(duracionprov.time()) > str(max):
            max = duracionprov.time()
        if duracionprov.time() > limin.time() and duracionprov.time() < limsup.time():
            info = mp.get(sightingmap, duracion)
            totalsightings = agregarInfo(info, totalsightings, False)
    return(totalsightings, max)  
    

def sightingsbyRange(analyzer, limsup, limin):
    max = datetime.datetime.strptime("2021-12-30", "%Y-%m-%d")
    totalsightings = lt.newList(cmpfunction=compareDurations)
    sightingDatesPair = om.keySet(analyzer["dateIndex"])
    limsup = datetime.datetime.strptime(limsup, "%Y-%m-%d")
    limin = datetime.datetime.strptime(limin, "%Y-%m-%d")
    for i in range(1, lt.size(sightingDatesPair)+1):
        date = (lt.getElement(sightingDatesPair, i))
        sightingdate = om.get(analyzer["dateIndex"], date)
        sightingmap = me.getValue(sightingdate)["datetimeIndex"]
        duracion = lt.firstElement(mp.keySet(sightingmap))    
        duracionprov = datetime.datetime.strptime(duracion, "%Y-%m-%d %H:%M:%S")
        if str(duracionprov.date()) < str(max):
            max = duracionprov.date()
        if duracionprov.date() > limin.date() and duracionprov.date() < limsup.date():
            info = mp.get(sightingmap, duracion)
            totalsightings = agregarInfo(info, totalsightings, False)
    return(totalsightings, max)  
    

def sightingsbycoords(analyzer, lonmax, lonmin, latmax, latmin):
    totalsightings = lt.newList(cmpfunction=compareDurations)
    sightingDatesPair = om.keySet(analyzer["dateIndex"])    
    for i in range(1, lt.size(sightingDatesPair)+1):
        date = (lt.getElement(sightingDatesPair, i))
        sightingdate = om.get(analyzer["dateIndex"], date)
        sightingmap = me.getValue(sightingdate)["longitudeIndex"]
        longitud = lt.firstElement(mp.keySet(sightingmap))
        if abs(float(longitud)) > abs(lonmin) and abs(float(longitud)) < abs(lonmax):
            infolst = mp.get(sightingmap, longitud)
            lstsightings = me.getValue(infolst)["lst"]
            for i in range(0, lt.size(lstsightings)):
                sightinginfo = lt.getElement(lstsightings, i)
                if float(sightinginfo["latitude"]) > latmin and float(sightinginfo["latitude"]) < latmax:  
                    agregarInfo(infolst, totalsightings, True)
    return(totalsightings)

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