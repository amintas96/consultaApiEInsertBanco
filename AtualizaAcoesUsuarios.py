from calendar import MONDAY
import consultaApi
import utils
import logging
import schedule
import time

logging.basicConfig(format='%(levelname)s:%(asctime)s %(message)s',filename='GerenciadorIdsElegiveis.log', level=logging.INFO)

def atualiza_usuarios_por_acao():
    logging.info('Iniciando automacao: atualiza_usuarios_por_acao')
    consultaApi.verificaNaApiIDUsuarioPorAcao()
    utils.montaEComparaArquivo()



schedule.every().monday.at('09:00').do(atualiza_usuarios_por_acao)


while True:
    schedule.run_pending()
    time.sleep(300)
