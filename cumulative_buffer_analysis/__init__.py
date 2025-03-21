# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CumulativeBufferAnalysis
                                 A QGIS plugin
 Ce plugin génère une zone tampon à plusieurs distances spécifiées par l'utilisateur selon un attribut de la couche
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2025-03-21
        copyright            : (C) 2025 by Jeremy Tem & Liam Messier
        email                : jeremy.tem@usherbrooke.ca
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""

__author__ = 'Jeremy Tem & Liam Messier'
__date__ = '2025-03-21'
__copyright__ = '(C) 2025 by Jeremy Tem & Liam Messier'


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load CumulativeBufferAnalysis class from file CumulativeBufferAnalysis.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .cumulative_buffer_analysis import CumulativeBufferAnalysisPlugin
    return CumulativeBufferAnalysisPlugin()
