import pandas as pd


def predict_valuacion_danios(row):
    prediction = row['politeness'] - row['formality']
    return prediction * 1e6
    
if __name__ == '__main__':
    df = pd.read_csv('data/processed_data_train.csv')
    df['Valuacion_Danios_Predicted'] = df.apply(predict_valuacion_danios, axis=1)
    mae = (df['Valuacion_Danios'] - df['Valuacion_Danios_Predicted']).abs().mean()
    print(f'MAE: {mae}')