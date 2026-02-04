import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import pycountry
import io



# pegar dataframe
df = pd.read_csv("https://raw.github.com/guilhermeonrails/data-jobs/refs/heads/main/salaries.csv")

# rodar função
# dados 5 primeiras linhas
df.head()

# rodar função
# dados 10 primeiras linhas
df.head(10)

# rodar função
# características gerais
df.info()

# rodar função
# estatísticas descritivas das variáveis numéricos
df.describe()

# pedir atributo
# (rows, collums)
df.shape

# printar quantidade de linhas e colunas do df
linhas, colunas = df.shape[0], df.shape[1]
print("linhas:",linhas, "e colunas:", colunas)

# pedir atributo
# nome das colunas
df.columns

# rodar função
# remapear df para df1

column_mapping = {
    "work_year": "ano",
    "experience_level": "senioridade",
    "employment_type": "contrato",
    "job_title": "cargo",
    "salary": "salario",
    "salary_currency": "moeda",
    "salary_in_usd": "usd",
    "employee_residence": "residencia",
    "remote_ratio": "remoto",
    "company_location": "empresa",
    "company_size": "tamanho_empresa"
}

df1 = df.rename(columns=column_mapping)
print("Novos nomes das colunas:")
print(df1.columns)

# rodar função
# contar variável textual
df1["senioridade"].value_counts()

# rodar função
# contar variável textual
df1["contrato"].value_counts()

# rodar função
# contar variável textual
df1["remoto"].value_counts()

# rodar função
# contar variável textual
df1["cargo"].value_counts()

# rodar função
# contar variável textual
df1["tamanho_empresa"].value_counts()

# rodar função
# remapear df1 para df2

senioridade_mapping = {
    "SE": "Sênior",
    "MI": "Pleno",
    "EN": "Júnior",
    "EX": "Executivo"
}

df2 = df1.copy()
df2["senioridade"] = df2["senioridade"].replace(senioridade_mapping)
df2["senioridade"].value_counts()

# rodar função
# remapear df1 para df2

contrato_mapping = {
    "FT": "Tempo Integral",
    "CT": "Contrato",
    "PT": "Meio Período",
    "FL": "Freelancer"
}

df2["contrato"] = df2["contrato"].replace(contrato_mapping)
df2["contrato"].value_counts()

# rodar função
# remapear df1 para df2

remoto_mapping = {
    0: "Presencial",
    50: "Híbrido",
    100: "Remoto",
}

df2["remoto"] = df2["remoto"].replace(remoto_mapping)
df2["remoto"].value_counts()

df2.head()

# rodar função
# dados 5 primeiras linhas
df2.describe()

# rodar função
# dados 5 primeiras linhas com variáveis não numéricas
df2.describe(include="object")

# voltando ao df
# criar cópia de df e apagar os na

df_limpo = df2.copy()

df_limpo = df_limpo.dropna()

df_limpo.isnull().sum()

# rodar função
# convertendo tipo de uma variável

df_limpo

df_limpo.info()

df_limpo["ano"] = df_limpo["ano"].astype("int64")

df_limpo.info()

df_limpo

# criando coluna "residência iso3"

df_limpo['residencia_iso3'] = df_limpo['residencia'].apply(lambda x: pycountry.countries.get(alpha_2=x).alpha_3 if pycountry.countries.get(alpha_2=x) else x)

# criando coluna "nome_país"

df_limpo['nome_país'] = df_limpo['residencia'].apply(lambda x: pycountry.countries.get(alpha_2=x).name if pycountry.countries.get(alpha_2=x) else x)

# configurando tipos > função sorted + função unique

anos_disponiveis = sorted(df_limpo["ano"].unique())
senioridades_disponiveis = sorted(df_limpo['senioridade'].unique())
contratos_disponiveis = sorted(df_limpo['contrato'].unique())
tamanhos_disponiveis = sorted(df_limpo["tamanho_empresa"].unique())

# configurando estrutura da página > função set_page_config

st.set_page_config(
                    page_title="Dashboard de salários na área de dados",
                    page_icon="📊",
                    layout="wide")

