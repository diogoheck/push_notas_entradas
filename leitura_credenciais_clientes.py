import pandas as pd
import openpyxl
import os
from leitura_planilha_empresas import ler_planilha_empresas
from leitura_planilha_certificados import ler_planilha_certificados
from leitura_diretorio_certificados import ler_diretorio_certificados
from salvar_logs_sistema import salvar_logs
LOCAL_GRAVAR = 'R:\Compartilhado\Ti\Push_XML_log\log_certificados.txt'
LOCAL_CERTIFICADO = 'R:\Compartilhado\Certificados\Arquivos Certificados Digitais - ECNPJ A1'

def ler_credenciais_clientes():

    if os.path.exists(LOCAL_GRAVAR):
        os.remove(LOCAL_GRAVAR)

    lista_CNPJ_8_digitos_iniciais = ler_planilha_empresas(apenas_CNPJ=True)
    dic_planilha_certificado = ler_planilha_certificados()
    dic_certificados = ler_diretorio_certificados()

    dic_certificados_filtrado = {}
    for CNPJ in lista_CNPJ_8_digitos_iniciais:
        if dic_certificados.get(CNPJ):
            if dic_planilha_certificado.get(CNPJ):
                arquivo_certificado = dic_certificados.get(CNPJ)
                senha_certificado = dic_planilha_certificado.get(CNPJ)
                # dic_certificados_filtrado[CNPJ] = {'CERTIFICADO': str(arquivo_certificado)}
                dic_certificados_filtrado[CNPJ] = {'CERTIFICADO': LOCAL_CERTIFICADO + os.sep + arquivo_certificado}
                dic_certificados_filtrado[CNPJ].update({'SENHA_CERTIFICADO': str(senha_certificado)})
                # salvar_logs(f'{arquivo_certificado} | {senha_certificado}')
            else:
                salvar_logs(f'certificado nao encontrado na planilha de certificados => {CNPJ}', LOCAL_GRAVAR)
        else:
            salvar_logs(f'Certificado nao encontrado no diretorio de certificados => {CNPJ}', LOCAL_GRAVAR)


    plan_empresas = ler_planilha_empresas(apenas_CNPJ=False)
    dicionario_empresa = {}
    for plan in plan_empresas.values:
        cnpj = plan[1].replace('.', '').replace('/', '').replace('-', '')
        cnpj_8_digitos = cnpj[0:8]
        if dic_certificados_filtrado.get(cnpj_8_digitos): 
            dicionario_empresa[cnpj] = {'COD_UNICO': plan[0]}
            dicionario_empresa[cnpj].update({'CNPJ': cnpj})
            try:
                dicionario_empresa[cnpj].update({'NOME_PASTA': plan[2] + ' ' + plan[3]})
            except:
                dicionario_empresa[cnpj].update({'NOME_PASTA': plan[2]})

            dicionario_empresa[cnpj].update({'CERTIFICADO': dic_certificados_filtrado.get(cnpj_8_digitos)['CERTIFICADO']})
            dicionario_empresa[cnpj].update({'SENHA_CERTIFICADO': dic_certificados_filtrado.get(cnpj_8_digitos)['SENHA_CERTIFICADO']})
        
    
    
    return dicionario_empresa