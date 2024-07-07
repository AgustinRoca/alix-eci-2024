import pandas as pd

from model import predict_valuacion_danios 

df = pd.read_csv('data/clean_raw_data.csv')
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