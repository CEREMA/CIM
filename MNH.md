# Création de MNH

Tuto inspiré de https://www.youtube.com/watch?v=dgZLSgtaRYI (Création de MNT, MNS, MNSn dans QGIS à partir de données LiDAR ( QGIS 8/10))

## Téléchargement du LIDAR

- Aller sur https://diffusion-lidarhd.ign.fr/
- Aller sur Lorgues
- Télécharger la donnée en cliquant sur le lien
  - On peut aussi copier le lien https://storage.sbg.cloud.ovh.net/v1/AUTH_63234f509d6048bca3c9fd7928720ca1/ppk-lidar/QQ/LHD_FXX_0971_6272_PTS_C_LAMB93_IGN69.copc.laz pour le mettre dans QGIS

## DSM (MNS ou Modèle Numérique de Surface)

- Ouvrir la dalle LIDAR LHD_FXX_0971_6272_PTS_C_LAMB93_IGN69.copc.laz
- Aller dans `Traitement > Conversion de nuage de points > Exporter en raster`
  - Entrée : LIDAR LHD_FXX_0971_6272_PTS_C_LAMB93_IGN69.
  - Attribut : Z
  - Resolution : 0.5
  - Tile size : 1000
  - Advanced parameters
    - Filter expression
      - Laisser vide
  - DSM.tif
- Ouvrir DSM.tif
- Aller dans `Outils raster > Remplir les cellules sans données`
  - Entrée : DSM
  - Maximum distance : 100 (nb de pixels voisins pour l'estimation)
  - Nb of smoothing : 10
  - FilledDSM.tif

## DTM (MNT ou Modèle Numérique de Terrain)

- Ouvrir la dalle LIDAR
- Aller dans `Traitement > Conversion de nuage de points > Exporter en raster`
  - Entrée : LIDAR LHD_FXX_0971_6272_PTS_C_LAMB93_IGN69.
  - Attribut : Z
  - Resolution : 0.5
  - Tile size : 1000
  - Advanced parameters
    - Filter expression
      - Classification = 2 (ground)
  - DTM.tif

- Aller dans `Outils raster > Remplir les cellules sans données`
  - Entrée : DTM
  - Maximum distance : 100 (nb de pixels voisins pour l'estimation)
  - Nb of smoothing : 10
  - FilledDTM.tif

## MNSn ou MNH (Modèle Numérique de Hauteur)

- Aller dans la Calculatrice Raster
- "Taper FilledDSM@1" - "FilledDTM@1"
- Sortie : nDSM.tif
- On a notre MNH à partir duquel déterminer la hauteur des arbres, par exemple