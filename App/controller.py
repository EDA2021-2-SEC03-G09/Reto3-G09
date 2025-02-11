﻿"""
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
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def init():
  
    analyzer = model.newAnalyzer()
    return analyzer

# Funciones para la carga de datos

def loadData(analyzer, ufosfile, categoria):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    ufosfile = cf.data_dir + ufosfile
    input_file = csv.DictReader(open(ufosfile, encoding="utf-8"),
                                delimiter=",")
    for sighting in input_file:
        model.addSighting(analyzer, sighting, categoria)
    return analyzer

def sightingsSize(analyzer):
    return model.sightingssize(analyzer)


def indexHeight(analyzer):
    return model.indexHeight(analyzer)

def indexSize(analyzer):

    return model.indexSize(analyzer)

def minKey(analyzer):
    """
    La menor llave del arbol
    """
    return model.minKey(analyzer)


def maxKey(analyzer):
    """
    La mayor llave del arbol
    """
    return model.maxKey(analyzer)

def getSightingsbyCity(analyzer, city):
    return model.getSightingsbyCity(analyzer, city)

def sightingsbyDuration(analyzer, limin, limsup):
    return model.sightingsbyDuration(analyzer, limin, limsup)

def latestSighting(analyzer, limsup, limin):
    return model.latestSightings(analyzer, limsup, limin)

def sightingsbyRange(analyzer, limsup, limin):
    return model.sightingsbyRange(analyzer, limsup, limin)

def sightingsbycoords(analyzer, lonmax, lonmin, latmax, latmin):
    return model.sightingsbycoords(analyzer, lonmax, lonmin, latmax, latmin)

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
