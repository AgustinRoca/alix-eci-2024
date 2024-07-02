import pandas as pd

from data import get_claims, get_parcels_data
from model import predict_valuacion_danios
from sklearn.metrics import mean_absolute_error


claims_df = get_claims()
# Get the claims that are validated
ground_truth_claims = claims_df[claims_df['Validado'] == 'X']

sanroque_parcels = get_parcels_data('data/parcelas_sanroque.json')
santiago_parcels = get_parcels_data('data/parcelas_santiago.json')
parcels = pd.concat([sanroque_parcels, santiago_parcels])
merged_df = pd.merge(parcels, claims_df, left_on='id', right_on='idParcela', how='right')

# get column names
print(merged_df.columns)
print(merged_df[['bbox']].head())

y_true = ground_truth_claims['Valuacion_Danios']
y_pred = ground_truth_claims.apply(predict_valuacion_danios, axis=1)

mae = mean_absolute_error(y_true, y_pred)
print(f'Mean Absolute Error: {mae}')