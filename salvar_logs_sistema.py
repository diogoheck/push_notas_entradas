
def salvar_logs(conteudo, LOCAL_GRAVAR_LOGS):
    with open(LOCAL_GRAVAR_LOGS, 'a') as log:
        print(conteudo, file=log)