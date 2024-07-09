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

def abogado(texto_reclamo):   
    words = ['abogado', 'lic', 'estudio', 'legal', 'jurídico', 'legales']
    for word in words:
        if word in texto_reclamo.lower():
            return True
    return False

def formal(texto_reclamo):
    informal_raw_words = [ "Pa'", "pa'", "pa'l"]
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
        'caliente',
        'garrón',
        'percha',
        'tujes', 
    ]

    return (not any_word_in_clean_text(informal_words, texto_reclamo)) or (not any_word_in_raw_text(informal_raw_words, texto_reclamo))

def hollin(texto_reclamo):
    words = ['hollín']
    return any_word_in_clean_text(words, texto_reclamo)

def cenizas(texto_reclamo):
    words = ['cenizas']
    return any_word_in_clean_text(words, texto_reclamo)

def humo(texto_reclamo):
    words = ['humo']
    return any_word_in_clean_text(words, texto_reclamo)

def evaluacion(texto_reclamo):
    words = ['evaluación']
    return any_word_in_clean_text(words, texto_reclamo)

def evacuacion(texto_reclamo):
    words = ['evacuación', 'evacuar']
    return any_word_in_clean_text(words, texto_reclamo)

def limpieza(texto_reclamo):
    words = ['limpieza']
    return any_word_in_clean_text(words, texto_reclamo)

def restauracion(texto_reclamo):
    words = ['restauración']
    return any_word_in_clean_text(words, texto_reclamo)

def reparacion(texto_reclamo):
    words = ['reparación']
    return any_word_in_clean_text(words, texto_reclamo)

def restitucion(texto_reclamo):
    words = ['restitución']
    return any_word_in_clean_text(words, texto_reclamo)

def reforestacion(texto_reclamo):
    words = ['reforestación']
    return any_word_in_clean_text(words, texto_reclamo)

def recuperacion(texto_reclamo):
    words = ['recuperación']
    return any_word_in_clean_text(words, texto_reclamo)

def reconstruccion(texto_reclamo):
    words = ['reconstrucción']
    return any_word_in_clean_text(words, texto_reclamo)

def compensacion(texto_reclamo):
    words = ['compensación']
    return any_word_in_clean_text(words, texto_reclamo)

def medidas_preventivas(texto_reclamo):
    words = ['medidas preventivas', 'prevenir', 'prevención']
    return any_word_in_clean_text(words, texto_reclamo)

def economico(texto_reclamo):
    words = ['económico', 'económica', 'económicos', 'económicas', 'económicamente', 'comercial']
    return any_word_in_clean_text(words, texto_reclamo)

def vegetacion(texto_reclamo):
    words = ['vegetación', 'flora', 'árboles', 'flores', 'arbustos', 'plantas', 'pasto', 'naturaleza', 'ambiente natural']
    return any_word_in_clean_text(words, texto_reclamo)

def animales(texto_reclamo):
    words = ['animales', 'fauna', 'mascotas', 'mascota', 'animal']
    return any_word_in_clean_text(words, texto_reclamo)

def madera(texto_reclamo):
    words = ['madera', 'maderas']
    return any_word_in_clean_text(words, texto_reclamo)

def suelo(texto_reclamo):
    words = ['suelo', 'deterioro', 'deteriorada', 'deteriorado', 'deteriorados', 'deterioradas', 'erosionado', 'desgastado', 'erosión']
    return any_word_in_clean_text(words, texto_reclamo)

def aire(texto_reclamo):
    words = ['aire']

def marcas(texto_reclamo):
    words = ['marcas']
    return any_word_in_clean_text(words, texto_reclamo)

def valor(texto_reclamo):
    words = ['valor']
    return any_word_in_clean_text(words, texto_reclamo)

def futura_salud(texto_reclamo):
    words = ['salud', 'calidad de vida', 'pueda afectar a', 'bienestar']
    return any_word_in_clean_text(words, texto_reclamo)

def emocional(texto_reclamo):
    words = ['emocional', 'psicológico', 'psicológica', 'emocionalmente', 'psicológicamente', 'emocionales', 'psicológicos']
    return any_word_in_clean_text(words, texto_reclamo)

def fisico(texto_reclamo):
    words = ['hospital', 'hospitalización', 'hospitalizado', 'hospitalizada', 'lesiones', 'internación', 'internado', 'internada', 'médicos']
    return any_word_in_clean_text(words, texto_reclamo)

