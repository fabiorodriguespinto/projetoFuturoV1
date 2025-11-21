##nn/training/train_linear.py

from sklearn.linear_model import LinearRegression
import joblib, os
from datetime import datetime
from shared import config
from .utils import preparar_dados

def treinar_modelo_linear():
    X, y = preparar_dados()
    modelo = LinearRegression()
    modelo.fit(X, y)

    caminho = os.path.join(config.DIRETORIO_MODELOS, f"linear_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.pkl")
    joblib.dump(modelo, caminho)
    print(f"✅ Modelo Linear salvo em: {caminho}")
