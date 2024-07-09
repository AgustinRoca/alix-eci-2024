import pandas as pd

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

def get_referred_company_name(texto_reclamo):
    companies = ['SierraVolt Energética Limitada', 'SierraVolt Energética', 'SierraV Segura', 'Aseguradora del Norte', 'Volterra Seguros']
    for company in companies:
        if company in texto_reclamo:
            return company
    return None

def any_word_in_clean_text(words, text):
    delete_chars = ['\r\n', ',', '.', '(', ')', '!', '?', '¿', '¡', ';', ':', '"', "'", '-']
    for char in delete_chars:
        text = text.replace(char, ' ')
    text = ' ' + text.lower() + ' '
    while '  ' in text:
        text = text.replace('  ', ' ')
    
    for word in words:
        if ' ' + word + ' ' in text:
            return True
    return False

def any_word_in_raw_text(words, text):
    text = text.lower()
    for word in words:
        if word in text:
            return True
    return False

def written_by_lawyer(texto_reclamo):   
    words = ['abogado', 'lic', 'estudio', 'legal', 'jurídico']
    for word in words:
        if word in texto_reclamo.lower():
            return True
    return False

def is_formal(texto_reclamo):
    informal_raw_words = [ "Pa'", "pa'"]
    informal_words = [
        'pa',
        'jodió',
        'quilombo',
        'jodidos',
        'corazón',
        'hola',
        'ojalá',
        'guita',
        're',
        'caliente'
    ]

    return (not any_word_in_clean_text(informal_words, texto_reclamo)) or (not any_word_in_raw_text(informal_raw_words, texto_reclamo))

def has_hollin(texto_reclamo):
    words = ['hollín', 'cenizas']
    return any_word_in_clean_text(words, texto_reclamo)

def do_cleaning_and_maintenance(texto_reclamo):
    words = ['limpieza', 'restauración', 'reforestación', 'mantenimiento']
    return any_word_in_clean_text(words, texto_reclamo)

def has_flora_damage(texto_reclamo):
    words = ['vegetación', 'flora', 'árboles', 'flores', 'arbustos', 'plantas', 'pasto', 'naturaleza', 'ambiente natural']
    return any_word_in_clean_text(words, texto_reclamo)

def has_emotional_damage(texto_reclamo):
    words = ['emocional', 'psicológico', 'psicológica', 'emocionalmente', 'psicológicamente', 'emocionales', 'psicológicos']
    return any_word_in_clean_text(words, texto_reclamo)

def has_economic_damage(texto_reclamo):
    words = ['económico', 'económica', 'económicos', 'económicas', 'económicamente']
    return any_word_in_clean_text(words, texto_reclamo)

def has_physical_damage(texto_reclamo):
    words = ['hospital', 'hospitalización', 'hospitalizado', 'hospitalizada', 'lesiones', 'salud', 'internación', 'internado', 'internada']
    return any_word_in_clean_text(words, texto_reclamo)

def has_fauna_damage(texto_reclamo):
    words = ['animal', 'fauna', 'mascota', 'mascotas', 'animales']
    return any_word_in_clean_text(words, texto_reclamo)

def has_crop_damage(texto_reclamo):
    words = ['cultivo', 'cultivos', 'cosecha', 'cosechas', 'agricultura']
    return any_word_in_clean_text(words, texto_reclamo)

def has_soil_damage(texto_reclamo):
    words = ['suelo', 'deterioro', 'deteriorada', 'deteriorado', 'deteriorados', 'deterioradas', 'erosionado', 'desgastado', 'erosión']
    return any_word_in_clean_text(words, texto_reclamo)

def has_insurance_coverage(texto_reclamo):
    words = ['no cubre']
    return not any_word_in_clean_text(words, texto_reclamo)

def has_evacuation(texto_reclamo):
    words = ['evacuación', 'evacuar']
    return any_word_in_clean_text(words, texto_reclamo)

def mentioned_negligence(texto_reclamo):
    words = ['negligencia', 'negligente', 'negligentes']
    return any_word_in_clean_text(words, texto_reclamo)

def is_angry(texto_reclamo):
    words = ['maldita', 'enojado', 'caliente', 'enojo', 'furioso', 'furiosa', 'enojada', 'furiosamente', 'inaceptable', 'intolerable', 'indignante', 'indignado', 'indignada', 'indignados', 'indignadas']
    return any_word_in_clean_text(words, texto_reclamo)

def main():
    df = pd.read_csv('data/clean_raw_data.csv')
    df['direccion'] = df['TextoReclamo'].apply(get_direccion_from_texto_reclamo)    
    df['referred_company'] = df['TextoReclamo'].apply(get_referred_company_name)
    df['written_by_lawyer'] = df['TextoReclamo'].apply(written_by_lawyer)
    df['formal'] = df['TextoReclamo'].apply(is_formal)
    df['hollin'] = df['TextoReclamo'].apply(has_hollin)
    df['cleaning_and_maintenance'] = df['TextoReclamo'].apply(do_cleaning_and_maintenance)
    df['flora_damage'] = df['TextoReclamo'].apply(has_flora_damage)
    df['emotional_damage'] = df['TextoReclamo'].apply(has_emotional_damage)
    df['economic_damage'] = df['TextoReclamo'].apply(has_economic_damage)
    df['physical_damage'] = df['TextoReclamo'].apply(has_physical_damage)
    df['fauna_damage'] = df['TextoReclamo'].apply(has_fauna_damage)
    df['crop_damage'] = df['TextoReclamo'].apply(has_crop_damage)
    df['soil_damage'] = df['TextoReclamo'].apply(has_soil_damage)
    df['insurance_coverage'] = df['TextoReclamo'].apply(has_insurance_coverage)
    df['evacuation'] = df['TextoReclamo'].apply(has_evacuation)
    df['negligence'] = df['TextoReclamo'].apply(mentioned_negligence)
    df['angry'] = df['TextoReclamo'].apply(is_angry)
    df['low_claim'] = df['ValorReclamo'] / df['valuacion_fiscal'] < 1.3
    df['has_mejoras'] = df['valuacion_mejoras'] > 0
    df.to_csv('data/clean_processed_data.csv', index=False)

if __name__ == '__main__':
    main()