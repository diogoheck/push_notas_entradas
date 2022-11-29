import pandas as pd
import openpyxl
import os


# ler planilha certificados e pegar as senhas.
def ler_planilha_certificados():
    df2 = pd.read_excel('R:\Compartilhado\Certificados\Controle administrativo\Senhas Certificados Digitais.xlsx', sheet_name='eCNPJ')
    plan = df2[['CNPJ', 'SENHA']]
    dic_planilha_certificado = {}
    for p in plan.values:
        CNPJ = str(p[0]).split('.')[0]
        if len(CNPJ) < 14:
            CNPJ = CNPJ.zfill(14)
        CNPJ = CNPJ[0:8]
        dic_planilha_certificado[CNPJ] = p[1]
    return dic_planilha_certificado