import pandas as pd
from sklearn.linear_model import HuberRegressor
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer

# Cargar los archivos CSV
test_df = pd.read_csv('data/test.csv')
clean_raw_data_df = pd.read_csv('data/clean_raw_data.csv')

# Convertir idParcela a numérico para facilitar la búsqueda de ids cercanos
clean_raw_data_df['id_num'] = clean_raw_data_df['idParcela'].str.extract('(\d+)', expand=False).astype(int)

# Función para imputar valores faltantes basado en los IDs cercanos
def imputar_valoracion(df, k=5):
    for i, row in df[df['Valuacion_Danios'].isnull()].iterrows():
        id_num = row['id_num']
        # Encontrar los k IDs más cercanos
        cercanos = df[~df['Valuacion_Danios'].isnull()].copy()
        cercanos['distancia'] = abs(cercanos['id_num'] - id_num)
        cercanos = cercanos.nsmallest(k, 'distancia')
        # Calcular la media de Valuacion_Danios de los ids cercanos
        valoracion_promedio = cercanos['Valuacion_Danios'].mean()
        # Imputar el valor
        df.at[i, 'Valuacion_Danios'] = valoracion_promedio
    return df

# Imputar los valores faltantes
clean_raw_data_df = imputar_valoracion(clean_raw_data_df)

# Seleccionar características y la variable objetivo
features = ['fxf', 'superficie', 'dnbr', 'sep_ndvi', 'nov_ndvi']
target = 'Valuacion_Danios'

# Eliminar filas con valores NaN en las características seleccionadas
model_data = clean_raw_data_df.dropna(subset=features + [target])

# Separar características y objetivo
X = model_data[features]
y = model_data[target]

# Dividir en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar el modelo HuberRegressor (robusto a outliers)
regressor = HuberRegressor()
regressor.fit(X_train, y_train)

# Imputar los valores faltantes en las características con la mediana
imputer = SimpleImputer(strategy='median')
X_full_imputed = imputer.fit_transform(clean_raw_data_df[features])

# Convertir el resultado de nuevo a un DataFrame para facilitar su uso
X_full_imputed_df = pd.DataFrame(X_full_imputed, columns=features)

# Predecir las valoraciones faltantes en el conjunto de datos completo con los valores imputados
predicted_values = regressor.predict(X_full_imputed_df)

# Añadir las predicciones al dataframe original
clean_raw_data_df['predicted_valuacion'] = predicted_values

# Ajustar las predicciones según la condición del dnbr
clean_raw_data_df.loc[clean_raw_data_df['dnbr'] < -0.05, 'predicted_valuacion'] = 0

# Reemplazar las valoraciones faltantes con las predicciones del modelo
clean_raw_data_df['Valuacion_Danios'] = clean_raw_data_df['Valuacion_Danios'].combine_first(clean_raw_data_df['predicted_valuacion'])

# Extraer la parte numérica de los IDs en ambos dataframes
test_df['id_num'] = test_df['idParcela'].str.extract('(\d+)', expand=False).astype(int)

# Realizar el merge basado en los IDs numéricos
merged_df = pd.merge(test_df, clean_raw_data_df, on='id_num', how='left')

# Usar la predicción existente y rellenar los valores faltantes con la media
mean_prediction = merged_df['predicted_valuacion'].mean()
merged_df['prediccion'] = merged_df['Valuacion_Danios'].combine_first(merged_df['predicted_valuacion'])
merged_df.loc[merged_df['dnbr'] < -0.05, 'prediccion'] = 0
merged_df['prediccion'].fillna(mean_prediction, inplace=True)

# Seleccionar solo las columnas necesarias para el archivo de salida
output_df = merged_df[['idParcela_x', 'prediccion']]
output_df.rename(columns={'idParcela_x': 'idParcela'}, inplace=True)

# Guardar el dataframe de salida en un archivo CSV
output_df.to_csv('predicciones_umbral_modificado.csv', index=False)

print("Predicciones guardadas en predicciones_umbral_modificado.csv")
