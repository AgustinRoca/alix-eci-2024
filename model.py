import pandas as pd
import math

def predict_valuacion_danios(row):
    valuacion = row['valuacion_fiscal']
    dnbr = row['dnbr_mean']
    ratio = row['ValorReclamo'] / valuacion

    if ratio > 10:
        if dnbr > 0.1:
            coef = 10
        elif dnbr > 0:
            coef = 9
        elif dnbr > -0.1:
            coef = 6
        else:
            coef = 3
    else: 
        coef = 0

    predicted = valuacion * coef * 0.09
    predicted = round(predicted, 4)
    predicted = predicted if predicted > 0 else 0

    if row['Valuacion_Danios'] > 0:
        return row['Valuacion_Danios']
    return predicted

if __name__ == '__main__':
    df = pd.read_csv('data/clean_processed_data.csv')
    test_df = pd.read_csv('data/test.csv')
    df.drop(columns=['idParcela'], inplace=True)

    test_df['id'] = test_df['idParcela'].str.split('-').str[0]
    test_df['id'] = test_df['id'].astype('Int64')

    merged_df = pd.merge(test_df, df, right_on='id', left_on='id', how='left')
    merged_df['Valuacion_Danios_Predicted'] = merged_df.apply(predict_valuacion_danios, axis=1)
    merged_df = merged_df[['idParcela', 'Valuacion_Danios_Predicted']]
    # fill NaN values with 0
    merged_df['Valuacion_Danios_Predicted'].fillna(0, inplace=True)
    merged_df.to_csv('data/submission.csv', index=False)