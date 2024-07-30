# CIM

![](https://live.staticflickr.com/5074/14237749595_bf0e61ae25_w_d.jpg)

/ Image composite : terrain (Mapillary) => JNT /

Ce répertoire contient xxx

Il a été réalisé pendant mon stage de xxx mois au Cerema Med.

Pendant ce stage, j'ai xxx sur ces territoires xxx

Sur le territoire de xxx, j'ai xxx

Sur le territoire de xxx, j'ai xxx

/ Parler de la marchabilité, de l'accessibilité /

Auteur : Alaeddine JERAD ([compte OpenStreetMap](https://www.openstreetmap.org/user/Alaeddinejerad))

## Contenu

```
data_open                         # Données ouvertes, disponibles sur les portails
  raw                             # Données brutes
  processed                       # Données traitées
terrain_data                      # Données terrain
	raw
	  06-2024-Pole-Activites-Aix  # Campagne terrain réalisée à Aix en Juin 2024
	  07-2024-Lorgues
	processed
	  06-2024-Pole-Activites-Aix
	  07-2024-Lorgues
terrain_photos                    # Echantillon de photos prises sur le terrain
cartes                            # Cartes de préparation terrain 
								  # + restitutions micro-cartographiques
notebooks
qgis-projets                      # Projets QGIS
qgis-scripts                      # Scripts QGIS
livrables                         # Livrables (rapport + projet blender)
```

## Matériel terrain utilisé

![](imagematos)

- GOPRO xxx
- RTK Centipede
- Smartphone avec le logiciel SWMaps

## Utilisation

### Scripts QGIS

Dans le dossier qgis-scripts, il y a :

- xxx qui permet de xxx
- xxx

Eclairage_bbox.py fait appel à :

- xxx

Pour utiliser un script dans QGIS, il faut xxx

Pour le script Eclairage_mly_bbox.py, il est nécessaire de créer un compte sur mapillary.

Mettre la clé API dans un fichier texte

Mapillary permet de récupérer sur une emprise territoriale :

- cette [liste d'objets points](https://www.mapillary.com/developer/api-documentation/points?locale=fr_FR)
- cette [liste d'objets traffic-sign](https://www.mapillary.com/developer/api-documentation/traffic-signs?locale=fr_FR)

Le script Eclairage_mly_bbox.py peut être adapté pour récupérer d'autres objets, pour d'autres thématiques.

#### Installation de librairies Python dans QGIS

Certains scripts QGIS nécessitent, pour fonctionner, d'installer certaines librairies python.

En particulier, le script faisant appel à Mapillary.

Voici comment installer une nouvelle librairie python dans QGIS :

- Si QGIS 3.26, aller dans `C:\ProgramData\Microsoft\Windows\Start Menu\Programs\QGIS 3.26.0`
- Ouvrir **OSGeo4W Shell**
- Taper `pip install mercantile vt2geojson geopandas pandas`
- Ouvrir QGIS
- Aller dans `Extensions > Console Python`
- Taper `import mercantile` pour tester si la librairie existe
- Sinon, essayer https://www.youtube.com/watch?v=TPMHhgR-r7E ou https://landscapearchaeology.org/2018/installing-python-packages-in-qgis-3-for-windows/

### Notebooks Python

Les notebooks ont servi à préparer les scripts QGIS. Ils sont dans le dossier **notebooks** :

| Notebook                                                     | Action                                                       | Mode d'action |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------- |
| 02.1-Eclairage_datasud.ipynb                                 | Lampadaires de DataSud                                       | OpenData      |
| 02.2-Eclairage_OSM.ipynb                                     | Lampadaires d'OSM                                            | OpenData      |
| 02.3-Eclairage_Mapillary.ipynb                               | Lampadaires de Mapillary                                     | OpenData      |
| 02.4-Eclairage_Mapillary_Par_Routes_Lorgues.ipynb            | Lampadaires le long des rues de Lorgues                      | OpenData      |
| 02.4.a-Eclairage_Mapillary_Par_Routes--mr.ipynb              | Lampadaires le long des rues de Lorgues (version Mathieu)    | OpenData      |
| 02.5-Objets_Points_Mapillary_Par_Routes_Lorgues.ipynb        | Objets points Mapillary le long des rues de Lorgues          | OpenData      |
| 03-Education_OSM.ipynb                                       | Ecoles sur une étendue géographique donnée                   | OpenData      |
| 04.1-Points_Mapillary.ipynb                                  | Objets points Mapillary                                      | OpenData      |
| 04.2-Paneaux_signalisation_Mapillary.ipynb                   | Panneaux de signalisation depuis Mapillary                   | OpenData      |
| 05.1-arrets-de-transport-datagouv.ipynb                      | Arrêts de transport depuis DataGouv                          | OpenData      |
| 05.2-arrets-de-transport-datasud.ipynb                       | Arrêts de transport depuis DataSud                           | OpenData      |
| 05.3-arrets-de-transport-OSM.ipynb.ipynb                     | Arrêts de transport depuis OSM                               | OpenData      |
| 05.4-Arrêts-Transport-API-GTFS-DataGouv.ipynb                | Arrêts de transport depuis API GTFS Data Gouv fr             |               |
| 06-passage_piétons_OSM.ipynb                                 | Passages piétons depuis OSM                                  | OpenData      |
| 07.1-trottoirs_OSM.ipynb                                     | Trottoirs depuis OSM<br />`footway:sidewalk`                 | OpenData      |
| 07.2-Présence_trottoir_OSM.ipynb                             | Présence de trottoir<br />`sidewalk': ['both','left','right']` | OpenData      |
| 08-rue_piétonne_OSM.ipynb                                    | Rue piétonne depuis OSM<br />`'highway': 'pedestrian'`       | OpenData      |
| 09-Voie_en_zone_de_rencontre_OSM.ipynb                       | Voie en zone de rencontre<br />`'highway': 'living_street', 'maxspeed':'20'` | OpenData      |
| 10-Voie_en_zone_30_OSM.ipynb                                 | `'zone:maxspeed': 'FR:30','maxspeed': '30'`                  | OpenData      |
| 11-Voie_en_zone_40_OSM-Copy1.ipynb                           | `'zone:maxspeed': 'FR:40','maxspeed': '40'`                  | OpenData      |
| 12-Voie_en_zone_50_OSM.ipynb                                 | `'zone:maxspeed': 'FR:50','maxspeed': '50'`                  | OpenData      |
| 13.1-Recalage points Gopro.ipynb (expérimental)              | Expérience de recalage des points par plus proche voisin     | Terrain       |
| 13-Vérification recalage points Gopro.ipynb                  | Vérification du recalage photo réalisé par JOSM              | Terrain       |
| 14.1-Création de la trace GPX horodatée - Lorgues.ipynb      | Création d'une trace depuis les points trackpoints collectés depuis SWMaps pour Lorgues | Terrain       |
| 14.2-Création de la trace GPX horodatée - Pole d'activités.ipynb | Création d'une trace depuis les points trackpoints collectés depuis SWMaps pour le Pôle d'Activités | Terrain       |
| 14.3-Création de la trace GPX horodatée - Rover RTK et GoPro collés.ipynb | Création d'une trace depuis les points trackpoints collectés depuis SWMaps pour le Pôle d'Activités avec GoPro et RTK collés l'un à l'autre (vérification des interférences et qualité du signal) | Terrain       |
| 14.4-Création de la trace GPX horodatée - Rover RTK et GoPro séparés.ipynb | Création d'une trace depuis les points trackpoints collectés depuis SWMaps pour le Pôle d'Activités avec GoPro et RTK séparés l'un de l'autre (vérification des interférences et qualité du signal) | Terrain       |
| 16-Liste_des_objets_Point_Mapillary.ipynb                    | Liste les objets pouvant être détectés par Mapillary         | Terrain       |
| 17-Export-GPKG-Layers-For-JOSM--MR.ipynb                     | Exporte les différentes couches contenues dans un GPKG unique issu de SWMaps | Terrain       |

### Projets QGIS

xxx

### Projet Blender

xxx

### Recalage des photos avec JOSM

xxx

### Recalage des adresses avec OSM Id

xxx

## Livrables

- Rapport de stage
- Présentation pour Data & Co
- Bibliographie Zotero : https://www.zotero.org/groups/5458220/cim-dtermed/library
- Notebooks Python
- Scripts QGIS
- Non réalisé
  - Data Management Plan


## Ressources

### Vidéos utiles

- Comment créer un MNT, un MNS et un MNH depuis une donnée LIDAR comme Lidar HD.
- xxx

### OpenStreetMap

#### Surfaces

- [smoothness](https://wiki.openstreetmap.org/wiki/Key:smoothness)
  - good
  - bad
  - ...
- [surface](https://wiki.openstreetmap.org/wiki/Key:surface)

#### Arbres

- tree_row

#### Trottoirs

- https://wiki.openstreetmap.org/wiki/Key:sidewalk
- https://wiki.openstreetmap.org/wiki/Key:width
- https://wiki.openstreetmap.org/wiki/Opensidewalkmap
- opensidewalkmap https://x.com/asturksever/status/1802702457295818931/photo/1
- walkabout https://tasks.mapwith.ai/projects/165
- OSMontrouge https://data.osmontrouge.fr/explore/dataset/emprise-des-trottoirs/information/

### Applis mobiles OSM

https://thejeshgn.com/2022/06/10/linked-list-three-android-apps-to-efficiently-contribute-to-openstreetmap/

### Points d'accès aux données

- catalogue.data.gouv.fr
- API de découverte data.gouv.fr

### Services de calculs

- Isochrones IGN ou OSM

### Data Management Plan

- *Toolkit from EU Commission http://ec.europa.eu/research/participants/data/ref/h2020/gm/reporting/h2020-tpl-oa-data-mgt-plan_en.docx
- *Horizon https://ec.europa.eu/research/participants/data/ref/h2020/grants_manual/hi/oa_pilot/h2020-hi-oa-data-mgt_en.pdf
- Belmont
  - Formation https://bfe-inf.github.io/toolkit/index.html
  - Guide https://bfe-inf.github.io/toolkit/ddomp.html
- Good practices https://zenodo.org/records/1421739
- DMP Tool https://dmptool.org/public_plans
- Liste de DMPs https://dmponline.dcc.ac.uk/public_plans
- Exemples https://www.dcc.ac.uk/resources/data-management-plans/guidance-examples
- DZW Tool https://ds-wizard.org/
- Data model plan : https://bu.univ-amu.libguides.com/donneesrecherche/PGD-DMP https://doranum.fr/wp-content/uploads/FicheSynthDMP.pdf

#### BPMN

Business Processing Model Notation (BPMN) : https://en.wikipedia.org/wiki/Business_process_modeling
