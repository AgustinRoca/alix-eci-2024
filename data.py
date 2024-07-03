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
    df['TextoReclamo'] = df['TextoReclamo'].str.replace('\r\n', '\\n')

    missing_addresses = df[df['direccion'].isna()]
    missing_addresses['direccion'] = missing_addresses['TextoReclamo'].apply(get_direccion_from_texto_reclamo)
    df.update(missing_addresses)
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

def clean_text(df):
    texts = []
    for text, direccion, propietario in df[['TextoReclamo', 'direccion', 'Propietario']].values:

        text = text.lower()
        text = text.replace('\\n', ' ')
        text = text.replace(',', '')
        text = text.replace('.', '')
        text = text.replace(')', '')
        text = text.replace('(', '')
        text = text.replace('¡', '')
        text = text.replace('!', '')
        text = text.replace('?', '')
        text = text.replace('¿', '')

        while '  ' in text:
            text = text.replace('  ', ' ')
    
        # remove stopwords
        stop_words = ['un', 'y', 'su', 'que', 'en', 'por', 'a', 'el', 'la', 'una', 'con', 'es', 'no', 'los', 'para', 'ha', 'mi', 'de', 'me', 'del', 'se', 'las', 'como', 'este', 'ya', 'al', 'nos', 'lo', 'ende', 'o', 'han', 'esta', 'he', 'les', 'mí', 'sus', 'esto', 'está', 'él', 'si']
        for word in stop_words:
            spaced_word = ' ' + word + ' '
            text = text.replace(spaced_word, ' ')
            if text.startswith(word + ' '):
                text = text[len(word) + 1:]
            
        # remove direccion words from text
        direccion = direccion.lower()
        direccion = direccion.replace(',', '')
        text = ' '.join([word for word in text.split() if word not in direccion.split()])

        if type(propietario) == str:
            propietario = propietario.lower()
            propietario = propietario.replace(',', '')
            text = ' '.join([word for word in text.split() if word not in propietario.split()])


        for word in direccion.split():
            spaced_word = ' ' + word + ' '
            text = text.replace(spaced_word, ' ')
            if text.startswith(word + ' '):
                text = text[len(word) + 1:]
        

        common_words = ['incendio', 'forestal', 'terreno', 'propiedad', 'atención']
        for word in common_words:
            spaced_word = ' ' + word + ' '
            text = text.replace(spaced_word, ' ')
            if text.startswith(word + ' '):
                text = text[len(word) + 1:]

        text = ' '.join([word for word in text.split() if not word.startswith('$')])

        texts.append(text)

    df['cleaned_text'] = texts
    return texts


def pecentage_appearences_words(df):
    words = {}
    for text in df['cleaned_text']:
        words_appeared_this_text = set()
        for word in text.split():
            if word not in words_appeared_this_text:
                if word in words:
                    words[word] += 1
                else:
                    words[word] = 1
                words_appeared_this_text.add(word)
        
    words = {word: apps/len(df) for word, apps in words.items()}
    words = {k: v for k, v in sorted(words.items(), key=lambda item: item[1], reverse=True) if v > 0.05}
    return words

def written_by_lawyer(df):
    # 0 to 1 (probability)
    obvious_favorable_keywords = [
        'abogado',
        'abogada',
        'lic',
        'estudio',
        'legal',
        'jurídico',
    ]

    obvious_unfavorable_keywords = [
        'mi',
        'yo',
        'nuestro',
    ]

    slight_favorable_keywords = [
        'representada',
        'cliente'
    ]

    slight_unfavorable_keywords = [
        'soy',
    ]

    written_by_lawyer_list = []
    for text in df['cleaned_text']:
        degree=0.5
        step = 0.1
        for word in text.split():
            if word in obvious_favorable_keywords:
                degree = 1
                break
            if word in obvious_unfavorable_keywords:
                degree = 0
                break
            if word in slight_favorable_keywords:
                degree += step
            elif word in slight_unfavorable_keywords:
                degree -= step

        written_by_lawyer_list.append(degree)
    
    df['written_by_lawyer'] = written_by_lawyer_list
        


def predominant_feeling(df):
    # anger, fear, sadness, anguish, neutral

    anger_keywords = [
        'enojado',
        'enojada',
        'furioso',
        'furiosa',
        'furiosamente',
        'caliente',
        'intolerable'
    ]

    fear_keywords = [
        'miedo',
        'asustado',
        'asustada',
        'temor',
        'temeroso',
        'temerosa',
    ]

    sadness_keywords = [
        'triste',
        'tristeza',
        'llorar',
        'llorando',
        'lamentablemente',
        'lamentable'
    ]

    anguish_keywords = [
        'angustia',
        'angustiado',
        'angustiada',
        'angustiante',
        'congoja',
        'desazón',
        'inquietud'
    ]

    feelings = []
    for text in df['cleaned_text']:

        feeling_degrees = {
            'anger': 0,
            'fear': 0,
            'sadness': 0,
            'anguish': 0,
        }

        for word in text.split():
            if word in anger_keywords:
                feeling_degrees['anger'] += 1
            elif word in fear_keywords:
                feeling_degrees['fear'] += 1
            elif word in sadness_keywords:
                feeling_degrees['sadness'] += 1
            elif word in anguish_keywords:
                feeling_degrees['anguish'] += 1

        predominant = max(feeling_degrees, key=feeling_degrees.get)
        if feeling_degrees[predominant] == 0:
            predominant = 'neutral'
        feelings.append(predominant)
    df['predominant_feeling'] = feelings

