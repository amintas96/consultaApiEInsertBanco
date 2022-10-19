import Repository as cb
import logging

logging.basicConfig(format='%(levelname)s:%(asctime)s %(message)s',filename='GerenciadorIdsElegiveis.log', level=logging.INFO)

def montaArquivoDeComparacao():
    logging.info('Iniciando automacao : montaArquivoDeComparacao')
    arquivo = open('ArquivoBanco.txt','w')
    listaAcoesBanco = cb.consultaAcoes()
    for acao in listaAcoesBanco:
        listaDeUsuarios = cb.consultaUsuariosInTbBaixaUsuariosPorAcoes(acao)
        arquivo.write(f'{acao} =  {listaDeUsuarios}' + '\n')
    logging.info('montaArquivoDeComparacao: Concluído!')

def converteToDict(usuariosElegiveis, acoesUsuarios):
    logging.info(f'iniciando automacao: converteToDict')
    dictAeU = {}
    for linha in acoesUsuarios:
        listaUsuarios = []
        acao = linha[:4]
        for user in usuariosElegiveis:
            if user in linha:
                listaUsuarios.append(user)
        dictAeU[acao] = listaUsuarios
    return dictAeU

def comparaArquivos():
    logging.info(f'iniciando automacao: comparaArquivos')
    listaUsuariosElegiveis = cb.consultaUsuariosElegiveis()
    arquivoAtualizado = open('arquivoAtualizado.txt', 'r')
    aquivoBanco = open('ArquivoBanco.txt', 'r')

    arquivoAtualizado = converteToDict(listaUsuariosElegiveis, arquivoAtualizado)
    aquivoBanco = converteToDict(listaUsuariosElegiveis, aquivoBanco)

    for chave, valor in arquivoAtualizado.items():  
        usuariosAtualizados = valor
        listaArquivoBanco = aquivoBanco.get(chave)
        if len(usuariosAtualizados) != 0:                                                         
            for usuario in listaArquivoBanco:
                if usuario not in usuariosAtualizados:                                      
                    logging.info(f'deletando o {usuario} da {chave}.')                             
                    cb.deletaUsuarioNaAcao(usuario, chave)
            for usuario in usuariosAtualizados:
                if usuario not in listaArquivoBanco:
                    cb.insertTotbBaixaUsuariosPorAcoes(chave, usuario)
                    logging.info(f'Incluindo na Ação {chave} o usuário: {usuario}.')
        else:
            logging.info(f'Não possui usuário para cadastrar na acão {chave}')
            for usuario in listaArquivoBanco:
                if usuario:
                    logging.info(f'deletando o {usuario} da {chave}.')  
                    cb.deletaUsuarioNaAcao(usuario, chave)

    logging.info('comparaArquivos: finalizado')

def montaEComparaArquivo():
    logging.info('Iniciando automacao : montaArquivoDeComparacao')
    montaArquivoDeComparacao()
    comparaArquivos()
    logging.info('done')

