import pandas as pd
from data import clean_text, written_by_lawyer, predominant_feeling, formality_level, politeness_level, referred_company_name, psychological_impact_mentioned, economic_impact_mentioned
    


df = pd.read_csv('data/clean_data.csv')
df['id'] = df['id'].astype('Int64')
df['vut'] = df['vut'].astype('Int64')

clean_text(df)
written_by_lawyer(df)
predominant_feeling(df)
formality_level(df)
politeness_level(df)
referred_company_name(df)
psychological_impact_mentioned(df)
economic_impact_mentioned(df)
df = df[['id', 'tipo', 'estado', 'valuacion', 'pedania', 'written_by_lawyer', 'predominant_feeling', 'formality', 'politeness', 'referred_company_name', 'psychological_impact', 'economic_impact', 'ValorReclamo', 'Valuacion_Danios']]
# df = df[df['Valuacion_Danios'].notna()]
df.to_csv('data/processed_data.csv', index=False)