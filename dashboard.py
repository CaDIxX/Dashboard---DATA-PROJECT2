import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title='Dashboard de Venda de Carros',
    page_icon='📊',
    layout="wide"
)

df = (
    pd.read_csv(r"C:\Users\Caio\Desktop\Codigos\IMPACTA\3° Semestre\Aulas DataProject\base_desafio_final\usadas_treino\precos_carros.csv",
            sep=",",
            encoding="utf-8",
            engine="python")
    )

columns_translate = {
    "year": "ano",
    "make": "marca",
    "model": "modelo",
    "trim": "nível de acabamento",
    "body": "carroceria",
    "transmission": "transmissão",
    "vin": "código de identificação",
    "state": "estado(EUA)",
    "condition": "condição",
    "odometer(Km)": "hodômetro",
    "color": "cor externa",
    "interior": "cor interna",
    "seller": "vendedor",
    "mmr": "media de mercado",
    "sellingprice(US$)": "preço de venda(US$)",
    "sale_year": "ano da venda"
}

df = df.rename(columns=columns_translate)

# Criando Filtros
st.sidebar.header("Filtros")

anos_disponiveis = sorted(df['ano'].dropna().unique())
anos_selecionados = st.sidebar.multiselect("Ano", anos_disponiveis, default=anos_disponiveis)

condicao_disponiveis = sorted(df['condição'].unique())
condicao_selecionadas = st.sidebar.multiselect('Condição', condicao_disponiveis, default=condicao_disponiveis)

carroceria_disponiveis = sorted(df['carroceria'].unique())
carroceria_selecionadas = st.sidebar.multiselect('Carroceria', carroceria_disponiveis, default=carroceria_disponiveis)

estados_disponiveis = sorted(df['estado(EUA)'].unique())
estado_selecionados = st.sidebar.multiselect('Estados(EUA)', estados_disponiveis, default=estados_disponiveis)

ano_venda_disponiveis = sorted(df['ano da venda'].unique())
ano_venda_selecionados = st.sidebar.multiselect('Ano da Venda', ano_venda_disponiveis, default=ano_venda_disponiveis)

# O dataframe principal é filtrado com base nas seleções feitas na barra lateral
df_filtrado = df[
    (df['ano'].isin(anos_selecionados)) &
    (df['condição'].isin(condicao_selecionadas)) &
    (df['carroceria'].isin(carroceria_selecionadas)) &
    (df['estado(EUA)'].isin(estado_selecionados)) &
    (df['ano da venda'].isin(ano_venda_selecionados))
]

st.title("Dashboard de Análise de Vendas de Carros")
st.markdown(
    """#### Explore a base de dados de vendas de carros usados, que já foram vendidos no Brasil lá nos EUA, entre 2014 à 2015.
##### **Utilize os filtros a esquerda**.
"""
)

# Métricas Principais

st.subheader("Métricas gerais (valores em USD)")

if not df_filtrado.empty:
    valor_medio = df_filtrado['preço de venda(US$)'].mean()
    valor_maximo = df_filtrado['preço de venda(US$)'].max()
    valor_minimo = df_filtrado['preço de venda(US$)'].min()


    kilometragem_media = df_filtrado['hodômetro'].mean()
    kilometragem_maxima = df_filtrado['hodômetro'].max()
    kilometragem_minima = df_filtrado['hodômetro'].min()
    
    total_registros = df_filtrado.shape[0]
    marca_mais_vendida = df_filtrado['marca'].mode()[0]

else:
    valor_medio, valor_minimo, valor_maximo, kilometragem_minima, kilometragem_media, kilometragem_maxima, total_registros, marca_mais_vendida = 0, 0, 0, 0, 0, 0, 0, ""

col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)


col1.metric("Valor Médio", f"${valor_medio:.2f}")
col2.metric("Valor Maximo", f"${valor_maximo:.2f}")
col3.metric("Valor Minimo", f"${valor_minimo:.2f}")
col4.metric("Total de Vendas", f"{total_registros}")
col5.metric("Quilometragem Média", f"{kilometragem_media:.2f}")
col6.metric("Quilometragem Máxima", f"{kilometragem_maxima:.2f}")
col7.metric("Quilometragem Minima", f"{kilometragem_minima:.2f}")
col8.metric("Marca Mais Frequênte", f"{marca_mais_vendida.capitalize()}")

st.markdown("---")

# Análise Visuais com Plotly
st.subheader("Gráficos")

col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    if not df_filtrado.empty:
        top_condicoes = (df_filtrado.groupby('condição')['preço de venda(US$)']
                      .mean()
                      .nlargest(5)
                      .sort_values(ascending=False)
                      .reset_index())
        
        grafico_condicoes = px.bar(
            top_condicoes,
            x='preço de venda(US$)',
            y='condição',
            orientation='h',
            title="Top 5 de Condições de veiculo.",
            labels={
                'US$': 'Media do Valor da Venda(US$)',
                'condição': ''
            }
        )
        grafico_condicoes.update_layout(title_x=0.1, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(grafico_condicoes, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de condições.")


with col_graf2:
    if not df_filtrado.empty:
        graficos_hist = px.histogram(
            df_filtrado,
            x='preço de venda(US$)',
            nbins=15,
            title='Distibuição de Valor de Venda.(US$)',
            labels={
                'preço de venda(US$)': 'preço de venda(US$)',
                'count': ''
            }
        )
        graficos_hist.update_layout(title_x=0.1)
        st.plotly_chart(graficos_hist, use_container_width=True)
    else:
        st.warning('Nenhum dado para exibir no gráfico de distribuição.')

col_graf3, col_graf4 = st.columns(2)

with col_graf3:
    if not df_filtrado.empty:
        marca_contagem = df_filtrado['marca'].value_counts().reset_index()
        marca_contagem.columns = ['marca', 'quantidades']
        graficos_remoto = px.pie(
            marca_contagem,
            names=marca_contagem.columns[0],
            values=marca_contagem.columns[1],
            title='Proporção das Marcas Vendidas.',
            hole=0.5
        )
        graficos_remoto.update_traces(textinfo='percent+label')
        graficos_remoto.update_layout(title_x=0.1)
        st.plotly_chart(graficos_remoto, use_container_width=True)
    else:
        st.warning('Nenhum dado para exibir no gráfico dos marcas vendidas.')


with col_graf4:
    filtro = (df_filtrado['carroceria']
          .str
          .contains('Sedan',
                    case=False, 
                    na=False)
          )
    df_ds = df_filtrado.loc[filtro].copy()

    if not df_ds.empty:
        media_ds_estado = df_ds.groupby('estado(EUA)')['hodômetro'].mean().reset_index()
        grafico_USA = px.choropleth(
            media_ds_estado,
            locations='estado(EUA)',
            color='hodômetro',
            color_continuous_scale='rdylgn',
            title='Quilometragem média por estado(EUA).',
            labels={
                'hodômetro': 'Quilometragem Média',
                'estado(EUA)': 'estado(EUA)'
            }
        )
        grafico_USA.update_layout(title_x=0.1)
        st.plotly_chart(grafico_USA, use_container_width=True)
    else:
        st.warning("Nenhum veiculo encontrado nos filtros selecionados.")

st.markdown('---')

st.subheader("Dados Detalhados")
st.dataframe(df_filtrado.drop('Unnamed: 0', axis=1))
df_filtrado.to_csv('dados-imersao-final.csv')