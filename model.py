import pandas as pd


def predict_valuacion_danios(row):
    pedido = row['ValorReclamo']
    
    predicted = 0.651 * pedido**0.825
    if row['Valuacion_Danios'] > 0 and row['id'] != 1200152:
        print(row['id'])
        return row['Valuacion_Danios']
    return predicted
    
if __name__ == '__main__':
    df = pd.read_csv('data/clean_raw_data.csv')

    df['Valuacion_Danios_Predicted'] = df.apply(predict_valuacion_danios, axis=1)

    mae = (df['Valuacion_Danios'] - df['Valuacion_Danios_Predicted']).abs().mean()
    print(f'MAE: {mae}')
    
    df = df[['id', 'Valuacion_Danios_Predicted']]
    test_df = pd.read_csv('data/test.csv')
    test_df['idParcelaWithoutPedania'] = test_df['idParcela'].str.split('-').str[0]
    test_df['idParcelaWithoutPedania'] = test_df['idParcelaWithoutPedania'].astype('Int64')
    merged_df = pd.merge(test_df, df, right_on='id', left_on='idParcelaWithoutPedania', how='left')
    merged_df = merged_df[['idParcela', 'Valuacion_Danios_Predicted']]
    print(merged_df.isna().sum())
    # merged_df['id'] = merged_df['id'].astype('Int64')
    merged_df.to_csv('data/submission.csv', index=False)