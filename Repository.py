import pymssql
import logging

logging.basicConfig(format='%(levelname)s:%(asctime)s %(message)s',filename='GerenciadorIdsElegiveis.log', level=logging.INFO)

bancoAtual = 2

def conectaBanco(banco):    
    if banco == 1:
        try:
            server = '10.36.0.93'
            database = 'DB_AUTOMACAO'
            username = 'usr_automacao_bko'
            password = 'YqOleSorL7Eak5cHHJrW'
            conn = pymssql.connect(server, username, password, database)

            return conn
        except ConnectionError as e:
            logging.warning(f'error: {e}')

    elif banco == 2:
        try:
            server = '10.33.9.38'
            database = 'DB_AUTOMACAO'
            username = 'Usr_Desenv'
            password = 'Callink01'
            conn = pymssql.connect(server, username, password, database)
            return conn
        except ConnectionError as e:
            logging.warning(f'error: {e}')

    else:
        logging.warning(f'parametro errado')

def consultaAcoes():
    logging.info(f'Iniciando automação: consultaAcoes')
    conn = conectaBanco(1)
    cursor = conn.cursor()
    listaDeAcoes = []
    cursor.execute("""select acao from DB_AUTOMACAO..tbASD002AcoesElegiveis(nolock) order by acao""")
    for linha in cursor:
        listaDeAcoes.append(linha[0])
    conn.close()
    
    return listaDeAcoes

def consultaUsuariosElegiveis():
    logging.info(f'Iniciando automação: consultaUsuariosElegiveis')
    conn = conectaBanco(1)
    cursor = conn.cursor()
    listaUsuariosElegiveis = []
    cursor.execute(""" SELECT UE.USUARIO FROM DB_AUTOMACAO..TB_BRADESCO_USER BU (NOLOCK) 
                        INNER JOIN DB_AUTOMACAO..TBASD002USUARIOSELEGIVEIS (NOLOCK) UE ON BU.USER_DIGITOS = UE.USUARIO 
                        WHERE BU.TIPOSISTEMA IN(3, 13)""")
    for linha in cursor:
        listaUsuariosElegiveis.append(linha[0])
    conn.close()
    return listaUsuariosElegiveis

def consultaSeExisteAcao(acao):
    logging.info(f'Iniciando automação: consultaSeExisteAcao')
    conn = conectaBanco(bancoAtual)
    cursor = conn.cursor()
    cursor.execute(f""" select upa.acao_id from tbBaixaUsuariosPorAcoes upa (nolock)
    inner join tbASD002AcoesElegiveis ae (nolock) on ae.id = upa.acao_id
    where ae.acao = '{acao} ' """)

    linha = cursor.fetchone()
    if not linha:
        cursor.close()
        return False
    else:
        cursor.close()
        return True

def consultaSeExisteUsuario(acao, usuario):
    logging.info(f'Iniciando automação: consultaSeExisteUsuario')

    conn = conectaBanco(bancoAtual)
    cursor = conn.cursor()
    cursor.execute(f""" 
        select top 1 upa.usuario_id from tbBaixaUsuariosPorAcoes upa  (nolock)
        inner join tbASD002AcoesElegiveis ae    (nolock) on  ae.id = upa.acao_id
        inner join tbASD002UsuariosElegiveis ue (nolock) on ue.id = upa.usuario_id
        where ae.acao = '{acao}'  and ue.usuario = '{usuario}'
        """)
    linha = cursor.fetchone()
    if not linha:
        conn.close()
        return False
    else:
        conn.close()
        return True

def consultaIdUsuarioByUserDigito(usuario):
    logging.info(f'Iniciando automação: consultaIdUsuarioByUserDigito')
    conn = conectaBanco(bancoAtual)
    cursor = conn.cursor()

    cursor.execute(f"""
    select id from tbASD002UsuariosElegiveis (nolock) 
        where usuario = '{usuario}'    
    """)
    linha = cursor.fetchone()
    if not linha:
        conn.close()
        logging.info('Id não existe')
    else:
        conn.close()
        return linha[0]

def consultaIdAcaoByNomeAcao(acao):
    logging.info(f'Iniciando automação: consultaIdAcaoByNomeAcao')
    conn = conectaBanco(bancoAtual)
    cursor = conn.cursor()
    cursor.execute(f"""
        select id from DB_AUTOMACAO..tbASD002AcoesElegiveis(nolock) where acao = '{acao}' """)
    linha = cursor.fetchone()
    if not linha:
        conn.close()
        logging.info('Id não existe')
    else:
        conn.close()
        return linha[0]

def consultaOrg(code):
    logging.info(f'Iniciando automação: consultaOrg')
    conn = conectaBanco(1)
    cursor = conn.cursor()
    cursor.execute(f"""SELECT TOP (1) ORG FROM [DB_AUTOMACAO].[dbo].[tbASD002Importacao] (nolock) where code = '{code}'""")
    for linha in cursor:
        conn.close()
        return linha[0]

def insertTotbBaixaUsuariosPorAcoes(acao_id, usuario_id):
    logging.info(f'Iniciando automação: insertTotbBaixaUsuariosPorAcoes')
    acao_id = consultaIdAcaoByNomeAcao(acao_id)
    usuario_id = consultaIdUsuarioByUserDigito(usuario_id)
    conn = conectaBanco(bancoAtual)
    cursor = conn.cursor()
    cursor.execute(f"""INSERT INTO tbBaixaUsuariosPorAcoes(acao_id, usuario_id, data_vinculo) VALUES ('{acao_id}', '{usuario_id}', getdate())""")
    conn.commit()

def consultaAcaoInTbBaixaUsuariosPorAcoes():
    logging.info(f'Iniciando automação: consultaAcaoInTbBaixaUsuariosPorAcoes')
    conn = conectaBanco(bancoAtual)
    cursor = conn.cursor()
    cursor.execute("""select distinct ae.acao from tbBaixaUsuariosPorAcoes(nolock) upa
    inner join tbASD002AcoesElegiveis ae on upa.acao_id = ae.id""")
    listaDeAcoes = []
    for linha in cursor:
        listaDeAcoes.append(linha[0])
    conn.close()
    return listaDeAcoes

def consultaUsuariosInTbBaixaUsuariosPorAcoes(acao):
    logging.info(f'Iniciando automação: consultaUsuariosInTbBaixaUsuariosPorAcoes')
    conn = conectaBanco(bancoAtual)
    cursor = conn.cursor()
    cursor.execute(f"""select ue.usuario from tbBaixaUsuariosPorAcoes upa (nolock) 
    inner join tbASD002UsuariosElegiveis ue (nolock) on upa.usuario_id = ue.id
    inner join tbASD002AcoesElegiveis ae (nolock) on upa.acao_id = ae.id
    where ae.acao = '{acao}'""")
    listaUsuarios = []
    for linha in cursor:
        listaUsuarios.append(linha[0])
    conn.close()
    return listaUsuarios

def deletaUsuarioNaAcao(usuario, acao):
    logging.info(f'Iniciando automação: deletaUsuarioNaAcao')
    conn = conectaBanco(bancoAtual)
    cursor = conn.cursor()
    usuario = consultaIdUsuarioByUserDigito(usuario)
    acao = consultaIdAcaoByNomeAcao(acao)
    cursor.execute(f"""delete from tbBaixaUsuariosPorAcoes where acao_id = '{acao}' and usuario_id = '{usuario}' """)
    conn.commit()
    conn.close()


