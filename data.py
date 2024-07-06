import pandas as pd
import json
from tqdm import tqdm
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import textstat

# IDEAS: 
# - written_by_lawyer (abogado, lic, estudio, legal, jurídico)
# - sentiment (sentiment analysis)
# - formality_level (flesch reading ease)
# - referred_company_name (SierraVolt Energética Limitada, SierraVolt Energética, SierraV Segura, Aseguradora Norte, Volterra Seguros)
# - psychological_impact_mentioned
# - economic_impact_mentioned
# - physical_impact_mentioned (hospital, hospitalización, hospitalizado, hospitalizada, lesiones, salud, internación, internado, internada)

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
