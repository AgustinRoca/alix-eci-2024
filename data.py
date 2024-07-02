import pandas as pd
import json
from pyproj import Proj, Transformer
from tqdm import tqdm

def get_direccion_from_texto_reclamo(texto_reclamo):
    phrases = ['situado en', 'lote en', 'ubicado en', 'terreno urbano en', 'terreno en', 'situada en', 'ubicada en', 'vivienda en', 'localizado en', 'propiedad en', 'lote urbano en']
    indexes = {}
    for phrase in phrases:
        phrase_words = ' '+phrase+' '
        if phrase_words in texto_reclamo:
            indexes[phrase] = texto_reclamo.find(phrase_words) +1
    
    # Get the phrase with the lowest index
    phrase = min(indexes, key=indexes.get)
    if phrase in texto_reclamo:
        address = texto_reclamo.split(phrase)[1]
        index = 0
        if 'Leandro N.' in address:
            index +=1
        address = address.split('.')[index].strip()
        if address.startswith('la ') or address.startswith('el '):
            address = address[3:]
        return address
    return None

def get_claims(file_path='data/Claims-WorkingFile_v2.csv'):
    df = pd.read_csv(file_path)
    # Clean the idParcela column
    df['idParcela'] = df['idParcela'].str.replace('-SAN ROQUE', '')
    df['idParcela'] = df['idParcela'].str.replace('-SANTIAGO', '')
    df['abogado'] = df['TextoReclamo'].str.contains('abogado', case=False, na=False)

    # Extract the address from the claim text when the address is not provided
    missing_addresses = df[df['direccion'].isna()]
    missing_addresses['direccion'] = missing_addresses['TextoReclamo'].apply(get_direccion_from_texto_reclamo)
    df.update(missing_addresses)
    # Add a column to identify if the claim is angry by words like "enojado" or "furioso"
    angry_words = ['enoj', 'furio', 'indigna', 'molest', 'enfad', 'irrit']
    df['enojado'] = df['TextoReclamo'].str.contains('|'.join(angry_words), case=False, na=False)
    return df

def get_parcels_data(file_path):
    data = json.load(open(file_path))
    return clean_parcels_data(data)

def clean_parcels_data(parcels_data):
    cleaned_data = []
    for feature in tqdm(parcels_data['features']):
        parcel = {}
        parcel['id'] = f"{feature['properties']['par_idparcela']}"
        parcel['tipo'] = feature['properties']['Tipo_Parcela']
        parcel['tipo_val'] = feature['properties']['Tipo_Valuacion']
        parcel['estado'] = feature['properties']['Estado']
        parcel['fxf'] = feature['properties']['fxf']
        parcel['vut'] = feature['properties']['vut_vigente']
        parcel['valuacion'] = feature['properties']['Valuacion']
        parcel['superficie_urbano'] = feature['properties']['Superficie_Tierra_Urbana']
        parcel['valuacion_urbano'] = feature['properties']['Valuacion_Tierra_Urbana']
        parcel['superficie_rural'] = feature['properties']['Superficie_Tierra_Rural']
        parcel['valuacion_rural'] = feature['properties']['Valuacion_Tierra_Rural']
        parcel['superficie_mejoras'] = feature['properties']['Superficie_Mejoras']
        parcel['valuacion_mejoras'] = feature['properties']['Valuacion_Mejoras']
        parcel['departamento'] = feature['properties']['departamento']
        parcel['pedania'] = feature['properties']['pedania']
        parcel['localidad'] = feature['properties']['localidad']
        parcel['bbox'] = [translate_to_lat_lon(utm) for utm in zip(feature['bbox'][::2], feature['bbox'][1::2])] if 'bbox' in feature else None
        cleaned_data.append(parcel)

    df = pd.DataFrame(cleaned_data)
    return df

def translate_to_lat_lon(utm_coordinates):
    x,y = utm_coordinates[0], utm_coordinates[1]
    # Define the Gauss-Krüger faja 4 projection (EPSG:22174)
    gauss_kruger_proj = Proj('EPSG:22174')

    # Define the WGS84 projection
    wgs84_proj = Proj(proj='latlong', datum='WGS84')

    # Define the transformer for converting to WGS84
    transformer = Transformer.from_proj(gauss_kruger_proj, wgs84_proj, always_xy=True)

    # Convert the coordinates to latitude and longitude (WGS84)
    lat, lon = transformer.transform(x, y)
    return lon, lat