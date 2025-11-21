##nn/training/train.py

from .train_linear import treinar_modelo_linear
from .train_rf import treinar_modelo_rf
from .train_xgb import treinar_modelo_xgb

def treinar_todos_modelos():
    treinar_modelo_linear()
    treinar_modelo_rf()
    treinar_modelo_xgb()


