import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from matplotlib_venn import venn2

st.title('Content GAP')
st.write('Por favor, sube el archivo de referencia y 2 archivos adicionales para comparar.')

# Carga el archivo de referencia y obtiene su nombre
archivo_referencia = st.file_uploader('Sube el archivo de referencia:', type=['xlsx'])
# Obtiene el nombre del dominio y si no lo encuentra añade un texto general
nombre_referencia = archivo_referencia.name.split('-')[0] if archivo_referencia else "Archivo de Referencia"

# Carga otros dos archivos y obtiene sus nombres
archivos = []
nombres_archivos = []
for i in range(1, 3):
    archivo = st.file_uploader(f'Sube el archivo {i}:', type=['xlsx'], key=f'file{i}')
    nombre_archivo = archivo.name.split('-')[0] if archivo else f"Archivo {i}"
    archivos.append(archivo)
    nombres_archivos.append(nombre_archivo)

# Definimos las columnas
guardar_columnas = ['Keyword', 'Position', 'Search Volume', 'URL']

# Si se cargan todos los archivos, realiza el análisis
if archivo_referencia and all(archivos):
    ref_filtro = pd.read_excel(archivo_referencia)[guardar_columnas]

    # Comparar archivo de referencia con el resto
    for i, (archivo, nombre_archivo) in enumerate(zip(archivos, nombres_archivos), start=1):
        arch_filtro = pd.read_excel(archivo)[guardar_columnas]

        k_compartidas = set(ref_filtro['Keyword']) & set(arch_filtro['Keyword'])
        k_unicas_ref = set(ref_filtro['Keyword']) - set(arch_filtro['Keyword'])
        k_unicas_otros = set(arch_filtro['Keyword']) - set(ref_filtro['Keyword'])

        #Diagrama de Venn
        plt.figure(figsize=(10, 6))
        venn = venn2(subsets=(len(k_unicas_ref), len(k_unicas_otros), len(k_compartidas)),
                     set_labels=(nombre_referencia, nombre_archivo))
        plt.title(f"Content GAP entre {nombre_referencia} y {nombre_archivo}")
        st.pyplot(plt)

        col1, col2, col3 = st.columns(3)
        
        with col1:
        # Palabras compartidas
            st.write(f'Compartidas entre {nombre_referencia} y {nombre_archivo}')
            st.dataframe(pd.DataFrame(list(k_compartidas), columns=['Keyword']))
        
        with col2:
        # Palabras únicas del archivo de referencia
            st.write(f'Únicas de {nombre_referencia}')
            st.dataframe(pd.DataFrame(list(k_unicas_ref), columns=['Keyword']))
        
        with col3:
        # Palabras únicas del otro archivo
            st.write(f'Únicas de {nombre_archivo}')
            st.dataframe(pd.DataFrame(list(k_unicas_otros), columns=['Keyword']))
else:
    st.write('Por favor, sube todos los archivos para continuar.')
st.caption('By [David Merelas](https://www.linkedin.com/in/david-merelas/?lipi=urn%3Ali%3Apage%3Ad_flagship3_feed%3B8wejHCrAREOJ9OVT46UkiA%3D%3D) / Hecho con [Streamlit](https://www.streamlit.io/)🎈')