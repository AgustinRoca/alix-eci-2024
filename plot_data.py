import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_valor_reclamo_vs_valuacion(df):
    plt.figure(figsize=(10, 6))
    # sns.scatterplot(data=df, x='ValorReclamo', y='valuacion', hue='formality')
    plt.title('ValorReclamo vs Valuacion')
    plt.xlabel('ValorReclamo')
    plt.ylabel('Valuacion')
    # log scale
    plt.xscale('log')
    plt.yscale('log')

    # plot x=y line
    x = [5e4, 1e8]
    y = [5e4, 1e8]
    plt.plot(x, y, color='red')

    # plot with crosses the points (valorreclamo, valuacion) where ValuacionDanios is not null, color based on ValuacionDanios
    df_not_null = df[df['Valuacion_Danios'].notna()]
    sns.scatterplot(data=df_not_null, x='ValorReclamo', y='valuacion', hue='formality')
    sns.scatterplot(data=df_not_null, x='ValorReclamo', y='valuacion', hue='Valuacion_Danios', marker='x', s=100)
    plt.show()

if __name__ == '__main__':
    df = pd.read_csv('data/processed_data.csv')
    plot_valor_reclamo_vs_valuacion(df)