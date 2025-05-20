# nn/training/treinar_modelo.py
import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle

df = pd.read_csv('dados/btc.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['dia'] = df['timestamp'].dt.dayofyear
X = df[['dia']]
y = df['price']

modelo = LinearRegression()
modelo.fit(X, y)

with open('nn/modelos/modelo_btc.pkl', 'wb') as f:
    pickle.dump(modelo, f)

print("Modelo treinado e salvo em nn/modelos/modelo_btc.pkl")

# Enviar notificação ao finalizar
from shared.notifications import notificar_telegram
notificar_telegram("Re-treinamento finalizado com sucesso!")