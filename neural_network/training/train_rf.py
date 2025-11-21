##nn/training/train_rf.py

from sklearn.ensemble import RandomForestRegressor
import joblib, os
from datetime import datetime
from shared import config
from .utils import preparar_dados

def treinar_modelo_rf():
    X, y = preparar_dados()
    modelo = RandomForestRegressor(n_estimators=100, random_state=42)
    modelo.fit(X, y)

    caminho = os.path.join(config.DIRETORIO_MODELOS, f"rf_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.pkl")
    joblib.dump(modelo, caminho)
    print(f"✅ Modelo RF salvo em: {caminho}")
