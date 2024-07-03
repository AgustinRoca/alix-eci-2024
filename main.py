import pandas as pd
import math

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
        stop_words = ['un', 'y', 'su', 'que', 'en', 'por', 'a', 'el', 'la', 'una', 'con', 'es', 'no', 'los', 'para', 'ha', 'mi', 'de', 'me', 'del', 'se', 'las', 'como', 'este', 'ya', 'al', 'nos', 'lo', 'ende', 'o', 'han', 'esta', 'he']
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

    df['cleaned_texts'] = texts
    return texts


def pecentage_appearences_words(df):
    words = {}
    for text in df['cleaned_texts']:
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

        

df = pd.read_csv('data/clean_data.csv')
df['id'] = df['id'].astype('Int64')
df['vut'] = df['vut'].astype('Int64')

clean_text(df)
appearences = pecentage_appearences_words(df)
print(appearences)
