import pandas as pd
import openpyxl
import os
from leitura_planilha_empresas import ler_planilha_empresas
from leitura_planilha_certificados import ler_planilha_certificados
from leitura_diretorio_certificados import ler_diretorio_certificados

LOCAL_GRAVAR_LOGS = 'R:\Compartilhado\Ti\Push_XML_log\log.txt'


def salvar_logs(conteudo):
    with open(LOCAL_GRAVAR_LOGS, 'a') as log:
        print(conteudo, file=log)

if __name__ == '__main__':

    if os.path.exists(LOCAL_GRAVAR_LOGS):
        os.remove(LOCAL_GRAVAR_LOGS)

    lista_CNPJ_8_digitos_iniciais = ler_planilha_empresas(apenas_CNPJ=True)
    dic_planilha_certificado = ler_planilha_certificados()
    dic_certificados = ler_diretorio_certificados()

    
    for CNPJ in lista_CNPJ_8_digitos_iniciais:
        if dic_certificados.get(CNPJ):
            if dic_planilha_certificado.get(CNPJ):
                arquivo_certificado = dic_certificados.get(CNPJ)
                senha_certificado = dic_planilha_certificado.get(CNPJ)
                salvar_logs(f'{arquivo_certificado} | {senha_certificado}')
            else:
                salvar_logs(f'certificado nao encontrado na planilha de certificados => {CNPJ}')
        else:
            salvar_logs(f'Certificado nao encontrado no diretorio de certificados => {CNPJ}')


    plan_empresas = ler_planilha_empresas(apenas_CNPJ=False)
    for plan in plan_empresas.values:
        print(plan)
        # pass