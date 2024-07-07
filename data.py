import pandas as pd

def written_by_lawyer(texto_reclamo):   
    words = ['abogado', 'lic', 'estudio', 'legal', 'jurídico']
    for word in words:
        if word in texto_reclamo.lower():
            return True
    return False

def get_direccion_from_texto_reclamo(texto_reclamo):
    phrases = ['situado en', 'lote en', 'ubicado en', 'terreno urbano en', 'terreno rural en', 'terreno en', 'situada en', 'ubicada en', 'vivienda en', 'localizado en', 'propiedad en', 'lote urbano en', 'terrenito urbano en', 'terrenito en', 'predio rural en', 'un campo en', 'predio urbano en', 'dirección justita es']
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

def classify_emotion(text):
    text_lower = text.lower()
    if any(word in text_lower for word in ["preocupación", "angustia", "dolor", "triste", "lamento", "devastó", "pérdida"]):
        return "tristeza"
    elif any(word in text_lower for word in ["negligencia", "accidente", "enojado", "indignado", "molesto", "fue tan feroz", "se pudo haber prevenido"]):
        return "enojo"
    elif any(word in text_lower for word in ["gracias", "agradecido", "aprecio", "reconocimiento", "su apoyo", "cordialmente", "distinguidos"]):
        return "agradecimiento"
    else:
        return "neutral"

def get_formality_level(texto_reclamo):
    delete_chars = ['\r\n', ',', '.', '(', ')', '!', '?', '¿', '¡', ';', ':', '"', "'"]
    for char in delete_chars:
        texto_reclamo = texto_reclamo.replace(char, ' ')
    texto_reclamo = ' ' + texto_reclamo.lower() + ' '
    while '  ' in texto_reclamo:
        texto_reclamo = texto_reclamo.replace('  ', ' ')

    formal_words = [
        'indemnización',
        'agradecemos',
        'jurídico',
        'acuerdo',
        'abogado',
        'restauración',
        'resolución',
        'instrucciones',
        'acciones',
        'inmueble',
        'abogados',
        'afrontar',
        'incidente',
        'solución',
        'evacuación'
    ]

    informal_words = [
        'ya',
        'pa',
        'saludos',
        'ahora',
        'jodió',
        'acá',
        'saludo',
        'quilombo',
        'jodidos',
        'corazón',
        'hola',
        'ojalá',
        'ahí',
        'guita'
    ]

    formal_count = 0
    informal_count = 0

    for word in formal_words:
        formal_count += texto_reclamo.split().count(word)

    for word in informal_words:
        informal_count += texto_reclamo.split().count(word)



    if formal_count > 1.1 * informal_count:
        return 'formal'
    elif informal_count > 1.1 * formal_count:
        return 'informal'
    else:
        return 'neutral'

def any_word_in_text(words, text):
    delete_chars = ['\r\n', ',', '.', '(', ')', '!', '?', '¿', '¡', ';', ':', '"', "'"]
    for char in delete_chars:
        text = text.replace(char, ' ')
    text = ' ' + text.lower() + ' '
    while '  ' in text:
        text = text.replace('  ', ' ')
    
    for word in words:
        if ' ' + word + ' ' in text:
            return True
    return False

def get_referred_company_name(texto_reclamo):
    companies = ['SierraVolt Energética Limitada', 'SierraVolt Energética', 'SierraV Segura', 'Aseguradora del Norte', 'Volterra Seguros']
    for company in companies:
        if company in texto_reclamo:
            return company
    return None

def get_psychological_impact_mentioned(texto_reclamo):
    words = ['psicológico', 'emocional']
    return any_word_in_text(words, texto_reclamo)

def get_economic_impact_mentioned(texto_reclamo):
    words = ['económico', 'dinero', 'costo', 'gasto', 'presupuesto', 'financiero', 'finanzas']
    return any_word_in_text(words, texto_reclamo)

def get_physical_impact_mentioned(texto_reclamo):
    words = ['hospital', 'hospitalización', 'hospitalizado', 'hospitalizada', 'lesiones', 'salud', 'internación', 'internado', 'internada']
    return any_word_in_text(words, texto_reclamo)

def main():
    df = pd.read_csv('data/clean_raw_data.csv')
    df['direccion'] = df['TextoReclamo'].apply(get_direccion_from_texto_reclamo)    
    df['written_by_lawyer'] = df['TextoReclamo'].apply(written_by_lawyer)
    df['emotion'] = df['TextoReclamo'].apply(classify_emotion)
    df['formality_level'] = df['TextoReclamo'].apply(get_formality_level)
    df['referred_company'] = df['TextoReclamo'].apply(get_referred_company_name)
    df['psychological_impact_mentioned'] = df['TextoReclamo'].apply(get_psychological_impact_mentioned)
    df['economic_impact_mentioned'] = df['TextoReclamo'].apply(get_economic_impact_mentioned)
    df['physical_impact_mentioned'] = df['TextoReclamo'].apply(get_physical_impact_mentioned)
    df.to_csv('data/clean_processed_data.csv', index=False)

if __name__ == '__main__':
    main()