# configurando estrutura da página > função sidebar.header

st.sidebar.header("🔍 Filtros")

# configurando estrutura da página > função sidebar.multiselect

anos_selecionados = st.sidebar.multiselect("Ano", anos_disponiveis, default = anos_disponiveis)
senioridades_selecionadas = st.sidebar.multiselect("Senioridade", senioridades_disponiveis, default=senioridades_disponiveis)
contratos_selecionados = st.sidebar.multiselect("Tipo de Contrato", contratos_disponiveis, default=contratos_disponiveis)
tamanhos_selecionados = st.sidebar.multiselect("Tamanho da Empresa", tamanhos_disponiveis, default=tamanhos_disponiveis)

# configurando dataframe principal

df_filtrado = df_limpo[
                (df_limpo['ano'].isin(anos_selecionados)) &
                (df_limpo['senioridade'].isin(senioridades_selecionadas)) &
                (df_limpo['contrato'].isin(contratos_selecionados)) &
                (df_limpo['tamanho_empresa'].isin(tamanhos_selecionados))]

# configurando estrutura da página > função title + função markdown

st.title("Dashboard de Análise de Salários na Área de Dados")
st.markdown("Explore os dados salariais na área de dados nos últimos anos. Utilize os filtros à esquerda para refinar sua análise.")

# configurando análise de dados > métricas Principais (KPIs)

# configurando estrutura da página > função subheader

st.subheader("Métricas gerais (Salário anual em USD)")

# configurando análise de dados > gráfico de barras > gruoupby de cargo

if not df_filtrado.empty:
    salario_medio = df_filtrado['usd'].mean()
    salario_maximo = df_filtrado['usd'].max()
    total_registros = df_filtrado.shape[0]
    cargo_mais_frequente = df_filtrado["cargo"].mode()[0]
else:
    salario_medio, salario_mediano, salario_maximo, total_registros, cargo_mais_comum = 0, 0, 0, ""

col1, col2, col3, col4 = st.columns(4)
col1.metric("Salário médio", f"${salario_medio:,.0f}")
col2.metric("Salário máximo", f"${salario_maximo:,.0f}")
col3.metric("Total de registros", f"{total_registros:,}")
col4.metric("Cargo mais frequente", cargo_mais_frequente)

st.markdown("---")

# configurando análise de dados > gráficos

# configurando estrutura da página > função subheader

st.subheader("Gráficos")

# configurando estrutura da página > função colums + condicionantes

col_graf1, col_graf2 = st.columns(2)

# configurando análise de dados > gráfico de barras > gruoupby de cargo

