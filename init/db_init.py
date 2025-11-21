# init/db_init.py

from shared.database import init_db
from shared.database import engine
import time

def inicializar_banco():
    print("Aguardando o PostgreSQL ficar pronto...")

    # aguarda o postgres estar acessível
    for i in range(10):
        try:
            with engine.connect() as conn:
                print("PostgreSQL conectado!")
                break
        except:
            print("Tentativa", i+1, "/ 10 - PostgreSQL ainda não está pronto...")
            time.sleep(3)

    print("Criando tabelas...")
    init_db()
    print("Tabelas criadas com sucesso!")


if __name__ == "__main__":
    inicializar_banco()