def cultivos(texto_reclamo):
    words = ['cultivo', 'cultivos', 'cosecha', 'cosechas', 'agricultura']
    return any_word_in_clean_text(words, texto_reclamo)

def cobertura(texto_reclamo):
    words = ['no cubre']
    return not any_word_in_clean_text(words, texto_reclamo)

def negligencia(texto_reclamo):
    words = ['negligencia', 'negligente', 'negligentes']
    return any_word_in_clean_text(words, texto_reclamo)

def enojado(texto_reclamo):
    words = ['maldita', 'enojado', 'caliente', 'enojo', 'furioso', 'furiosa', 'enojada', 'furiosamente', 'inaceptable', 'intolerable', 'indignante', 'indignado', 'indignada', 'indignados', 'indignadas']
    return any_word_in_clean_text(words, texto_reclamo)

def interrupcion_actividades(texto_reclamo):
    words = ['interrupción de actividades', 'interrumpir', 'interrumpido', 'interrumpida', 'interrumpidos', 'interrumpidas', 'posibilidad de construir', 'desarrollo']
    return any_word_in_clean_text(words, texto_reclamo)

def responsabilidad(texto_reclamo):
    words = ['responsabilidad', 'responsable', 'responsables', 'culpa', 'culpable', 'culpables']
    return any_word_in_clean_text(words, texto_reclamo)

def estructural(texto_reclamo):
    words = ['estructural', 'estructurales']
    return any_word_in_clean_text(words, texto_reclamo)

def main():
    df = pd.read_csv('data/clean_raw_data.csv')
    df['direccion'] = df['TextoReclamo'].apply(get_direccion_from_texto_reclamo)    
    df['empresa'] = df['TextoReclamo'].apply(get_referred_company_name)
    df['reclamo_bajo'] = df['ValorReclamo'] / df['valuacion_fiscal'] < 1.3
    df['mejoras'] = df['valuacion_mejoras'] > 0
    df['abogaod'] = df['TextoReclamo'].apply(abogado)
    df['formal'] = df['TextoReclamo'].apply(formal)
    df['hollin'] = df['TextoReclamo'].apply(hollin)
    df['cenizas'] = df['TextoReclamo'].apply(cenizas)
    df['humo'] = df['TextoReclamo'].apply(humo)
    df['evaluacion'] = df['TextoReclamo'].apply(evaluacion)
    df['evacuacion'] = df['TextoReclamo'].apply(evacuacion)
    df['limpieza'] = df['TextoReclamo'].apply(limpieza)
    df['restauracion'] = df['TextoReclamo'].apply(restauracion)
    df['reparacion'] = df['TextoReclamo'].apply(reparacion)
    df['restitucion'] = df['TextoReclamo'].apply(restitucion)
    df['reforestacion'] = df['TextoReclamo'].apply(reforestacion)
    df['recuperacion'] = df['TextoReclamo'].apply(recuperacion)
    df['reconstruccion'] = df['TextoReclamo'].apply(reconstruccion)
    df['compensacion'] = df['TextoReclamo'].apply(compensacion)
    df['medidas_preventivas'] = df['TextoReclamo'].apply(medidas_preventivas)
    df['economico'] = df['TextoReclamo'].apply(economico)
    df['interrupcion_actividades'] = df['TextoReclamo'].apply(interrupcion_actividades)
    df['animales'] = df['TextoReclamo'].apply(animales)
    df['vegetacion'] = df['TextoReclamo'].apply(vegetacion)
    df['cultivos'] = df['TextoReclamo'].apply(cultivos)
    df['madera'] = df['TextoReclamo'].apply(madera)
    df['suelo'] = df['TextoReclamo'].apply(suelo)
    df['marcas'] = df['TextoReclamo'].apply(marcas)
    df['estructural'] = df['TextoReclamo'].apply(estructural)
    df['valor'] = df['TextoReclamo'].apply(valor)
    df['futura_salud'] = df['TextoReclamo'].apply(futura_salud)
    df['emocional'] = df['TextoReclamo'].apply(emocional)
    df['fisico'] = df['TextoReclamo'].apply(fisico)
    df['cobertura'] = df['TextoReclamo'].apply(cobertura)
    df['negligencia'] = df['TextoReclamo'].apply(negligencia)
    df['enojado'] = df['TextoReclamo'].apply(enojado)
    df['responsabilidad'] = df['TextoReclamo'].apply(responsabilidad)

    df.to_csv('data/clean_processed_data.csv', index=False)

if __name__ == '__main__':
    main()