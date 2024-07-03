import pandas as pd

from data import get_claims, get_parcels_data


claims_df = get_claims()
ground_truth_claims = claims_df[claims_df['Validado'] == 'X']

sanroque_parcels = get_parcels_data('data/parcelas_sanroque.json')
santiago_parcels = get_parcels_data('data/parcelas_santiago.json')
parcels = pd.concat([sanroque_parcels, santiago_parcels])
merged_df = pd.merge(parcels, claims_df, left_on='id', right_on='idParcela', how='right')

merged_df.to_csv('data/clean_data.csv', index=False)