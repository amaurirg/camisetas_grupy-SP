# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
import os
from decimal import *


def index():
    return dict()


def semantic_page():
    return dict()


def preenche_tabela_camisetas():
    """ Lê o arquivo .csv e preenche o registro conforme esses dados """
    file = open("applications/camisetas_grupy/static/CamisetasGrupy-SP.csv")
    fileReader = csv.reader(file)
    dados = list(fileReader)
    
    for row in dados:
        horario = row[0]
        nome = row[1]
        tipo = row[2]
        tam_val = row[3].split(' - ')
        tamanho = tam_val[0]
        # valor = tam_val[1]
        valor = tam_val[1][3:].replace(',','.')

        CG.insert(
            horario = horario,
            nome = nome,
            tipo = tipo,
            tamanho = tamanho,
            valor = valor
        )

    # return dict()
    redirect(URL('pedidos'))


def atualiza_tabela_camisetas():
    """ Muda todos os registros do campo 'pago' para 'NÃO' """
    todos = db(CG.id>0).update(pago='NÃO')
    redirect(URL('pedidos'))


def pedidos():
    """ Seleciona todos os registros, separa os pagos e nao_pagos, soma valores pagos """
    # Paginação
    if not request.vars.page:
        redirect(URL(vars={'page':1}))
    else:
        page = int(request.vars.page)
    start = (page-1)*7
    end = page*7
    geral = db(CG).select(orderby=db.camisetas.nome, limitby=(start,end))
    # A função 'Decimal' com o quantize retornam o número correto de casas decimais e 'sum' soma os valores
    soma_valores = sum([Decimal(soma.valor).quantize(Decimal('1.00')) for soma in db(CG.pago).select(CG.valor)])
    a_receber = sum([Decimal(soma.valor).quantize(Decimal('1.00')) for soma in db(CG.pago=='NÃO').select(CG.valor)])
    # dados = db(CG).select(CG.tipo,CG.tamanho, CG.valor, groupby=CG.tamanho)
    pagos = db(CG.pago=='SIM').select()
    nao_pagos = db(CG.pago=='NÃO').select()
    count = db.camisetas.id.count()
    qtde_tam = [[row.camisetas.tipo, row.camisetas.tamanho, row[count]] for row in 
                db(db.camisetas.id).select(db.camisetas.tipo, db.camisetas.tamanho, 
                count, groupby=(db.camisetas.tipo, db.camisetas.tamanho), orderby=db.camisetas.tipo)]
    # print qtde_tam
    return dict(geral=geral, pagos=pagos, nao_pagos=nao_pagos, 
                qtde_tam=qtde_tam, soma_valores=soma_valores, a_receber=a_receber)


def editar():
    pessoa = db(CG.id == request.args(0)).select().first()
    pagamento = pessoa.pago
    form = SQLFORM(CG, pessoa, _class="ui form")
    if form.process().accepted:
        cabecalho = DIV( 
                        DIV('Atualizar Dados', _class='header'), 
                        P('Alterado com sucesso!'), 
                        _class="ui success message")
    elif form.errors:
        cabecalho = DIV(
                        DIV('Atualizar Dados', _class='header'),
                        P('Erros no preenchimento ou campo vazio!'),
                        _class="ui negative message")
    else:
        cabecalho = DIV(
                        DIV('Atualizar Dados', _class='header'), 
                        P('Preencha os campos para alterar!'),
                        _class='ui floating medium message')
    return dict(form=form, pagamento=pagamento, cabecalho=cabecalho)


def tab():
    return dict()

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


