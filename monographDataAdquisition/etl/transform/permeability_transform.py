import pandas as pd
import numpy as np
import re
from sklearn.impute import KNNImputer 
from sklearn.decomposition import PCA

from logger import setup_logger

class PermeabilityTransoform:
    logger = setup_logger()
    
    def __init__(self,df_raw: pd.DataFrame) -> None:
        self.df_raw=df_raw
        self.df_processed = None
        self.pca_components = 2

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

        df = df.drop(columns=['Ano','Mes','Dia','Instrumentista','Referencia'])

        df['Estructura'] = df['Estructura'].astype(str).apply(lambda x: x.strip())

        regex_estructura_1 = "PET+[\s,/,-]+AL+[\s,/,-]+PE"
        Estructura_clean_PET_AL_PE = df['Estructura'][df['Estructura'].apply(lambda x: True if (re.search(regex_estructura_1, str(x))) else False)]
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

        # Conversión variable categorica a codigos
        df = pd.get_dummies(df, prefix='Estructura',drop_first=True)
        
        df['Permeabilidad'] = df['Permeabilidad'].where(df['Permeabilidad'] >= 0, np.nan)
        
        ## Data inputation
        df = self.data_inputation(df)

        df_x = df.loc[:,~df.columns.isin(['Permeabilidad'])]
        df_y = df['Permeabilidad']

        df_x,df_y = self.data_outliers(df_x,df_y)

        df_x = self.normalization_min_max(df_x)

        df_calibres= df_x[['Calibre1','Calibre2','Calibre3','Calibre4','Calibre5','Calibre_Prom']]
        df_x = df_x.loc[:,~df_x.columns.isin(['Calibre1','Calibre2','Calibre3','Calibre4','Calibre5','Calibre_Prom'])]

        x_pca,_ = self.compute_pca(df_to_reduce=df_calibres,n_components=self.pca_components)

        self.df_processed = pd.concat([df_x.reset_index(),pd.DataFrame(x_pca,columns=['comp1_calibre','comp2_calibre']),  df_y.to_frame().reset_index()],  axis=1)

        return self.df_processed 
    
    def data_inputation(self,df: pd.DataFrame)->pd.DataFrame:
        #### DATA INPUTATION ####
        imp_model = KNNImputer(missing_values = np.nan, n_neighbors = 5, weights= "distance")
        imp_model.fit(df)
        imp_model = imp_model.transform(df)

        df_inputed = pd.DataFrame(imp_model, columns = df.columns)
        return df_inputed
        ##########################

    def data_outliers(self,df_x: pd.DataFrame,df_y: pd.DataFrame)->tuple:
        # LOF con MinMax es recomendable usar el hiperparametro n_neighbors con un valor impar
        from sklearn.neighbors import LocalOutlierFactor 
        x_lof_v4 = LocalOutlierFactor(n_neighbors = 5, algorithm = 'auto', contamination = 'auto', metric = 'euclidean') 

        # Se realiza la predicción de los datos atípicos
        x_lof_filter_v4 = x_lof_v4.fit_predict(df_x)
        x_ground_truth_v4 = np.ones(len(df_x), dtype = int)
        
        # Se identifican en que muestras o filas de nuestra base de datos hay presencia de datos atípicos
        x_pos_v4 = np.where(x_lof_filter_v4 == x_ground_truth_v4) 
        x_pos_v4 = np.asarray(x_pos_v4)
        x_pos_v4 = np.hstack(x_pos_v4)

        # Excluimos los
        df_x = df_x.loc[x_pos_v4, :]
        df_y = df_y.loc[x_pos_v4]

        return (df_x,df_y)

    def compute_pca(self,df_to_reduce: pd.DataFrame,n_components: int)->pd.DataFrame:
        # Crear el modelo PCA
        pca = PCA(n_components=n_components)
        x_pca = pca.fit_transform(df_to_reduce)
        # Obtener la varianza explicada
        explained_var = pca.explained_variance_ratio_

        return x_pca,explained_var

    def normalization_min_max(self,df_x: pd.DataFrame) -> pd.DataFrame:
        from sklearn.preprocessing import MinMaxScaler 

        min_max = MinMaxScaler(copy=True, feature_range=(0, 1)) # Método MinMax con valores entre 0 y 1
        min_max = min_max.fit_transform(df_x) # Transformación de los nuevos datos con una escala MinMax
        df_min_max = pd.DataFrame(data = min_max, columns = df_x.columns)

        return df_min_max



# def plot_pca(x_pca: pd.DataFrame):
#     from mpl_toolkits.mplot3d import Axes3D
#     import matplotlib.pyplot as plt

#     fig = plt.figure()
#     ax = fig.add_subplot(111)
#     ax.scatter(x_pca[:,0], x_pca[:,2])
#     ax.set_xlabel('Main component 1')
#     # ax.set_ylabel('Main Component 2')
#     ax.set_ylabel('Main Component 3')
#     plt.show()

# def plot_explained_varaince(explained_var):
#     import matplotlib.pyplot as plt

#     # Graficar la varianza explicada
#     plt.plot(range(1, len(explained_var)+1), explained_var, marker='o')
#     plt.xlabel('Main Component')
#     plt.ylabel('Explained Variance')
#     plt.title('Explained Variance by Main Component')
#     plt.show()

# x_pca,explained_var = compute_pca(df_to_reduce=df_calibres,n_components=3)
# plot_pca(x_pca)
# plot_explained_varaince(explained_var)
    
