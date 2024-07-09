import pandas as pd


def predict_valuacion_danios(row):
    # pedido = row['ValorReclamo']
    valuacion = row['valuacion_fiscal']

    es_urbano = row['tipo'] == 'urbano'
    tiene_abogado = row['written_by_lawyer']
    es_formal = row['formal']
    tiene_hollin = row['hollin']
    hizo_limpieza = row['cleaning_and_maintenance']
    tiene_danio_flora = row['flora_damage']
    tiene_danio_emocional = row['emotional_damage']
    tiene_danio_economico = row['economic_damage']
    tiene_danio_fisico = row['physical_damage']
    tiene_danio_fauna = row['fauna_damage']
    tiene_danio_cosecha = row['crop_damage']
    tiene_danio_suelo = row['soil_damage']
    tiene_cobertura_seguro = row['insurance_coverage']
    necesita_evacuacion = row['evacuation']
    menciona_negligencia = row['negligence']
    esta_enojado = row['angry']
    reclamo_bajo = row['low_claim']
    tiene_mejoras = row['has_mejoras']
    dnbr = row['dnbr']
    es_baldio = row['estado']
    
    suma = 0
    suma += 1 if es_urbano else 0
    suma += 0 if tiene_abogado else 1
    suma += 0 if es_formal else 1
    suma += 1 if tiene_hollin else 0
    suma += 1 if hizo_limpieza else 0
    suma += 1 if tiene_danio_flora else 0
    suma += 1 if tiene_danio_emocional else 0
    suma += 2 if tiene_danio_economico else 0
    suma += 4 if tiene_danio_fisico else 0
    suma += 4 if tiene_danio_fauna else 0
    suma += 1 if tiene_danio_cosecha else 0
    suma += 1 if tiene_danio_suelo else 0
    # suma += 0 if tiene_cobertura_seguro else -1
    suma += 1 if necesita_evacuacion else 0
    suma += 1 if menciona_negligencia else 0
    suma += 1 if esta_enojado else 0
    # suma += 0 if reclamo_bajo else 1
    suma += 1 if tiene_mejoras else 0
    suma += 0 if es_baldio else 1
    if dnbr > 0.05:
        suma += 4
    elif dnbr > 0:
        suma += 2

    # if reclamo_bajo:
    #     predicted = valuacion * 20
    # elif not tiene_cobertura_seguro:
    #     predicted = 0
    # else:
    suma = max(suma, 6)
    predicted = valuacion * 0.9 * suma / 10

    if row['Valuacion_Danios'] > 0:
        return row['Valuacion_Danios']
    return predicted
    
if __name__ == '__main__':
    df = pd.read_csv('data/clean_processed_data.csv')

    df['Valuacion_Danios_Predicted'] = df.apply(predict_valuacion_danios, axis=1)

    mae = (df['Valuacion_Danios'] - df['Valuacion_Danios_Predicted']).abs().mean()
    print(f'MAE: {mae}')
    
    df = df[['id', 'Valuacion_Danios_Predicted']]
    test_df = pd.read_csv('data/test.csv')
    test_df['idParcelaWithoutPedania'] = test_df['idParcela'].str.split('-').str[0]
    test_df['idParcelaWithoutPedania'] = test_df['idParcelaWithoutPedania'].astype('Int64')
    merged_df = pd.merge(test_df, df, right_on='id', left_on='idParcelaWithoutPedania', how='left')
    merged_df = merged_df[['idParcela', 'Valuacion_Danios_Predicted']]
    # merged_df['id'] = merged_df['id'].astype('Int64')
    merged_df.to_csv('data/submission.csv', index=False)