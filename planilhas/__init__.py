import gspread
import pandas as pd
import re

from datetime import datetime as dt
from datetime import timedelta as td
from gspread_dataframe import get_as_dataframe, set_with_dataframe
from oauth2client.client import GoogleCredentials

class Planilha():
    def __init__(self, key=None, name=None, oauth = True):
        if key == None:
            gc = connect(oauth=oauth)
            gc.create(name)
            self.key = gc.open(name).id
        else:
            self.key = key

        self.sh = self.open(sheets=True)
        sh = self.open(sheets=True)
        self.abas = [el.title for el in sh.worksheets()]
    
    def __repr__(self):
        sh = self.open(sheets=True)
        abas = [el.title for el in sh.worksheets()]
        nome = sh.title

        base = 'https://docs.google.com/spreadsheets/d/'+self.key

        mensagem = "="*25+f"\n{nome}\n"+"-"*25+f"\nid: {self.key}\n"+f"{base}\n"+"="*25+"\n\nAs abas deste documento são:\n- "+ '\n- '.join(abas)

        return mensagem

    def open(self, tab=None, write=False, sheets=False):
        "Fazer ele abrir a primeira aba se não tiver tab"
        gc = connect()
        sh = gc.open_by_key(self.key)

        if sheets:
            return sh

        if tab:
            if not tab in [el.title for el in sh.worksheets()]:
                if write:
                    print(f'Criando aba "{tab}"')
                    sh.add_worksheet(tab, 1000, 26)
                else:
                    abas = [el.title for el in sh.worksheets()]
                    raise ValueError(f'Não existe uma aba "{tab}" no documento.\nAs abas atuais são:\n- '+ "\n- ".join(abas))
            wk = sh.worksheet(tab)
        else:
            wk = sh.get_worksheet(0)
        return wk

    def read(self, tab=None, raw=False, **kwargs):
        wk = self.open(tab)
        if not raw:
            df = get_as_dataframe(wk, evaluate_formulas=True, **kwargs)
            df = df.dropna(how='all', axis=1).dropna(how='all', axis=0)
        if raw:
            values = wk.get_all_values()
            df = '\n'.join('\t'.join(el) for el in values)
        return df

    def clear(self, tab):
        self.open(tab).clear()

    def write(self, tab, df, log=None, append=False, resize=False, include_index=False, start = None, force_append = False, **kwargs):
        if not tab in self.abas: 
            operacao = "Criação"
            append = False
        wk = self.open(tab, write=True)
        _df = self.read(tab)

        if append:
            operacao = 'Apêndice'
            if not start:
                start = _df.shape[0]
            # Header são iguais?

            def check_force(force_append=force_append):
                if not force_append:
                    if list(df.columns) == list(_df.columns):
                        return True
                    else:
                        raise ValueError(f'As colunas não concidem.\n\nColunas originais:\n{", ".join(_df.columns)}\n\nColunas novas:\n{", ".join(df.columns)}')
                else:
                    return True

            if check_force(force_append):
                set_with_dataframe(wk, df, row = start + 2, col=1, include_column_header=False, 
                                   resize=resize, include_index = include_index)
                
        if not append:
            operacao = "Mudança total"
            set_with_dataframe(wk, df, resize=resize, include_index = include_index, **kwargs)

        if log:
            self.logger(log, tab, operacao)

    def logger(self, log, tab, operacao):
        dados = {
            'Horario': (dt.now() - td(hours=3)).strftime('%H:%M, %d/%m/%Y'),
            'Aba': tab, 
            'Operação': operacao,
            'Alteração': log,
        }
        self.write('log',pd.DataFrame([dados]), include_index=False, append=True)

def search(query, oauth=True):
    gc = connect(oauth=oauth)

    query = query.lower()
    
    results = [{'nome': el.title, 'id':el.id} for el in gc.openall() if re.search(query, el.title.lower())]
    if len(results) > 0:
        intro = 'Planilhas encontradas' if len(results) > 1 else 'Planilha encontrada'
        print(intro+':\n')
        for result in results: 
            print(f'Nome:\t{result["nome"]}\nId:\t{result["id"]}')

def connect(oauth=True):
    if not oauth: 
        adc_path = 'C:/Users/rogerio.junior/OneDrive/jupyter/.apoio/planilhas-344512-622259d0ca23.json'
        with open(adc_path) as file:
            gc = gspread.authorize(GoogleCredentials.from_json(file.read()))

    else: gc = gspread.oauth()
    return gc