def formality_level(df):
    obvious_favorable_keywords = [
        'respetuosamente',
        'atentamente',
        'sinceramente',
    ]

    obvious_unfavorable_keywords = [
        're',
        "pa'",
        'jodido',
        'jodidos',
        'diablo',
        'poquito'
    ]

    slight_favorable_keywords = [
        'favor',
    ]

    slight_unfavorable_keywords = [

    ]

    formalities = []
    for text in df['cleaned_text']:
        degree=0.5
        step = 0.1
        for word in text.split():
            if word in obvious_favorable_keywords:
                degree = 1
                break
            if word in obvious_unfavorable_keywords:
                degree = 0
                break
            if word in slight_favorable_keywords:
                degree += step
            elif word in slight_unfavorable_keywords:
                degree -= step
        
        formalities.append(degree)
    df['formality'] = formalities

def politeness_level(df):
    obvious_favorable_keywords = [
        'favor',
        'gracias',
        'rogamos',
        'agradezco',
        'apreciamos'
    ]

    obvious_unfavorable_keywords = [
       'culpa',
       'culpable',
       'diablo'
    ]

    slight_favorable_keywords = [
        
    ]

    slight_unfavorable_keywords = [

    ]

    politenesses = []
    for text in df['cleaned_text']:
        degree=0.5
        step = 0.1
        for word in text.split():
            if word in obvious_favorable_keywords:
                degree = 1
                break
            if word in obvious_unfavorable_keywords:
                degree = 0
                break
            if word in slight_favorable_keywords:
                degree += step
            elif word in slight_unfavorable_keywords:
                degree -= step

        politenesses.append(degree)
    df['politeness'] = politenesses

def referred_company_name(df):
    possible_names = [
        'SierraVolt Energética Limitada',
        'SierraVolt Energética',
        'SierraV Segura',
        'Aseguradora Norte',
        'Volterra Seguros'
    ]

    names = []
    for text in df['cleaned_text']:
        found = False
        for name in possible_names:
            if name.lower() in text.lower():
                names.append(name)
                found = True
                break
        if not found:
            names.append(None)
    df['referred_company_name'] = names

def psychological_impact_mentioned(df):
    obvious_favorable_keywords = [
        'psicológico',
        'psicológica',
        'psicólogo',
        'psicóloga',
        'psicología',
        'emocional',
        'emocionalmente',
    ]

    obvious_unfavorable_keywords = [
    ]

    slight_favorable_keywords = [
        'estrés',
        'ansiedad',
        'depresión',
        'trauma',
        'traumático',
        'traumática',
    ]

    slight_unfavorable_keywords = [
    ]

    psychological_impacts = []
    for text in df['cleaned_text']:
        degree=0
        step = 0.1
        for word in text.split():
            if word in obvious_favorable_keywords:
                degree = 1
                break
            if word in obvious_unfavorable_keywords:
                degree = 0
                break
            if word in slight_favorable_keywords:
                degree += step
            elif word in slight_unfavorable_keywords:
                degree -= step

        psychological_impacts.append(degree)

    df['psychological_impact'] = psychological_impacts
        

def economic_impact_mentioned(df):
    obvious_favorable_keywords = [
        'dinero',
        'económico',
        'económica',
        'económicos',
        'económicas',
        'economía',
        'financiero',
        'financiera',
        'gastos',
        'gasto',
        'reparación',
        'costos',
        'restauración'
    ]

    obvious_unfavorable_keywords = [
    ]

    slight_favorable_keywords = [
        'pérdida',
        'perdida',
        'perdidas',
        'pérdidas',
        'daño',
        'daños',
        'deuda',
        'deudas'
    ]

    slight_unfavorable_keywords = [
    ]

    economic_impacts = []
    for text in df['cleaned_text']:
        degree=0.5
        step = 0.1
        for word in text.split():
            if word in obvious_favorable_keywords:
                degree = 1
                break
            if word in obvious_unfavorable_keywords:
                degree = 0
                break
            if word in slight_favorable_keywords:
                degree += step
            elif word in slight_unfavorable_keywords:
                degree -= step

        economic_impacts.append(degree)
    df['economic_impact'] = economic_impacts