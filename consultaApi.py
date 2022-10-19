import requests
import Repository
import logging

logging.basicConfig(format='%(levelname)s:%(asctime)s %(message)s',filename='GerenciadorIdsElegiveis.log', level=logging.INFO)


def verificaNaApiIDUsuarioPorAcao():
    logging.info(f'Iniciando automação: verificaNaApiIDUsuarioPorAcao')
    idElegiveisCallink = Repository.consultaUsuariosElegiveis()
    acoesElegiveis = Repository.consultaAcoes() 
    dictIdsElegiveisPorAcoes = {}
    dictIdsPorAcoes = {}        
    salva = open('arquivoAtualizado.txt', 'w')
    salva2 = open('TodosOsIdsPorAcao.txt', 'w')
    for acao in acoesElegiveis:
        try:
            code = Repository.consultaOrg(acao)
            listaDeIdElegiveisNaAcao = []
            listaDeTodosOsIds = []
            r = requests.get(f'http://10.36.0.63:8099/pcomm/pcomm-consulta-asqa/{acao}&{code}')
            consultaDict = r.json()['result']['asqa']['detalhes']['eligibles']
            for id in consultaDict:
                listaDeTodosOsIds.append(id)
                if id in idElegiveisCallink:
                    listaDeIdElegiveisNaAcao.append(id)

            dictIdsElegiveisPorAcoes[acao] = listaDeIdElegiveisNaAcao
            dictIdsPorAcoes[acao] = listaDeTodosOsIds
            salva2.write(f'{acao} = {listaDeTodosOsIds}' + '\n')
            logging.info(f'{acao} =  {listaDeIdElegiveisNaAcao}')
            salva.write(f'{acao} =  {listaDeIdElegiveisNaAcao}' + '\n')
        except:
            logging.warning(f'falha com o código, {acao}')

    logging.info('verificaNaApiIDUsuarioPorAcao finalizado')


