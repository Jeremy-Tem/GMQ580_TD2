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
"""

__author__ = 'Jeremy Tem & Liam Messier'
__date__ = '2025-03-21'
__copyright__ = '(C) 2025 by Jeremy Tem & Liam Messier'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterField,
                       QgsProcessingParameterString,
                       QgsProcessingException,
                       QgsFeature
                       )


class CumulativeBufferAnalysisAlgorithm(QgsProcessingAlgorithm):
    """
    This is an example algorithm that takes a vector layer and
    creates a new identical one.

    It is meant to be used as an example of how to create your own
    algorithms and explain methods and variables used to do it. An
    algorithm like this will be available in all elements, and there
    is not need for additional work.

    All Processing algorithms should extend the QgsProcessingAlgorithm
    class.
    """

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    OUTPUT = 'OUTPUT'
    INPUT = 'INPUT'
    FIELD = 'FIELD'
    DISTANCES = 'DISTANCES'


    def initAlgorithm(self, config):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        # We add the input vector features source. It can have any kind of
        # geometry.
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                self.tr('Input Point layer'),
                [QgsProcessing.TypeVectorPoint]
            )
        )

        # We add an input that allows the user to choose a field from the
        # attribute table of the input layer
        self.addParameter(
            QgsProcessingParameterField(
                self.FIELD,
                self.tr('Field used to categorize the buffer distances'),
                parentLayerParameterName=self.INPUT
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                self.DISTANCES,
                self.tr('List of buffer distances (comma separated), e.g. 10,20,30'),
                self.tr('*Vérifier le nombre de valeurs uniques dans le champ sélectionné*')
            )
        )

        # We add a feature sink in which to store our processed features (this
        # usually takes the form of a newly created vector layer when the
        # algorithm is run in QGIS).
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr('Output Buffer layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        # Ceci est un text pour tester le commit
        

        # Retrieve the feature source and sink. The 'dest_id' variable is used
        # to uniquely identify the feature sink, and must be included in the
        # dictionary returned by the processAlgorithm function.
        source = self.parameterAsSource(parameters, self.INPUT, context)
        category_field = self.parameterAsString(parameters, self.FIELD, context)
        distances = self.parameterAsString(parameters, self.DISTANCES, context).split(',')
        (sink, dest_id) = self.parameterAsSink(parameters, self.OUTPUT,
                context, source.fields(), source.wkbType(), source.sourceCrs())
        
        # Error message
        if not source or not category_field or not distances or not sink:
            raise QgsProcessingException('Invalid input parameters')
        


        # Compute the number of steps to display within the progress bar and
        # get features from source
        total = 100.0 / source.featureCount() if source.featureCount() else 0

        buffer_features = []
        
        
        features = source.getFeatures()

        for current, feature in enumerate(features):
            # Stop the algorithm if cancel button has been clicked
            if feedback.isCanceled():
                break

            category = int(feature[category_field])
            if category < 0 or category >= len(distances):
                continue

            # Création du tampon pour la catégorie actuelle
            buffer_geom = feature.geometry().buffer(distances[category], 5)
            new_feature = QgsFeature()
            new_feature.setGeometry(buffer_geom)
            buffer_features.append(new_feature)
            feedback.setProgress(int(current * total))

            # Add a feature in the sink
            sink.addFeature(feature, QgsFeatureSink.FastInsert)

            # Update the progress bar
            feedback.setProgress(int(current * total))

        # Return the results of the algorithm. In this case our only result is
        # the feature sink which contains the processed features, but some
        # algorithms may return multiple feature sinks, calculated numeric
        # statistics, etc. These should all be included in the returned
        # dictionary, with keys matching the feature corresponding parameter
        # or output names.
        return {self.OUTPUT: dest_id}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'Cumulative Buffer Analysis'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr(self.name())

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr(self.groupId())

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return ''

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return CumulativeBufferAnalysisAlgorithm()
