import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from sklearn.linear_model import RANSACRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline



def linear(x, m, b):
    return m * x + b

def exponential(x, a, b, c):
    return a * np.exp(b * x) + c

def logarithmic(x, a, b):
    return a * np.log(x) + b

def calculate_tendency_line(x, y, func):
    popt, _ = curve_fit(func, x, y)
    return popt
    
def plot_valuacion_vs_valorreclamo(df):
    known_df = df[df['Validado'] == 'X']
    # group A in red, group B in blue
    plt.scatter(df['valuacion'], df['ValorReclamo'], c=df['group'], cmap='coolwarm')
    plt.scatter(known_df['valuacion'], known_df['ValorReclamo'], c='black', marker='x')
    plt.xlabel('Valuacion')
    plt.ylabel('ValorReclamo')
    plt.xscale('log')
    plt.yscale('log')

    x = np.linspace(min(df['valuacion']), max(df['valuacion']), 100)

    plt.show()

def plot_valuacion_vs_valuacion_danios(known_df):
    plt.scatter(known_df['valuacion'], known_df['Valuacion_Danios'], c=known_df['group'], cmap='coolwarm')
    plt.xlabel('Valuacion')
    plt.ylabel('Valuacion_Danios')
    # plt.xscale('log')
    # plt.yscale('log')

    x = np.linspace(min(known_df['valuacion']), max(known_df['valuacion']), 100)
    plt.plot(x, 0.7 * x, label='y = 0.8x')

    plt.show()

    

def main():
    df = pd.read_csv('data/clean_raw_data.csv')
    df['diff_ndvi'] = df['sep_ndvi'] - df['nov_ndvi']
    df['dnbr+0.1'] = df['dnbr'] + 0.1
    df['group'] = (df['ValorReclamo'] / df['valuacion']).apply(lambda x: 'A' if 1-1/3 < x < 1+1/3 else 'B')
    df['group'] = df['group'].astype('category').cat.codes
    train_df = df[df['Validado'] == 'X']
    # plot_valuacion_vs_valorreclamo(df)
    plot_valuacion_vs_valuacion_danios(train_df)
    # df['first_term'] = df.apply(lambda row: first_term(row, ), axis=1)

    

if __name__ == '__main__':
    main()