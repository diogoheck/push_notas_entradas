import pandas as pd
import openpyxl
import os
from leitura_planilha_empresas import ler_planilha_empresas
from leitura_planilha_certificados import ler_planilha_certificados
from leitura_diretorio_certificados import ler_diretorio_certificados

if __name__ == '__main__':
    lista_CNPJ_8_digitos_iniciais = ler_planilha_empresas(apenas_CNPJ=True)
    dic_planilha_certificado = ler_planilha_certificados()
    dic_certificados = ler_diretorio_certificados()

    for CNPJ in lista_CNPJ_8_digitos_iniciais:
        if dic_certificados.get(CNPJ):
            if dic_planilha_certificado.get(CNPJ):
                # print(dic_certificados.get(CNPJ), dic_planilha_certificado.get(CNPJ))
                pass
            else:
                print(f'certificado nao encontrado na planilha de certificados => {CNPJ}')
        else:
            print(f'Certificado nao encontrado no diretorio de certificados => {CNPJ}')


    plan_empresas = ler_planilha_empresas(apenas_CNPJ=False)
    for plan in plan_empresas.values:
        print(plan)