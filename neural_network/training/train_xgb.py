from xgboost import XGBRegressor
import joblib, os
from datetime import datetime
from shared import config
from .utils import preparar_dados

def treinar_modelo_xgb():
    X, y = preparar_dados()
    modelo = XGBRegressor(n_estimators=100, random_state=42)
    modelo.fit(X, y)

    caminho = os.path.join(config.DIRETORIO_MODELOS, f"xgb_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.pkl")
    joblib.dump(modelo, caminho)
    print(f"✅ Modelo XGBoost salvo em: {caminho}")
