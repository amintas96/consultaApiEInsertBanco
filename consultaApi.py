import requests
import Repository

def verificaNaApiIDUsuarioPorAcao():
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
            print(f'{acao} =  {listaDeIdElegiveisNaAcao}')
            salva.write(f'{acao} =  {listaDeIdElegiveisNaAcao}' + '\n')
        except:
            print(f'falha com o código, {acao}')

    print('done')


