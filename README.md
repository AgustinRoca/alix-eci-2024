# Competencia AlixPartners ECI 2024

## SierraVolt Energética Limitada: Estimación de daño en patrimonio producido por incendios

### Preprocesamiento

#### Archivos necesarios

- Claims-WorkingFile_v2.csv
- .dbf, .prj, .shp, .shx de las parcelas de San Roque y Santiago
- Imagenes TIFF mostrando DNBR y NDVI que incluyan las zonas de San Roque y Santiago (Calculadas utilizando QGIS)

#### Scripts

-   `python3 clean_raw_data.py`: Matchea los datos de Claims-WorkingFile_v2.csv con los archivos .shp de las parcelas de
 San Roque y Santiago. También incluye el DNBR y NDVI promedio de cada parcela. La salida es un archivo .csv

-   `python3 process_data.py`: Hace procesamiento del texto de reclamo y extrae features. La salida es un archivo .csv

### Predicción de daño

-   `python3 model.py`: Contiene la formula utilizada para el modelo de predicción de daño. La salida es un archivo .csv
    con el formato adecuado para subirlo a Kaggle
