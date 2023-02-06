import os

i = 1
for pasta in os.listdir('R:\Compartilhado\Push'):
    for arquivos in os.listdir('R:\Compartilhado\Push' + os.sep + pasta):
        if os.path.isfile('R:\Compartilhado\Push' + os.sep + pasta + os.sep + arquivos):
            os.remove('R:\Compartilhado\Push' + os.sep + pasta + os.sep + arquivos)
            i += 1
            # print(arquivos)
print(i) 