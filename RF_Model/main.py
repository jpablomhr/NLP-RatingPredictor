import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(filepath):
    try:
        df = pd.read_csv(filepath) ## Cargamos el dataframe desde el filepath.
        return df
    except FileNotFoundError:
        print(f"Error: File not found in {filepath}")
        return None


def preprocess_data(df, text_column, target_column, max_features=500):
    """Preprocesa los datos convirtiendo el texto en vectores numéricos."""
    vectorizer = TfidfVectorizer(max_features=max_features)
    X = vectorizer.fit_transform(df[text_column])
    y = df[target_column]
    return X, y, vectorizer


def train_model(X_train, y_train):
    """Entrenamos el modelo de RandomForestRegressor."""
    model = RandomForestRegressor(random_state=42)
    model.fit(X_train, y_train)
    return model


def evaluate_model(model, X_test, y_test):
    """Evalúa el modelo y calcula el error absoluto medio (MAE)."""
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    return mae, y_pred

def feature_importance(model, vectorizer):
    """Graficamos la importancia de las características en un barplot."""
    feature_importances = model.feature_importances_
    feature_names = vectorizer.get_feature_names_out()
    importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': feature_importances})
    importance_df = importance_df.sort_values(by='Importance', ascending=False).head(20)

    plt.figure(figsize=(10, 8))
    sns.barplot(x='Importance', y='Feature', data=importance_df, palette='magma')
    plt.title('Top 20 Most Important Features')
    plt.xlabel('Relevance')
    plt.ylabel('Feature')
    plt.savefig('feature_importance.png')
    plt.show()

def rating_distribution(df):
    """Graficamos la distribución de las calificaciones (Rating)."""
    plt.figure(figsize=(8, 6))
    sns.countplot(x='Rating', data=df, palette='viridis')
    plt.title('Distribution of Ratings')
    plt.xlabel('Rating')
    plt.ylabel('Frequency')
    plt.savefig('distribution_of_ratings.png')
    plt.show()

def predictions_vs_actual(y_test, y_pred):
    """Scatterplot predicciones vs los valores reales."""
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=y_test, y=y_pred, alpha=0.5, color='purple')
    plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', linestyle='--')
    plt.title('Predictions vs Real')
    plt.xlabel('Real Value')
    plt.ylabel('Predictions')
    plt.savefig('real_vs_pred.png')
    plt.show()

def main():
    # Cargar el filepath
    filepath = 'review_with_feeling.csv'
    df_review = load_data(filepath)

    if df_review is not None:
        # Preprocesamiento de los datos
        X, y, vectorizer = preprocess_data(df_review, text_column='Cleanned Review', target_column='Rating')

        # Dividir los datos en conjuntos de entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Entrenamiento el modelo
        model = train_model(X_train, y_train)

        # Evaluación del modelo
        mae, y_pred = evaluate_model(model, X_test, y_test)
        print(f'Mean Absolute Error: {mae:.4f}')

        rating_distribution(df_review)
        feature_importance(model, vectorizer)
        predictions_vs_actual(y_test, y_pred)

if __name__ == "__main__":
    main()

