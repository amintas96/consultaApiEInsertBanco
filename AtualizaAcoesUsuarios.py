import consultaApi
import utils
import logging

logging.basicConfig(format='%(levelname)s:%(asctime)s %(message)s',filename='GerenciadorIdsElegiveis.log', level=logging.INFO)

def atualiza_usuarios_por_acao():
    logging.info('Iniciando automacao: atualiza_usuarios_por_acao')
    consultaApi.verificaNaApiIDUsuarioPorAcao()
    utils.montaEComparaArquivo()

