import pandas as pd
import openpyxl
import os


# Ler diretório de Certificados conforme lista CNPJ (pegar os 8 digitos e comparar)
def ler_diretorio_certificados():
    pasta_certificados = 'R:\Compartilhado\Certificados\Arquivos Certificados Digitais - ECNPJ A1'
    dic_certificados = {}
    for certificado in os.listdir(pasta_certificados):
        CNPJ = certificado.split('-')[-1].split('.')[0][0:8]
        dic_certificados[CNPJ] = certificado
    return dic_certificados