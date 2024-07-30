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
from urllib.request import urlretrieve
import geopandas as gpd
from shapely.geometry import box, polygon
import osmnx as ox

class GET_DATA_ECLAIRAGE_DATASUD(QgsProcessingAlgorithm):
    
    OUTPUT_INT = 'OUTPUT_INT'
    OUTPUT_GPKG = 'OUTPUT_GPKG'

    def __init__(self):
        super().__init__()

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return type(self)()

    def name(self):
        return 'Eclairage_DATASUD'

    def displayName(self):
        return self.tr('Eclairage_DATASUD')

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_INT,
                'Output intermédiaire'
            )
        )

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
        
        fichier_intermediaire = self.parameterAsOutputLayer(parameters, self.OUTPUT_INT, context)
        output_gpkg = self.parameterAsOutputLayer(parameters, self.OUTPUT_GPKG, context)

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
        
        get_eclairage_BBOX_datasud(fichier_intermediaire, S, N , E, W, output_gpkg)
        
        return {}
            