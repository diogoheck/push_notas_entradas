import os
import xml.etree.ElementTree as Et
from datetime import date
import time
from salvar_logs_sistema import salvar_logs
LOCAL_GRAVAR = 'R:\Compartilhado\Ti\Push_XML_log\log_duplicidade_notas.txt'

class Read_xml():
    def __init__(self, directory) -> None:
        self.directory = directory

    def all_files(self):

        return [os.path.join(self.directory, arq) for arq in os.listdir(self.directory)
                if arq.lower().endswith(".xml")]

    def check_none(sef, var):
        if var == None:
            return ""
        else:
            try:
                return var.text.replace('.', ',')
            except:
                return var.text

    def format_cnpj(self, cnpj):
        try:
            cnpj = f'{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}.{cnpj[8:12]}-{cnpj[12:14]}'
            return cnpj

        except:
            return ""

    def nfe_data(self, xml):
        root = Et.parse(xml).getroot()
        nsNfe = {"ns": "http://www.portalfiscal.inf.br/nfe"}

        # DADOS DA NFE
        nfe = self.check_none(
            root.find("./ns:NFe/ns:infNFe/ns:ide/ns:nNF", nsNfe))
        naturezaOp = self.check_none(
            root.find("./ns:NFe/ns:infNFe/ns:ide/ns:natOp", nsNfe))
        naturezaOp = ''.join(char for char in naturezaOp if char.isalnum())
        serie = self.check_none(
            root.find("./ns:NFe/ns:infNFe/ns:ide/ns:serie", nsNfe))
        data_emissao = self.check_none(
            root.find("./ns:NFe/ns:infNFe/ns:ide/ns:dhEmi", nsNfe))
        data_emissao = F"{data_emissao[8:10]}-{data_emissao[5:7]}-{data_emissao[:4]}"

        # DADOS EMITENTES
        chave = self.check_none(
            root.find("./ns:protNFe/ns:infProt/ns:chNFe", nsNfe))
        cnpj_emitente = self.check_none(
            root.find("./ns:NFe/ns:infNFe/ns:emit/ns:CNPJ", nsNfe))
        nome_emitente = self.check_none(
            root.find("./ns:NFe/ns:infNFe/ns:emit/ns:xFant", nsNfe))

        cnpj_emitente = self.format_cnpj(cnpj_emitente)
        valorNfe = self.check_none(
            root.find("./ns:NFe/ns:infNFe/ns:total/ns:ICMSTot/ns:vNF", nsNfe))
        data_importacao = date.today()
        data_importacao = data_importacao.strftime('%d/%m/%Y')
        data_saida = ''
        usuario = ''

        itemNota = 1
        notas = []

        for item in root.findall("./ns:NFe/ns:infNFe/ns:det", nsNfe):

            # DADOS DO ITEM
            cod = self.check_none(item.find(".ns:prod/ns:cProd", nsNfe))
            qntd = self.check_none(item.find(".ns:prod/ns:qCom", nsNfe))
            descricao = self.check_none(item.find(".ns:prod/ns:xProd", nsNfe))
            unidade_medida = self.check_none(
                item.find(".ns:prod/ns:uCom", nsNfe))
            valorProd = self.check_none(item.find(".ns:prod/ns:vProd", nsNfe))
            combustivel = self.check_none(
                item.find(".ns:prod/ns:comb/ns:descANP", nsNfe))

            dados = [nfe, serie, data_emissao, chave, cnpj_emitente, nome_emitente,
                     valorNfe, itemNota, cod, qntd, descricao, unidade_medida, valorProd,
                     data_importacao, usuario, data_saida, naturezaOp, combustivel]

            notas.append(dados)
            itemNota += 1
        return notas


def renome_arquivo(nome_pasta):
    xml = Read_xml(rf'r:\Compartilhado\Push\xmls_temp')
    all = xml.all_files()
    # print(all)
    w = 1

    for i in all:

        result = xml.nfe_data(i)
        comb = result[0][17]

        if comb == "":
            # destino de notas que não são combustivel com base na tag "descANP"
            nome_aqr = rf'r:\Compartilhado\Push\{nome_pasta}\{result[0][3]}.xml'
        else:
            nome_aqr = rf'r:\Compartilhado\Push\{nome_pasta}\{result[0][3]}.xml'
            # destino das notas que são combustivel com base na tag "descANP"
            # print("SEPARANDO XML DE COMBUSTIVEL")
            # nome_aqr = rf'U:\\TOTVS\\Protheus12\\Protheus_data\\xmlnfe\\nfe_in\\{result[0][3]}.xml'

        try:
            os.rename(i, nome_aqr)
            print(
                f'Caminho de origem renomeado para caminho de destino com sucesso. {result[0][0]}')
        except IsADirectoryError:
            print(
                f'A origem é um arquivo, mas o destino é um diretório. {result[0][0]}')
        except NotADirectoryError:
            print(
                f'A origem é um diretório, mas o destino é um arquivo. {result[0][0]}')
        except PermissionError:
            print(f'Operação não permitida. {result[0][0]}')
        except FileExistsError:
            os.remove(i)
            salvar_logs(f'############## DELETADO POR DUPLICIDADE ############## {nome_aqr}', LOCAL_GRAVAR)
        except OSError as error:
            print(error)
