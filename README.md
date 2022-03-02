# Planilhas
> Integração entre Notebooks e o Google Sheets, feita para humanos

O Pandas já está bem estabelecido como uma biblioteca para lidar com tabelas no Python - e os Notebook (seja o Jupyter, Jupyter Lab ou o Colab) também são muito usados para quando vamos usar o Pandas (principalmente em análises exploratórias). Mas um passo nesse trabalho ainda me parece ser mais complicado do que podia ser: as tarefas de ler e escrever dados de documentos (mais especificamente as planilhas do Google).

Hoje, se você for usar o snippet que o Google fornece para fazer essa conexão, vai encontrar um código assim:

```
from google.colab import auth
auth.authenticate_user() # Vai abrir uma janela onde você vai precisar se autenticar. E, por esse código, vai ter que fazer isso cada vez que reiniciar a sessão.

import gspread
from google.auth import default
creds, _ = default()

gc = gspread.authorize(creds)

sh = gc.create('A new spreadsheet') # Aqui ele vai criar uma nova planilha. Mas você vai ter que abrir o drive e pesquisar pelo nome para encontrar ela

# Open our new sheet and add some data.
worksheet = gc.open('A new spreadsheet').sheet1

cell_list = worksheet.range('A1:C2') 

import random
for cell in cell_list:
  cell.value = random.randint(1, 10) # Ele está povoando a planilha com dados de um iterador, não de um DataFrame

worksheet.update_cells(cell_list)
# Go to https://sheets.google.com to see your new spreadsheet.
```
Já com a biblioteca **Planilhas**, o processo de criar uma nova planilha do Google Sheets é, simplesmente:

```
planilha = Planilha(name = "A new spreadsheet")

>>>> =========================
>>>> A new spreadsheet
>>>> -------------------------
>>>> id: 1KWKAeEXkcroI_wUZ7R8R89ZsGKXHIgncxDdGrdwp3vo
>>>> https://docs.google.com/spreadsheets/d/1KWKAeEXkcroI_wUZ7R8R89ZsGKXHIgncxDdGrdwp3vo
>>>> =========================
>>>> 
>>>> As abas deste documento são:
>>>> - Página1
```

O que eu fiz com a biblioteca **Planilhas** foi envelopar várias dessas funções dentro da biblioteca para tornar ela o mais alto-nível possível, fazendo o processo de criar, abrir, escrever e acrescentar dados ser o mais parecido possível com a leitura de arquivos locais.

# Funcionalidades
- Criar arquivos e abas,
- Retornar informações sobre as planilhas (como url e nome das abas)
- Leitura e escrita de abas baseada em DataFrames,
- Atualização de abas, adcionando novas linhas (com a possiblidade de checar duplicadas),
- Criação de uma aba de log para documentação das alterações feitas no arquivo
- Função para pesquisar planilhas no Google Drive a partir do nome delas, retornando os ids.

# Instalação
Como o projeto ainda não tem um `setup.py`, o modo de instalar ainda é mais "artesanal" (o que, claro, ainda torna a biblioteca menos "própria para humanos").
```
!git clone https://github.com/rogeriomoreirajr/Planilhas

import sys
sys.path.insert(0,'/content/Planilhas/')

from planilha import Planilha, search
```

# Limitações
- O script ainda está muito ligado ao meu fluxo de trabalho - por exemplo, ele usa um arquivo de autenticação que guardo no meu Google Drive para se conectar ao Google.
- Ainda falta torná-lo mais amigável para a instalação (hoje ele pode ser feito através do código abaixo, mas um setup.py vai facilitar a vida)
- Documentação detalhando cada função da biblioteca.