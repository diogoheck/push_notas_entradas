from pyautogui import sleep
from pynfe.processamento.comunicacao import ComunicacaoSefaz
from pynfe.utils.descompactar import DescompactaGzip
from pynfe.utils.flags import NAMESPACE_NFE
# from manifestacao import w_manifestacao
import os
from lxml import etree
import requests
import time
from openpyxl import load_workbook
from renomarxml import renome_arquivo
requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning)
from salvar_logs_sistema import salvar_logs

LOCAL_GRAVAR = 'R:\Compartilhado\Ti\Push_XML_log\log_PUSH.txt'


def df_manifesto(dic):

    uf = 'rs'
    homologacao = False
    NSU = 0
    CHAVE = ''

    con = ComunicacaoSefaz(uf, dic['CERTIFICADO'], dic['SENHA_CERTIFICADO'], homologacao)
    ultNSU = 0
    maxNSU = 0
    cStat = 0

    while True:
        
        xml = con.consulta_distribuicao(
            cnpj=dic['CNPJ'], chave=CHAVE, nsu=NSU)
        NSU = str(NSU).zfill(15)
        print(f'Nova consulta a partir do NSU: {NSU}')
        salvar_logs(f'Nova consulta a partir do NSU: {NSU}', LOCAL_GRAVAR)

        with open(rf'r:\\Compartilhado\\Push\\xmls_temp\\Resumo_xml\\consulta_distrib_gzip-{NSU}.xml', 'w+') as f:
            f.write(xml.text)

        #resposta = etree.fromstring(xml.content)
        # print(resposta)
        resposta = etree.parse(
            rf'r:\\Compartilhado\\Push\\xmls_temp\\Resumo_xml\\consulta_distrib_gzip-{NSU}.xml')

        ns = {'ns': NAMESPACE_NFE}

        contador_resposta = len(resposta.xpath(
            '//ns:retDistDFeInt/ns:loteDistDFeInt/ns:docZip', namespaces=ns))
        print(f'Quantidade de NSUs na consulta atual: {contador_resposta}')
        salvar_logs(
            f'Quantidade de NSUs na consulta atual: {contador_resposta}', LOCAL_GRAVAR)

        try:
            cStat = resposta.xpath(
                '//ns:retDistDFeInt/ns:cStat', namespaces=ns)[0].text
            print(f'cStat: {cStat}')
            salvar_logs(f'cStat: {cStat}', LOCAL_GRAVAR)

            xMotivo = resposta.xpath(
                '//ns:retDistDFeInt/ns:xMotivo', namespaces=ns)[0].text
            print(f'xMotivo: {xMotivo}')
            salvar_logs(f'xMotivo: {xMotivo}', LOCAL_GRAVAR)

            maxNSU = resposta.xpath(
                '//ns:retDistDFeInt/ns:maxNSU', namespaces=ns)[0].text
            print(f'maxNSU: {maxNSU}')
            salvar_logs(f'maxNSU: {maxNSU}', LOCAL_GRAVAR)
        except IndexError:
            pass
            # 137=nao tem mais arquivos e 138=existem mais arquivos para baixar
        if (cStat == '138'):
            for contador_xml in range(contador_resposta):
                tipo_schema = resposta.xpath(
                    '//ns:retDistDFeInt/ns:loteDistDFeInt/ns:docZip/@schema', namespaces=ns)[contador_xml]
                numero_nsu = resposta.xpath(
                    '//ns:retDistDFeInt/ns:loteDistDFeInt/ns:docZip/@NSU', namespaces=ns)[contador_xml]

                #nfe = 'procNFe_v4.00.xsd'
                #evento = 'procEventoNFe_v1.00.xsd'
                #resumo = 'resNFe_v1.01.xsd'
                if (tipo_schema == 'procNFe_v4.00.xsd'):
                    zip_resposta = resposta.xpath(
                        '//ns:retDistDFeInt/ns:loteDistDFeInt/ns:docZip', namespaces=ns)[contador_xml].text

                    descompactar_resposta = DescompactaGzip.descompacta(
                        zip_resposta)
                    texto_descompactado = etree.tostring(
                        descompactar_resposta).decode('utf-8')

                    with open(rf'r:\\Compartilhado\\Push\\xmls_temp\\XML-nsu-{NSU}-contador-{contador_xml}.xml', 'w+', encoding='UTF-8') as f:
                        f.write(texto_descompactado)

                # baixar o resumo e realizar a manifestacao do destinatario
                elif (tipo_schema == 'resNFe_v1.01.xsd'):
                    zip_resposta = resposta.xpath(
                        '//ns:retDistDFeInt/ns:loteDistDFeInt/ns:docZip', namespaces=ns)[contador_xml].text
                    resposta_descompactado = DescompactaGzip.descompacta(
                        zip_resposta)
                    xml_completo = etree.tostring(
                        resposta_descompactado).decode('utf-8')

                    # Ler o resumo | Cosulta a chave das NFe
                    chave_acesso_nfe = resposta_descompactado.xpath(
                        '//ns:resNFe/ns:chNFe', namespaces=ns)[0].text

                    # Gerar ciÃªncia da operaÃ§Ã£o
                    chave_ = chave_acesso_nfe
                    # w_manifestacao(chave_)

            NSU = resposta.xpath(
                '//ns:retDistDFeInt/ns:ultNSU', namespaces=ns)[0].text
            print(f'NSU: {NSU}')
            salvar_logs(f'NSU: {NSU}', LOCAL_GRAVAR)

        elif (cStat == '137'):
            print(f'Nao ha mais documentos a pesquisar')
            salvar_logs(f'Nao ha mais documentos a pesquisar', LOCAL_GRAVAR)
            break
        else:
            print(f'Falha')
            salvar_logs(f'Falha', LOCAL_GRAVAR)
            break