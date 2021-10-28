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

def addSighting(analyzer, sighting):
    lt.addLast(analyzer["sightings"], sighting)
    updateDateIndex(analyzer["dateIndex"], sighting)
    return analyzer

def updateDateIndex(map, sighting):
    date = sighting["datetime"]
    sightingdate = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, sightingdate.date())
    if entry is None:
        datentry =  newDataEntry(sighting)
        om.put(map,sightingdate.date(), datentry)
    else:
        datentry = me.getValue(entry)
    addDateIndex(datentry, sighting)
    return map

def addDateIndex(datentry, sighting):
    lst = datentry["lstsightings"]
    lt.addLast(lst, sighting)
    countryIndex = datentry["countryIndex"]
    counentry = mp.get(countryIndex, sighting["country"])
    if (counentry is None):
        entry = newCountryEntry(sighting["country"], sighting)
        lt.addLast(entry["lstcountries"], sighting)
        mp.put(countryIndex, sighting["country"], entry)
    else:
        entry = me.getValue(counentry)
        lt.addLast(entry["lstcountries"], sighting)
    return datentry

def newDataEntry(sighting):
    entry = {"countryIndex": None, "lstsightings": None}
    entry["countryIndex"] = mp.newMap(numelements=200,
                                      maptype = "PROBING",
                                      comparefunction=compareCountries)
    entry["lstsightings"] = lt.newList("SINGLE_LINKED", compareDates)
    return entry

def newCountryEntry(country, sighting):
    centry = {"country": None, "lstcountries": None}
    centry["country"] = country
    centry["lstcountries"] = lt.newList("SINGLELINKED", compareCountries) 
    return centry
# Funciones para creacion de datos

# Funciones de consulta
def sightingssize(analyzer):
    return lt.size(analyzer["sightings"])

def indexHeight(analyzer):
    return om.height(analyzer["dateIndex"])

def indexSize(analyzer):
    return om.size(analyzer["dateIndex"])
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

def compareCountries(country1, country2):
    country = me.getKey(country2)
    if (country1 == country):
        return 0
    elif (country1 > country):
        return 1
    else:
        return -1