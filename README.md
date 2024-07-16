# CIM

![](https://live.staticflickr.com/5074/14237749595_bf0e61ae25_w_d.jpg)

/ Image composite : terrain (Mapillary) => JNT /

Ce répertoire contient xxx

Il a été réalisé pendant mon stage de xxx mois au Cerema Med.

Pendant ce stage, j'ai xxx sur ces territoires xxx

Sur le territoire de xxx, j'ai xxx

Sur le territoire de xxx, j'ai xxx

/ Parler de la marchabilité, de l'accessibilité /

Auteur : Alaeddine JERAD

## Contenu

```
data_open                         # Données ouvertes, disponibles sur les portails
  raw                             # Données brutes
  processed                       # Données traitées
data_terrain                      # Données terrain
	raw
	  06-2024-Pole-Activites-Aix  # Campagne terrain réalisée à Aix en Juin 2024
	  07-2024-Lorgues
	processed
	  06-2024-Pole-Activites-Aix
	  07-2024-Lorgues
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

### Scripts

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

### Notebooks

Les notebooks ont servi à préparer les scripts QGIS. 

| Besoin                            | Mode d'acquisition (mapillary / opendata / terrain / panoramax) | Notebook                                                     | Utilité               |
| --------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | --------------------- |
| Récupérer les écoles              | opendata                                                     | xxx.ipynb                                                    | Expérimental          |
| Récupérer les arrêts de transport | data                                                         | xxx.ipynb                                                    | Expérimental          |
| Récupérer les lampadaires         |                                                              |                                                              | Utilité pour le sujet |
| xxx                               | xxx                                                          | xxx                                                          |                       |
| xxx                               | xxx                                                          | xxx                                                          |                       |
| Recaler une trace                 |                                                              | xxx (voir la méthode Recalage des photos avec JOSM expliquée ci-dessous) | Utilisé               |
|                                   |                                                              |                                                              |                       |

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
