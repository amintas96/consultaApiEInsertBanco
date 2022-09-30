import Repository as cb

def montaArquivoDeComparacao():
    print('Iniciando automação : montaArquivoDeComparacao')
    arquivo = open('ArquivoBanco.txt','w')
    listaAcoesBanco = cb.consultaAcoes()
    for acao in listaAcoesBanco:
        listaDeUsuarios = cb.consultaUsuariosInTbBaixaUsuariosPorAcoes(acao)
        arquivo.write(f'{acao} =  {listaDeUsuarios}' + '\n')

    return print('montaArquivoDeComparacao: Concluído!')

def converteToDict(usuariosElegiveis, acoesUsuarios):
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
    print('iniciando automacao: comparaArquivos')
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
                    print(f'deletando o {usuario} da {chave}.')                             
                    cb.deletaUsuarioNaAcao(usuario, chave)
            for usuario in usuariosAtualizados:
                if usuario not in listaArquivoBanco:
                    cb.insertTotbBaixaUsuariosPorAcoes(chave, usuario)
                    print(f'Incluindo na Ação {chave} o usuário: {usuario}.')
        else:
            print(f'Não possui usuário para cadastrar na acão {chave}')

    print('comparaArquivos: finalizado')

def montaEComparaArquivo():
    montaArquivoDeComparacao()
    comparaArquivos()
    print('done')