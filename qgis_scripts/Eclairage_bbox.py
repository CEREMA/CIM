from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterFile,
    QgsProcessingParameterFeatureSink,
    QgsProject,
    QgsRasterLayer,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsProcessingParameterEnum,
    QgsMessageLog,
    Qgis
)

from qgis.utils import iface
from qgis import processing
from urllib.request import urlretrieve
import osmnx as ox
import mercantile
import requests
from vt2geojson.tools import vt_bytes_to_geojson
from concurrent.futures import ThreadPoolExecutor
from shapely.geometry import box, shape, Point, polygon
import geopandas as gpd
import os
import json
import functools

class GET_DATA_ECLAIRAGE_BBOX(QgsProcessingAlgorithm):
    
    OUTPUT = 'OUTPUT'
    OUTPUT_INT = 'OUTPUT_INT'
    ATTRIBUTE_VALUE = 'ATTRIBUTE_VALUE'
    access_token = 'access_token'

    def __init__(self):
        super().__init__()

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return type(self)()

    def name(self):
        return 'Eclairage_bbox'

    def displayName(self):
        return self.tr('Eclairage_bbox')

    def initAlgorithm(self, config=None):
        
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_INT,
                'Données_brutes_eclairage_datasud'
            )
        )
        
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                'Output'
            )
        )

        self.addParameter(
            QgsProcessingParameterFile(
                self.access_token,
                'Clé token Mapillary',
                optional=True
            )
        )

        #Ajouter le paramètre de liste déroulante
        options = ['Mapillary','OSM','Data_sud']
        self.addParameter(
            QgsProcessingParameterEnum(
            self.ATTRIBUTE_VALUE,
            "Source des données",
            options
            )
        )
        
    def processAlgorithm(self, parameters, context, feedback):
        
        # Initialisation de QgsProject et configuration de la projection pour chaque couche
        project = QgsProject.instance()
        crs = QgsCoordinateReferenceSystem(4326)
        project.setCrs(crs)
        
        source = self.parameterAsEnum(parameters, "Source des données", context)
        
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
        
        if source == 0: #Mapillary
            
            #access_token = self.parameterAsString(parameters, 'access_token', context)
            #with open(access_token, encoding="utf-8") as f:
                #access_token_text = f.read()

            access_token_param = self.parameterAsFile(parameters, self.access_token, context)
    
            if access_token_param:
                with open(access_token_param, encoding="utf-8") as f:
                    access_token_text = f.read()
            else:
                access_token_text = None  # Si non fourni, définir access_token_text comme None
                
            data_type = "tile_points"
            output = self.parameterAsOutputLayer(parameters, self.OUTPUT, context)

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

            get_mapillary_data(data_type, access_token_text, xmin, ymin, xmax, ymax, output)
        
        elif source == 1 : #OSM
            
            output = self.parameterAsOutputLayer(parameters, self.OUTPUT, context)

            def extract_from_bbox_osm(tags, S,N,E,W):
                
                bbox=(S,N,E,W)
                data_bbox = ox.features_from_bbox(*bbox, tags = tags)

                return(data_bbox)

            def export_osm(data, output):
                # Export en GeoPackage
                data.to_file(output, driver = "GPKG")

            def get_eclairage_bbox_OSM(S,N,E,W, output):
                
                # Voici les tags OSM associés à l'éclairage
                tags = {'highway': 'street_lamp'}

                # Extraction des données OSM relatives à l'éclairage
                eclairage = extract_from_bbox_osm(tags, S,N,E,W)
                
                # Export des données en Geopackage
                export_osm(eclairage, output)

            (S,N,E,W) = (ymin, ymax, xmin, xmax)

            get_eclairage_bbox_OSM(S,N,E,W, output)
        
        else: #Data_sud
            
            fichier_intermediaire = self.parameterAsOutputLayer(parameters, self.OUTPUT_INT, context)
            output_datasud = self.parameterAsOutputLayer(parameters, self.OUTPUT, context)
            def get_ecleraige_marseille_datasud(fichier_intermediaire):
                url = "https://www.datasud.fr/fr/dataset/datasets/858/resource/1013/download/"
                urlretrieve(url, fichier_intermediaire)
                return(fichier_intermediaire)
                
            def get_eclairage_BBOX_datasud(fichier_intermediaire, S, N , E, W, output_folder) :
                eclairage_marseille = get_ecleraige_marseille_datasud(fichier_intermediaire)
                csv = gpd.read_file(eclairage_marseille)
                gdf_eclairage = gpd.GeoDataFrame(
                    csv, geometry=gpd.points_from_xy(csv.LONGITUDE, csv.LATITUDE)
                )
                bound=box(E,S,W,N)
                boundgdf = gpd.GeoDataFrame({'geometry': [bound]}, crs='EPSG:4326') #avoir le geodataframe du bbox

                bounding_area = boundgdf
                boundgdf.set_crs(epsg=4326, inplace=True)
                gdf_eclairage.set_crs(epsg=4326, inplace=True)
                
                gdf_filtered = gpd.sjoin(gdf_eclairage, bounding_area, predicate='intersects')
                gdf_filtered.set_crs(4326, allow_override=True)
                print("il s'agit de %d ouvrages d'éclairage public au niveau du territoire d'étude" % len(gdf_filtered))
                eclairage_bbox_datasud = gdf_filtered.to_file(output_folder, driver = "GPKG")
            
            (S, N, E, W) = (ymin, ymax, xmin, xmax)
            
            get_eclairage_BBOX_datasud(fichier_intermediaire, S, N , E, W, output_datasud)

        return {}