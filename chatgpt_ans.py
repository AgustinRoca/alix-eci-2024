import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from textblob import TextBlob
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error
import nltk
from nltk.corpus import stopwords

# Load the CSV file
file_path = 'data/Claims-WorkingFile_v2.csv'
claims_data = pd.read_csv(file_path)

# Define a set of common Spanish stopwords
nltk.download('stopwords')
manual_stopwords = stopwords.words('spanish')

# Sentiment analysis function using TextBlob
def sentiment_analysis(text):
    if pd.isna(text):
        return 0
    sentiment_score = TextBlob(text).sentiment.polarity
    return sentiment_score

# Apply sentiment analysis
claims_data['Sentiment'] = claims_data['TextoReclamo'].apply(sentiment_analysis)

# Update the TF-IDF vectorizer to remove stop words
vectorizer = TfidfVectorizer(max_features=100, stop_words=manual_stopwords)

# Process the text data
text_features = vectorizer.fit_transform(claims_data['TextoReclamo'].fillna('')).toarray()
text_features_df = pd.DataFrame(text_features, columns=vectorizer.get_feature_names_out())

# Combine text features with sentiment score
text_features_df['Sentiment'] = claims_data['Sentiment']

# Extract features from idParcela
claims_data[['ParcelID', 'Location']] = claims_data['idParcela'].str.split('-', expand=True)

# Parse 'direccion' to extract department and locality
claims_data[['Localidad', 'Pedania', 'Departamento']] = claims_data['direccion'].str.extract(r'(?P<Localidad>.+), .+ de (?P<Pedania>.+), Departamento (?P<Departamento>.+)')

# Convert categorical data to numerical form
claims_data['Location'] = claims_data['Location'].astype('category').cat.codes
claims_data['Localidad'] = claims_data['Localidad'].astype('category').cat.codes
claims_data['Pedania'] = claims_data['Pedania'].astype('category').cat.codes
claims_data['Departamento'] = claims_data['Departamento'].astype('category').cat.codes

# Correct the feature set
text_features_df.columns = [col.lower() for col in text_features_df.columns]  # Ensuring lowercase consistency
adjusted_selected_features = [
    'ValorReclamo', 'Location', 'Localidad', 'Pedania', 'Departamento'
] + list(text_features_df.columns)  # Including text features

# Recreate the final dataset with adjusted features
final_data = pd.concat([claims_data[['ValorReclamo', 'Location', 'Localidad', 'Pedania', 'Departamento']], text_features_df], axis=1)

# Separate known and unknown data again
known_data = claims_data.dropna(subset=['Valuacion_Danios'])
unknown_data = claims_data[claims_data['Valuacion_Danios'].isna()]

# Re-create the final dataset for known data
final_known_data = pd.concat([known_data[['ValorReclamo', 'Location', 'Localidad', 'Pedania', 'Departamento', 'Valuacion_Danios']], text_features_df], axis=1)
final_unknown_data = pd.concat([unknown_data[['ValorReclamo', 'Location', 'Localidad', 'Pedania', 'Departamento']], text_features_df], axis=1)

# Features and target variable for the known data
X_known = final_known_data.drop(columns=['Valuacion_Danios'])
y_known = final_known_data['Valuacion_Danios']

# Features for the unknown data
X_unknown = final_unknown_data

# Split the known data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_known, y_known, test_size=0.2, random_state=42)

# Impute missing values with the median for numerical features
imputer = SimpleImputer(strategy='median')

# Fit and transform the training data
X_train_imputed = imputer.fit_transform(X_train)
X_test_imputed = imputer.transform(X_test)

# Handle NaN values in the target variable
y_train = y_train.fillna(y_train.median())
y_test = y_test.fillna(y_test.median())

# Initialize and train the model
gb_model = GradientBoostingRegressor(random_state=42)
gb_model.fit(X_train_imputed, y_train)

# Predict on the test set
gb_pred = gb_model.predict(X_test_imputed)

# Evaluate the model with MAE
gb_mae = mean_absolute_error(y_test, gb_pred)
print(f'Mean Absolute Error: {gb_mae}')
