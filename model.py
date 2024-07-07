import pandas as pd


def predict_valuacion_danios(row):
    # pedido = row['ValorReclamo']
    valuacion_mejoras = row['valuacion_mejoras']
    estado = int(row['estado'] == 'edificado noph')
    localidad = int(row['localidad'] == 'villa icho cruz')
    sep_ndvi = row['sep_ndvi']
    pedania = int(row['pedania'] == 'santiago')
    coefs = [1,103,342.49, 254012.42, 236936.53, 178470.58, 157821.80, 148291.58, 133447.29, 127187.62, 111916.25, 103152.23,  91832.48]
    values = [1, valuacion_mejoras**2, estado * sep_ndvi, valuacion_mejoras * localidad, valuacion_mejoras * sep_ndvi, estado * localidad, localidad * pedania, sep_ndvi ** 2, valuacion_mejoras * pedania, localidad, valuacion_mejoras * estado]
    predicted = sum([coef * value for coef, value in zip(coefs, values)])

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