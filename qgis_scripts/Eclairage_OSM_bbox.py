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
import osmnx as ox
import geopandas as gpd
from shapely.geometry import Point, box, polygon

class GET_DATA_ECLAIRAGE_OSM(QgsProcessingAlgorithm):
    
    OUTPUT_GPKG = 'OUTPUT_GPKG'

    def __init__(self):
        super().__init__()

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return type(self)()

    def name(self):
        return 'Eclairage_OSM'

    def displayName(self):
        return self.tr('Eclairage_OSM')

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_GPKG,
                'Output GPKG'
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        
        # Initialisation de QgsProject et configuration de la projection pour chaque couche
        project = QgsProject.instance()
        crs = QgsCoordinateReferenceSystem(4326)
        project.setCrs(crs)

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
        
        output_gpkg = self.parameterAsOutputLayer(parameters, self.OUTPUT_GPKG, context)

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

        get_eclairage_bbox_OSM(S,N,E,W, output_gpkg)
        
        return {}