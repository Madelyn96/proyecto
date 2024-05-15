import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

# Dashboard
st.title("Dashboard Interactivo")

# Cargar archivo de datos
uploaded_file = st.file_uploader("Cargar Data", type=["csv", "xlsx", "xls"])

if uploaded_file is not None:
    # Leer el archivo
    if uploaded_file.name.endswith('.csv'):
        data = pd.read_csv(uploaded_file)
    else:
        data = pd.read_excel(uploaded_file)

    # Obtener lista de columnas para filtrar
    filter_columns = data.columns.tolist()
    filter_column_x = st.selectbox("Selecciona una columna para el eje X:", filter_columns)
    filter_column_y = st.selectbox("Selecciona una columna para el eje Y:", filter_columns)

    # Obtener tipo de gráfico
    chart_type = st.selectbox("Selecciona el tipo de gráfico:",
                              ["Gráfico de barras", "Gráfico de dispersión", "Gráfico de líneas",
                               "Gráfico de cajas", "Histograma", "Gráfico de área", "Gráfico de violín"])

    # Gráfico
    st.subheader("Gráfico")

    if chart_type == "Gráfico de barras":
        fig, ax = plt.subplots()
        sns.barplot(x=filter_column_x, y=filter_column_y, data=data, ax=ax)
        st.pyplot(fig)
    elif chart_type == "Gráfico de dispersión":
        fig, ax = plt.subplots()
        sns.scatterplot(x=filter_column_x, y=filter_column_y, data=data, ax=ax)
        st.pyplot(fig)
    elif chart_type == "Gráfico de líneas":
        fig, ax = plt.subplots()
        sns.lineplot(x=filter_column_x, y=filter_column_y, data=data, ax=ax)
        st.pyplot(fig)
    elif chart_type == "Gráfico de cajas":
        st.write("Para el gráfico de cajas, selecciona una sola columna para el eje X.")
        filter_column_x_boxplot = st.selectbox("Selecciona una columna para el eje X del gráfico de cajas:", filter_columns)
        fig, ax = plt.subplots()
        sns.boxplot(x=filter_column_x_boxplot, y=filter_column_y, data=data, ax=ax)
        st.pyplot(fig)
    elif chart_type == "Histograma":
        fig, ax = plt.subplots()
        sns.histplot(data[filter_column_x], ax=ax)
        st.pyplot(fig)
    elif chart_type == "Gráfico de área":
        fig, ax = plt.subplots()
        sns.lineplot(x=filter_column_x, y=filter_column_y, data=data, ax=ax, ci=None)
        ax.fill_between(data[filter_column_x], data[filter_column_y], alpha=0.3)
        st.pyplot(fig)
    elif chart_type == "Gráfico de violín":
        fig, ax = plt.subplots()
        sns.violinplot(x=filter_column_x, y=filter_column_y, data=data, ax=ax)
        st.pyplot(fig)

    # Exportar a PDF y Excel
    if st.button("Exportar a PDF"):
        # Convertir el gráfico en bytes
        pdf_bytes = BytesIO()
        plt.savefig(pdf_bytes, format='pdf')
        plt.close()
        st.download_button(
            label="Descargar gráfico como PDF",
            data=pdf_bytes.getvalue(),
            file_name='grafico.pdf',
            mime='application/pdf'
        )

    if st.button("Exportar a Excel"):
        # Convertir los datos a Excel
        excel_data = BytesIO()
        data.to_excel(excel_data, index=False)
        excel_data.seek(0)
        st.download_button(
            label="Descargar datos como Excel",
            data=excel_data,
            file_name='datos.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
