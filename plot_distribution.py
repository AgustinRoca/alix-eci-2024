import pandas as pd
import matplotlib.pyplot as plt

def test_model(row):
    reclamo = row['ValorReclamo']
    valuacion = row['valuacion']
    dnbr = row['dnbr']
    sep_ndvi = row['sep_ndvi']
    nov_ndvi = row['nov_ndvi']
    diff_ndvi = nov_ndvi - sep_ndvi
    actual = row['Valuacion_Danios']
    
 

df = pd.read_csv('data/clean_raw_data.csv')
df = df[df['Validado'] == 'X']
wierd_row = df[df['Valuacion_Danios'] > df['ValorReclamo']]
df = df[df['Valuacion_Danios'] <= df['ValorReclamo']]

# # plot valuacion vs valuacion danios
# plt.scatter(df['ValorReclamo'], df['Valuacion_Danios'])
# # plt.scatter(wierd_row['ValorReclamo'], wierd_row['Valuacion_Danios'], color='red')
# plt.xlabel('Valor Reclamo')
# plt.ylabel('Valuacion Danios')
# plt.xscale('log')
# plt.yscale('log')
# plt.title('Valor Reclamo vs Valuacion Danios')
# plt.show()

# # plot dnbr vs (valuacion danios - valuacion)
# plt.scatter(df['dnbr'], df['Valuacion_Danios'] - df['ValorReclamo'])
# # plt.scatter(wierd_row['dnbr'], wierd_row['Valuacion_Danios'] - wierd_row['ValorReclamo'], color='red')
# plt.xlabel('DNBR')
# plt.ylabel('Valuacion Danios')
# plt.title('DNBR vs Valuacion Danios')
# plt.show()

# plot sep_ndvi vs valuacion
# plt.scatter(df['sep_ndvi'], df['valuacion'])
# plt.xlabel('September NDVI')
# plt.ylabel('Valuacion')
# plt.title('September NDVI vs Valuacion')
# plt.show()

# # plot sep_ndvi vs (valuacion danios - valuacion)
# plt.scatter(df['sep_ndvi'], df['Valuacion_Danios'] - df['ValorReclamo'])
# plt.xlabel('September NDVI')
# plt.ylabel('Valuacion Danios')
# plt.title('September NDVI vs Valuacion Danios')
# plt.show()

# # plot nov_ndvi vs (valuacion danios - valuacion)
# plt.scatter(df['nov_ndvi'], df['Valuacion_Danios'] - df['ValorReclamo'])
# plt.xlabel('November NDVI')
# plt.ylabel('Valuacion Danios')
# plt.title('November NDVI vs Valuacion Danios')
# plt.show()

# # plot (nov_ndvi - sep_ndvi) vs (valuacion danios - valuacion)
# plt.scatter(df['nov_ndvi'] - df['sep_ndvi'], df['Valuacion_Danios'] - df['ValorReclamo'])
# # plt.scatter(wierd_row['nov_ndvi'] - wierd_row['sep_ndvi'], wierd_row['Valuacion_Danios'] - wierd_row['ValorReclamo'], color='red')
# plt.xlabel('November NDVI - September NDVI')
# plt.ylabel('Valuacion Danios')
# plt.title('November NDVI - September NDVI vs Valuacion Danios')
# plt.show()

# plot predicted - valuacion danios vs number of samples
df['predicted'] = df.apply(test_model, axis=1)
df['diff'] = df['Valuacion_Danios'] - df['predicted']
wierd_row['predicted'] = wierd_row.apply(test_model, axis=1)
wierd_row['diff'] = wierd_row['Valuacion_Danios'] - wierd_row['predicted']

plt.scatter(df.index, df['diff'])
plt.scatter(wierd_row.index, wierd_row['diff'], color='red')
plt.xlabel('Sample number')
plt.ylabel('Valuacion Danios - Predicted')
plt.title('Valuacion Danios - Predicted vs Sample number')
plt.show()

print(f'mae: {(df["Valuacion_Danios"] - df["predicted"]).abs().mean()}')