with col_graf1:
    if not df_filtrado.empty:
        top_cargos = df_filtrado.groupby('cargo')['usd'].mean().nlargest(10).sort_values(ascending=True).reset_index()
        grafico_cargos = px.bar(
            top_cargos,
            x='usd',
            y='cargo',
            orientation='h',
            title="Top 10 cargos por salário médio",
            labels={'usd': 'Média salarial anual (USD)', 'cargo': ''}
        )
        grafico_cargos.update_layout(title_x=0.1, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(grafico_cargos, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de cargos.")

# configurando gráficos > gráfico de histograma > gruoupby de cargo

with col_graf2:
    if not df_filtrado.empty:
        grafico_hist = px.histogram(
            df_filtrado,
            x='usd',
            nbins=30,
            title="Distribuição de salários anuais",
            labels={'usd': 'Faixa salarial (USD)', 'count': ''}
        )
        grafico_hist.update_layout(title_x=0.1)
        st.plotly_chart(grafico_hist, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de distribuição.")

# configurando estrutura da página > função colums + condicionantes

col_graf3, col_graf4 = st.columns(2)

# configurando gráficos > gráfico de torta > gruoupby de cargo

with col_graf3:
    if not df_filtrado.empty:
        remoto_contagem = df_filtrado['remoto'].value_counts().reset_index()
        remoto_contagem.columns = ['tipo_trabalho', 'quantidade']
        grafico_remoto = px.pie(
            remoto_contagem,
            names='tipo_trabalho',
            values='quantidade',
            title='Proporção dos tipos de trabalho',
            hole=0.5
        )
        grafico_remoto.update_traces(textinfo='percent+label')
        grafico_remoto.update_layout(title_x=0.1)
        st.plotly_chart(grafico_remoto, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico dos tipos de trabalho.")

with col_graf4:
    if not df_filtrado.empty:
        df_ds = df_filtrado[df_filtrado['cargo'] == 'Data Scientist']
        media_ds_pais = df_ds.groupby('residencia_iso3')['usd'].mean().reset_index()
        grafico_paises = px.choropleth(media_ds_pais,
            locations='residencia_iso3',
            color='usd',
            color_continuous_scale='rdylgn',
            title='Salário médio de Cientista de Dados por país',
            labels={'usd': 'Salário médio (USD)', 'residencia_iso3': 'País'})
        grafico_paises.update_layout(title_x=0.1)
        st.plotly_chart(grafico_paises, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de países.")

# configurando estrutura da página > função colums + condicionantes
# como eu quis deixar só esse gráfico na linha eu tenho que colocar uma virgula depois do col_graf

col_graf5, = st.columns(1)

# para passar um código do sns + plt do jupyter para o sns + st do vscode
# precisa criar um objeto como para receber boxplot
# precisa mudar as funções plt de title, xlabel e ylabel para funções do st
# precisa mudar a função show do plt para a função pyplot 
# por fim, usa o clf do plt para limpar as configs

with col_graf5:
    if not df_filtrado.empty:
        plt.figure(figsize=(50, 5))
        df_box_1 = sns.boxplot(data = df_filtrado, x = "residencia_iso3", y = "usd", palette = "Set2", hue = "residencia", legend=False)
        df_box_1.set_title("Distribuição salarial por país", fontsize=20)
        df_box_1.set_xlabel("País de Residência", fontsize=15)
        df_box_1.set_ylabel("Salário anual (USD)", fontsize=15)
        st.pyplot(plt.gcf(), use_container_width=True, dpi = 600)
        plt.clf() 
    else:
        st.warning("Nenhum dado disponível para o Boxplot.")

# configurando estrutura da página > função colums + condicionantes
# como eu quis deixar só esse gráfico na linha eu tenho que colocar uma virgula depois do col_graf

col_graf6, = st.columns(1)

# para passar um código do sns + plt do jupyter para o sns + st do vscode
# precisa criar um objeto como para receber boxplot
# precisa mudar as funções plt de title, xlabel e ylabel para funções do st
# precisa mudar a função show do plt para a função pyplot 
# por fim, usa o clf do plt para limpar as configs

with col_graf6:
    if not df_filtrado.empty:
        plt.figure(figsize=(50, 5))
        df_box_2 = sns.boxplot(data = df_filtrado, x = "residencia_iso3", y = "usd", palette = "Set2", hue = "residencia", legend=False)
        df_box_2.set_title("Distribuição salarial por país", fontsize=20)
        df_box_2.set_xlabel("País de Residência", fontsize=15)
        df_box_2.set_ylabel("Salário anual (USD)", fontsize=15)
        f = io.StringIO()
        plt.savefig(f, format="svg")
        st.image(f.getvalue(), use_container_width=True)
        plt.clf() 
    else:
        st.warning("Nenhum dado disponível para o Boxplot.")


# configurando estrutura da página > função colums + condicionantes
# como eu quis deixar só esse gráfico na linha eu tenho que colocar uma virgula depois do col_graf

col_graf7, = st.columns(1)

# para passar um código do sns + plt do jupyter para o sns + st do vscode
# precisa criar um objeto como para receber boxplot
# precisa mudar as funções plt de title, xlabel e ylabel para funções do st
# precisa mudar a função show do plt para a função pyplot 
# por fim, usa o clf do plt para limpar as configs

with col_graf7:
    if not df_filtrado.empty:
        df_box_3 = px.box(df_filtrado, x="residencia", y="usd", title="Distribuição salarial de data scientists por país", labels={'usd': 'Salário anual (USD)', 'residencia': 'País de Residência'})
        st.plotly_chart(df_box_3, use_container_width=True, key="grafico_box_3")
    else:
        st.warning("Nenhum dado disponível para o Boxplot.")


# configurando estrutura da página > função colums + condicionantes
# como eu quis deixar só esse gráfico na linha eu tenho que colocar uma virgula depois do col_graf

col_graf8, = st.columns(1)

# para passar um código do sns + plt do jupyter para o sns + st do vscode
# precisa criar um objeto como para receber boxplot
# precisa mudar as funções plt de title, xlabel e ylabel para funções do st
# precisa mudar a função show do plt para a função pyplot 
# por fim, usa o clf do plt para limpar as configs

with col_graf8:
    if not df_filtrado.empty:
        df_box_4 = px.box(df_filtrado, x="residencia", y="usd", title="Distribuição salarial de data scientists por país", subtitle= "Passe o mouse sobre o ponto para ver o nome do país", hover_data=["nome_país"], hover_name = "nome_país", labels={'usd': 'Salário anual (USD)', 'residencia': 'País de Residência'})
        df_box_4.update_traces(hoverlabel=dict(font_size=16, font_family="Arial"))
        st.plotly_chart(df_box_4, use_container_width=True, key="grafico_box_4")
    else:
        st.warning("Nenhum dado disponível para o Boxplot.")

# configurando estrutura da página > função colums + condicionantes
# como eu quis deixar só esse gráfico na linha eu tenho que colocar uma virgula depois do col_graf

col_graf9, = st.columns(1)

# para passar um código do sns + plt do jupyter para o sns + st do vscode
# precisa criar um objeto como para receber boxplot
# precisa mudar as funções plt de title, xlabel e ylabel para funções do st
# precisa mudar a função show do plt para a função pyplot 
# por fim, usa o clf do plt para limpar as configs

with col_graf9:
    if not df_filtrado.empty:
        ordem_paises = df_filtrado.groupby("nome_país")["usd"].mean().sort_values(ascending=True).index.tolist()
        df_box_5 = px.box(df_filtrado, x="nome_país", y="usd", title="Distribuição salarial de data scientists por país, ordenado por média", subtitle= "Passe o mouse sobre o ponto para ver o nome do país", hover_data=["nome_país"], hover_name = "nome_país", labels={"usd": "Salário anual (USD)", "nome_país": "País de Residência"}, category_orders={"nome_país": ordem_paises})
        df_box_5.update_traces(hoverlabel=dict(font_size=16, font_family="Arial"))
        st.plotly_chart(df_box_5, use_container_width=True, key="grafico_box_5")
    else:
        st.warning("Nenhum dado disponível para o Boxplot.")


# configurando estrutura da página > função colums + condicionantes
# como eu quis deixar só esse gráfico na linha eu tenho que colocar uma virgula depois do col_graf

col_graf10, = st.columns(1)

# para passar um código do sns + plt do jupyter para o sns + st do vscode
# precisa criar um objeto como para receber boxplot
# precisa mudar as funções plt de title, xlabel e ylabel para funções do st
# precisa mudar a função show do plt para a função pyplot 
# por fim, usa o clf do plt para limpar as configs

with col_graf10:
    if not df_filtrado.empty:
        ordem_paises = df_filtrado.groupby("nome_país")["usd"].median().sort_values(ascending=True).index.tolist()
        df_box_6 = px.box(df_filtrado, x="nome_país", y="usd", title="Distribuição salarial de data scientists por país, ordenado por mediana", subtitle= "Passe o mouse sobre o ponto para ver o nome do país", hover_data=["nome_país"], hover_name = "nome_país", labels={"usd": "Salário anual (USD)", "nome_país": "País de Residência"}, category_orders={"nome_país": ordem_paises})
        df_box_6.update_traces(hoverlabel=dict(font_size=16, font_family="Arial"))
        st.plotly_chart(df_box_6, use_container_width=True, key="grafico_box_6")
    else:
        st.warning("Nenhum dado disponível para o Boxplot.")

st.markdown("---")

# --- Tabela de Dados Detalhados ---
st.subheader("Dados Detalhados")
st.dataframe(df_filtrado)