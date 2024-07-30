from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterFile,
    QgsProcessingParameterFeatureSink,
    QgsProject,
    QgsRasterLayer,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform
)
from qgis.utils import iface
from qgis import processing
import mercantile
import requests
from vt2geojson.tools import vt_bytes_to_geojson
from concurrent.futures import ThreadPoolExecutor
from shapely.geometry import box, shape
import geopandas as gpd
import os
import json
import functools

class GET_DATA_ECLAIRAGE_MLY(QgsProcessingAlgorithm):
    
    OUTPUT_GEOJSON = 'OUTPUT_GEOJSON'

    def __init__(self):
        super().__init__()

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return type(self)()

    def name(self):
        return 'Eclairage_mly'

    def displayName(self):
        return self.tr('Eclairage_mly')

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_GEOJSON,
                'Output GeoJSON'
            )
        )

        self.addParameter(
            QgsProcessingParameterFile(
                'access_token',
                'Clé token Mapillary'
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        
        # Initialisation de QgsProject et configuration de la projection pour chaque couche
        project = QgsProject.instance()
        crs = QgsCoordinateReferenceSystem(4326)
        project.setCrs(crs)
        
        access_token = self.parameterAsString(parameters, 'access_token', context)
        
        with open(access_token, encoding="utf-8") as f:
            access_token_text = f.read()

        canvas = iface.mapCanvas()
        extent = canvas.extent()
        
        project.setCrs(canvas.mapSettings().destinationCrs())
        
        # Définir la transformation de la projection de la carte en WGS84
        transform = QgsCoordinateTransform(canvas.mapSettings().destinationCrs(), QgsCoordinateReferenceSystem('EPSG:4326'), project)
        
        # Projeter l'étendue de la carte dans le système de coordonnées géographiques (lat/lon)
        extent_wgs84 = transform.transformBoundingBox(extent)
        
        xmin = extent_wgs84.xMinimum()
        xmax = extent_wgs84.xMaximum()
        ymin = extent_wgs84.yMinimum()
        ymax = extent_wgs84.yMaximum()
        
        #xmin = extent.xMinimum()
        #xmax = extent.xMaximum()
        #ymin = extent.yMinimum()
        #ymax = extent.yMaximum()
        
        data_type = "tile_points"
        output_geojson = self.parameterAsOutputLayer(parameters, self.OUTPUT_GEOJSON, context)

        def choose_data_type(data_type):

            if (data_type == "tile_points"):
                return("mly_map_feature_point")
            elif (data_type == "tile_traffic_signs"):
                return("mly_map_feature_traffic_sign")

        def filter_features(features, polygon):

            filtered_features = []
            for feature in features:
                geom = shape(feature['geometry'])
                if geom.intersects(polygon):
                    filtered_features.append(feature)
            return filtered_features
        
        def fetch_tile(tile, data_type):
            
            tile_url = f'https://tiles.mapillary.com/maps/vtp/{choose_data_type(data_type)}/2/{tile.z}/{tile.x}/{tile.y}?access_token={access_token_text}'
            response = requests.get(tile_url)
            data = vt_bytes_to_geojson(response.content, tile.x, tile.y, tile.z)
            filter_values = ["object--street-light"]
            #choisir les type selon les valeurs des entités
            filtered_data = [feature for feature in data['features'] if feature['properties']['value'] in filter_values]
            return (filtered_data)
        
        def get_mapillary_data(data_type, access_token, xmin, ymin, xmax, ymax,output_folder):
            
            # Définir un GeoJSON vide en tant que sortie
            output = {"type": "FeatureCollection", "features": []}

            # Récupérer la liste des tuiles intersectant notre bounding box
            tiles = list(mercantile.tiles(xmin, ymin, xmax, ymax, 14))

            # Créer un polygone à partir de la bounding box
            bbox_polygon = box(xmin, ymin, xmax, ymax)
            gdf_bbox = gpd.GeoDataFrame({'geometry': [bbox_polygon]}, crs='EPSG:4326')

            # Utilisation de functools.partial pour fixer la valeur de l'argument 'data_type' dans la fonction fetch_tile
            partial_fetch_tile = functools.partial(fetch_tile, data_type=data_type)

            # Exécuter les requêtes en parallèle vu le nombre important des tuiles
            with ThreadPoolExecutor() as executor:
                results = list(executor.map(partial_fetch_tile, tiles))

            # Filtrer les resultats des entités contenues dans la bbox
            for features in results:
                filtered_features = filter_features(features, bbox_polygon)
                output['features'].extend(filtered_features)

            # Export du fichier résultat sous fromat geojson
            with open(output_folder, "w") as fx:
                json.dump(output, fx)

        get_mapillary_data(data_type, access_token_text, xmin, ymin, xmax, ymax, output_geojson)

        return {}