#%%
# IMPORTAMOS LAS LIBRERIAS NECESARIAS
import pandas as pd

# DEFINIMOS FUNCIONES 
def readFile(file_path):
    try:
        df2 = pd.read_csv(file_path, skiprows=2)
        print('csv')
    except:
        try: 
            df2 = pd.read_excel(file_path, skiprows=2)
            print('excel')
        except:
            print('not file found')
    return df2



# SELECCIONAMOS LOS ARCHIVOS DE INTERÉS EN ESTE CASO SON INFORMES EXTRAIDOS DESDE GOOGLE ADS :
search_path = 'searchTDB.csv'
dsa_path = 'dsaTDB.csv'

# LEEMOS LOS ARCHIVOS Y AGREGAMOS COLUMNA CON NOMBRE ESTRATEGIA
search = readFile(search_path)
search['estrategia'] = 'search'
try:
    search = search.drop(columns='Campaña')
except:
    print('no hay columna campaña')

dsa = readFile(dsa_path)
dsa['estrategia'] = 'dsa'
try:
    dsa = dsa.drop(columns='Campaña')
except:
    print('no hay columna campaña en dsa')

#%%
# SELECCIONAMOS LAS PALABRAS QUE HAYAN TENIDO MÁS DE 50 CLICKS (PARAMETRIZABLE)

# search_ok = search[search['Clics']>50]
# dsa_ok = dsa[dsa['Clics']>50]


search_ok = search.copy()

search_ok['Clics'] = pd.to_numeric(search_ok['Clics'].str.replace(".",""), errors="raise")
dsa_ok = dsa.copy()
dsa_ok['Clics'] = pd.to_numeric(dsa_ok['Clics'].str.replace(".",""), errors="raise")

search_ok = search_ok[search_ok['Clics']>50]
dsa_ok = dsa_ok[dsa_ok['Clics']>50]

#%%

# ARMAMOS LISTA CON LOS TÉRMINOS DE BÚSQUEDA

search_ts = search_ok['Término de búsqueda'].tolist()
dsa_ts = dsa_ok['Término de búsqueda'].tolist()

# RECORREMOS LAS LISTAS PARA COMPARAR MATCH DE PALABRA
palabras = []
cuenta=0
for a in search_ts:
  if a in dsa_ts:
    cuenta = cuenta +1 
    palabras.append(a)
print(cuenta)


# ARMAMOS UN DF DE SEARCH SOLO CON LAS FILAS CORRESPONDIENTES A PALABRAS REPETIDAS
search_coincide = search_ok[search_ok['Término de búsqueda'].isin(palabras)]
# ARMAMOS UN DF DE DSA SOLO CON LAS FILAS CORRESPONDIENTES A PALABRAS REPETIDAS
dsa_coincide =  dsa_ok[dsa_ok['Término de búsqueda'].isin(palabras)]


# CONCATENAMOS LOS DOS DF
frames = [search_coincide, dsa_coincide]
result = pd.concat(frames).drop(columns=['Añadido/excluido','Tipo de campaña']).sort_values(by='Término de búsqueda')

# VEMOS LOS RESULTADOS
result.head()

#%%