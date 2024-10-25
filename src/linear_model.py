import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

data = pd.read_csv("C:\\Users\\jorge\\OneDrive\\Documents\\software\\housing.csv")
X = data.iloc[:,0:4]  
y = data.iloc[:,6]   

# Dividimos los datos en conjunto de entrenamiento y prueba (80% entrenamiento, 20% prueba)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Creamos el modelo lineal
model = LinearRegression()

# Entrenamos el modelo con los datos de entrenamiento
model.fit(X_train, y_train)

# Predecimos los valores para el conjunto de entrenamiento
y_train_pred = model.predict(X_train)

# Calculamos el error cuadrático medio (MSE) y el coeficiente de determinación (R²)
mse_train = mean_squared_error(y_train, y_train_pred)
r2_train = r2_score(y_train, y_train_pred)

print(f'Error cuadrático medio (MSE) en entrenamiento: {mse_train}')
print(f'Coeficiente de determinación (R²) en entrenamiento: {r2_train}')

