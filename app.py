from leitura_credenciais_clientes import ler_credenciais_clientes
from requisicao_webservice import df_manifesto as requisicao_web
from renomarxml import renome_arquivo as renomear_xml
from openpyxl import load_workbook
import os
from time import sleep
LOCAL_GRAVAR = 'R:\Compartilhado\Ti\Push_XML_log\log_PUSH.txt'
LOCAL_GRAVAR_DUPL = 'R:\Compartilhado\Ti\Push_XML_log\log_duplicidade_notas.txt'
from salvar_logs_sistema import salvar_logs

if __name__ == '__main__':
    dic_credencais_clientes = ler_credenciais_clientes()
    if os.path.exists(LOCAL_GRAVAR):
        os.remove(LOCAL_GRAVAR)
    # if os.path.exists(LOCAL_GRAVAR_DUPL):
    #     os.remove(LOCAL_GRAVAR_DUPL)
    

    # Criar as pastas dos clientes para armazenar os xmls
    while 1:
        cwd = os.getcwd()
        arquivos = os.listdir('R:/Compartilhado/Push/xmls_temp/Resumo_xml')
        for arquivo in arquivos:
            os.chdir('R:/Compartilhado/Push/xmls_temp/Resumo_xml')
            os.remove(arquivo)
        os.chdir(cwd)
        caminho_padrao = f'R:/Compartilhado/Push/'
        
        for cnpj, credencias in dic_credencais_clientes.items():

            caminho_pasta = caminho_padrao  + credencias.get('NOME_PASTA')
            # print(caminho_pasta)
    
            # se a pasta nao existe, crie a pasta
            if not os.path.isdir(caminho_pasta):
                os.mkdir(caminho_pasta)

            # se nao ha nenhum xml na pasta, faça a requisicao
            # if not os.listdir(caminho_pasta):
            salvar_logs('*' * 50, LOCAL_GRAVAR)
            salvar_logs(credencias.get('NOME_PASTA'), LOCAL_GRAVAR)
            salvar_logs('*' * 50, LOCAL_GRAVAR)

            print('*' * 50)
            print(credencias.get('NOME_PASTA'))
            print('*' * 50)
            print(credencias)
            # fazer as requisições / downloads
            requisicao_web(credencias)
            renomear_xml(credencias.get('NOME_PASTA'))

            
        print('*' * 50)
        print('aguardando 1 hora')
        print('*' * 50)
        sleep(4000)
