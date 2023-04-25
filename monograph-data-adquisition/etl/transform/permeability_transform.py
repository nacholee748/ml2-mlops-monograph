import pandas as pd
import numpy as np
import re

from logger import setup_logger

class PermeabilityTransoform:
    logger = setup_logger()
    
    def __init__(self,df_raw: pd.DataFrame) -> None:
        self.df_raw=df_raw
        self.df_processed = None

    def clean_permability(self) -> pd.DataFrame:
        df = self.df_raw
        df.drop(['CONSECUTIVO','Unnamed: 17','Unnamed: 18','Unnamed: 19'],axis = 1, inplace=True)
        
        # Renombramos las columnas con nombres legibles
        df.columns = ['Ano', 'Mes', 'Dia', 'Referencia', 'Estructura', 'Calibre1',
            'Calibre2', 'Calibre3', 'Calibre4', 'Calibre5', 'Calibre_Prom',
            'Muestra', 'Grados_C', 'Porc_Humedad', 'Permeabilidad',
            'Instrumentista']

        bad_text = set()
        for i in range(1,6):
            # print(df[f'Calibre{i}'][~df[f'Calibre{i}'].astype(str).str.isnumeric()].value_counts())
            bad_text.update(df[f'Calibre{i}'][~df[f'Calibre{i}'].astype(str).str.isnumeric()].value_counts().index)
            # print(bad_text)  

        for i in range(1,6):
            df[f'Calibre{i}'].replace(bad_text,np.nan,inplace=True)
            df[f'Calibre{i}'].astype(float)

        
        regex_float = '[-+]?\d*\.\d+|\d+"'

        for i in ['Permeabilidad','Calibre_Prom']:
            error = df[i][(~df[i].apply(lambda x: True if (re.fullmatch(regex_float, str(x))) else False)) & (~df[i].astype(str).str.isnumeric())].unique()
            df[i].replace(error,np.nan,inplace= True)
            df[i] = df[i].astype(float)

        df = df.drop(columns=['Ano','Mes','Dia','Calibre2','Calibre3','Calibre4','Calibre5','Calibre_Prom','Instrumentista','Referencia'])

        df['Estructura'] = df['Estructura'].astype(str).apply(lambda x: x.strip())

        regex_estructura_1 = "PET+[\s,/,-]+AL+[\s,/,-]+PE"
        Estructura_clean_PET_AL_PE = df['Estructura'][df['Estructura'].apply(lambda x: True if (re.search(regex_estructura_1, str(x))) else False)]
        # print(Estructura_clean_PET_AL_PE.unique())
        Estructura_clean_PET_AL_PE.count()
        df['Estructura'] = df['Estructura'].replace(Estructura_clean_PET_AL_PE.unique(),'PET-AL-PE')

        # Optimización de categoria BOPP-BOPP-MET
        regex_estructura_1 = "BOPP+[\s,/,-]+BOPP+[\s,/,-]+MET"
        Estructura_clean_PET_AL_PE = df['Estructura'][df['Estructura'].apply(lambda x: True if (re.search(regex_estructura_1, str(x))) else False)]
        # print(Estructura_clean_PET_AL_PE.unique())
        Estructura_clean_PET_AL_PE.count()
        df['Estructura'] = df['Estructura'].replace(Estructura_clean_PET_AL_PE.unique(),'BOPP-BOPP MET')

        df['Estructura'] = df['Estructura'].replace(regex=['\s+','/'],value='-')


        # Identificamos algunas categorias que son las mismas solo tenian diferencias en la escritorua
        df['Estructura'] = df['Estructura'].replace('BOPP-BOPPMET','BOPP-BOPP-MET')
        df['Estructura'] = df['Estructura'].replace('BOPP-MATE---BOPP-MET','BOPP-MATE-BOPP-MET')
        df['Estructura'] = df['Estructura'].replace('NO-REPORTADO','NO-REPORTADA')

        # Eliminamos las filas de las estructuras nan, ya que no podemos hacer imputación 
        df.drop(df.loc[df['Estructura']=='nan'].index,inplace=True)

        df.loc[df['Permeabilidad']<0] = np.nan

        # Conversión variable categorica a codigos
        df = pd.get_dummies(df, prefix='Estructura',drop_first=True)

        self.df_processed = df

        return self.df_processed 