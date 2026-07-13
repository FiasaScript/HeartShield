import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

quest=[
    {
    'PERGUNTA' : 'VOCÊ POSSUI HISTÓRICO FAMILIAR DE DOENÇAS CARDÍACAS EM PARENTES DE 01º GRAU?',
    'OPCOES' : ['SIM', 'NÃO', 'NÃO SEI'],
    'PESO' : {'SIM': 2, 'NÃO':0, 'NÃO SEI':1}
    },

    {
    'PERGUNTA' : 'VOCÊ POSSUI PRESSÃO ALTA (HIPERTENSÃO)?',
    'OPCOES' : ['SIM', 'NÃO', 'NÃO SEI'],
    'PESO' : {'SIM': 4, 'NÃO':0, 'NÃO SEI':2}
    },

    {
    'PERGUNTA' : 'VOCÊ POSSUI COLESTEROL ALTO?',
    'OPCOES' : ['SIM', 'NÃO', 'NÃO SEI'],
    'PESO' : {'SIM': 2, 'NÃO':0, 'NÃO SEI':1}
    },
    
    {
    'PERGUNTA' : 'VOCÊ FUMA ATUALMENTE?',
    'OPCOES' : ['SIM', 'NÃO'],
    'PESO' : {'SIM': 4, 'NÃO':0}
    },
    
    {
    'PERGUNTA' : 'VOCÊ POSSUI DIABETES?',
    'OPCOES' : ['SIM', 'NÃO', 'NÃO SEI'],
    'PESO' : {'SIM': 4, 'NÃO':0, 'NÃO SEI':2}
    },

    {
    'PERGUNTA':'VOCÊ CONSOME BEBIDAS ALCOOLICAS FREQUENTEMENTE?',
    'OPCOES': ['SIM','NÃO'],
    'PESO' : {'SIM':1, 'NÃO':0}
    },

    {
    'PERGUNTA':'VOCÊ PRATICA ATIVIDADES FÍSICAS REGULARMENTE (PELO MENOS 3X POR SEMANA)?',
    'OPCOES': ['SIM','NÃO'],
    'PESO' : {'SIM':0, 'NÃO':2}
    },

    {
    'PERGUNTA':'VOCÊ UTILIZA ESTIMULANTES FREQUENTEMENTE (ENERGÉTICOS, EXCESSO DE CAFEÍNA, PRÉ-TREINOS MUITO FORTES, ETC.)',
    'OPCOES': ['SIM','NÃO'],
    'PESO' : {'SIM':1, 'NÃO':0}
    },

    {
    'PERGUNTA':'VOCÊ UTILIZA ANABOLIZANTES OU OUTROS ERGOGÊNICOS HORMONAIS?',
    'OPCOES': ['SIM','NÃO'],
    'PESO' : {'SIM':3, 'NÃO':0}
    },

    {
    'PERGUNTA':'VOCÊ UTILIZA DROGAS ESTIMULANTES SINTÉTICAS (COCAÍNA, MDMA, ANFETAMINAS, ETC.)?',
    'OPCOES': ['SIM','NÃO'],
    'PESO' : {'SIM':5, 'NÃO':0}
    }
]
#DEFINE O VALOR DE ALGUMAS VARIÁVEIS PARA INICIAR A ANAMNESE
if 'etapa' not in st.session_state:
    st.session_state.etapa = 0

if 'respostas' not in st.session_state:
    st.session_state.respostas = {}

if 'dados_usuario' not in st.session_state:
    st.session_state.dados_usuario = {}

#UTILIZANDO O ST.SESSION_STATE INICIA A PRIMEIRA ETAPA DO CÓDIGO
if st.session_state.etapa == 0:
    st.title(':red[ANAMNESE PRIMÁRIA]', text_alignment='center')
    st.write('Antes de classificarmos seu score de risco, responda algumas perguntas para que te conheçamos melhor:')

    nome = st.text_input("Seu Nome:")
    idade = st.number_input("Sua Idade:", min_value=0, max_value=120, step=1)
    peso = st.number_input("Seu Peso (kg):", min_value=0.0, max_value=300.0, step=0.1, format="%.1f")
    altura = st.number_input("Sua Altura (metros):", min_value=0.0, max_value=3.0, step=0.01, format="%.2f")

#TRATAMENTO DE ERROS
    if st.button('COMEÇAR QUESTIONÁRIO'):
     if nome == '':
        st.warning('Por favor, preencha corretamente seus dados para continuarmos!')

    elif altura == 0.0:
        st.warning('Por favor, preencha corretamente seus dados para continuarmos')

    elif peso == 0.0:
         st.warning('Por favor, preencha corretamente seus dados para continuarmos')

#CRIA UM DICIONARIO COM OS DADOS DO USUÁRIO E ATUALIZA O VALOR DA SEÇÃO PARA 1
    else:
        st.session_state.dados_usuario = {
            "Nome": nome,
            "Idade": idade,
            "Peso": peso,
            "Altura": altura
        }

        st.session_state.etapa = 1
        st.rerun()

#INICIA A PRÓXIMA ETAPA COM O QUESTIONÁRIO 
elif st.session_state.etapa > 0 and st.session_state.etapa <= len(quest):
    
    indice_pergunta = st.session_state.etapa - 1

    st.title(f'Pergunta {indice_pergunta+1} de {len(quest)}')

    pergunta_atual = quest[indice_pergunta]
    st.write(f"### {pergunta_atual['PERGUNTA']}")
    
    resposta_usuario = st.radio(
        "Selecione sua resposta:", 
        pergunta_atual["OPCOES"], 
        key=f"radio_{indice_pergunta}"
    )

    if st.button("Próxima Etapa"):
        st.session_state.respostas[indice_pergunta] = resposta_usuario
        st.session_state.etapa += 1
        st.rerun()
    
    if st.button('Voltar'):
        st.session_state.etapa -= 1
        st.session_state.respostas[indice_pergunta] = resposta_usuario
        st.rerun()

#UPLOAD DO ARQUIVO .CSV COM AS FR CARDÍACAS
elif st.session_state.etapa == len(quest)+1:
    st.title('MONITORAMENTO CARDÍACO')
    st.write('AGORA FAÇA O UPLOAD DO ARQUIVO **.CSV** COM AS REFERÊNCIAS DE FREQUÊNCIA CARDÍACA AO LONGO DO MÊS')

    arquivo_csv = st.file_uploader('FAÇA O UPLOAD DO ARQUIVO', type=['csv'])

    if arquivo_csv is not None:
        try:
            df = pd.read_csv(arquivo_csv)

            st.success('Arquivo carregado com sucesso!')
            st.write('PRÉVIA DOS DADOS: ')
            st.dataframe(df.head(3))

            if st.button("Gerar Diagnóstico Final"):
                st.session_state.df_cardiaco = df
                st.session_state.etapa += 1
                st.rerun()
        
        except Exception as e:
            st.error('Erro ao ler o .CSV. Certifique-se de que o arquivo está correto!')

#INICIA A ULTIMA ETAPA COM O CÁLCULO DO SCORE GLOBAL
else:
    st.title(f'RELATÓRIO FINAL: {st.session_state.dados_usuario['Nome']}')

#DEFINE O ARQUIVO .CSV E OS DADOS DO USUÁRIO
    df = st.session_state.df_cardiaco
    dados = st.session_state.dados_usuario

#FAZ ALGUNS CÁLCULOS QUE INFLUENCIARÃO NA CLASSIFICAÇÃO FINAL
    imc = dados['Peso']/(dados['Altura']**2)
    fc_max = 220 - dados['Idade']
    lim_critico = fc_max * 0.85

    score_biometria = 0
    motivos_biometria = []

    if imc > 27.5:
        score_biometria += 3
        motivos_biometria.append(f'IMC ELEVAD ({imc:.1f}): AUMENTO DO DÉBITO CARDÍACO BASAL.')

    if dados['Idade'] < 21 and st.session_state.respostas[9] == 'SIM':
        score_biometria +=3
        motivos_biometria.append('PACIENTE JOVEM + USO DE ESTIMULANTES SINTÉTICOS: ALTÍSSIMO RISCO DE ARRITMIA AGUDA POR HIPERATIVIDADE SIMPÁTICA')

    elif dados['Idade'] > 40:
        score_biometria += 4
        motivos_biometria.append('IDADE > 40 ANOS: RISCO INTRÍNSECO CORONARIANO AUMENTADO.')

    score_quest = 0

#DEFINE O SCORE DO QUESTIONÁRIO RESPONDIDO PELO USUÁRIO
    for i, p in enumerate(quest):
        resp = st.session_state.respostas[i]
        score_quest += p['PESO'][resp]
    
    df['Data_Hora'] = pd.to_datetime(df['Data_Hora'])
    df['Dia'] = df['Data_Hora'].dt.date
    
    #FAZ O RESUMO DO VALOR MÉDIO E MÁXIMO DIÁRIO DO DATAFRAME
    resumo_diario = df.groupby('Dia')['Frequencia_Cardiaca_BPM'].agg(['mean', 'max']).reset_index()

    score_cardiaco = 0
    dias_taquicardia = 0
    dias_criticos = 0

    #DEFINE O SCORE DE DIAS CRÍTICOS E TAQUICARDIA
    for index, linha in resumo_diario.iterrows():
        if linha['mean']>100:
            dias_taquicardia += 1

        if linha['max'] > lim_critico:
            dias_criticos += 1

    if dias_taquicardia == 0:
        score_cardiaco += 0   
    elif dias_taquicardia <= 5:
        score_cardiaco += 2  
    elif dias_taquicardia <= 10:
        score_cardiaco += 5   
    else:
        score_cardiaco += 10  


    if dias_criticos == 0:
        score_cardiaco += 0
    elif dias_criticos <= 5 and st.session_state.respostas[6] == 'NÃO' :
        score_cardiaco += 3
    elif dias_criticos <= 10 and st.session_state.respostas[6] == 'NÃO'  :
        score_cardiaco += 7
    elif dias_criticos <=5 and st.session_state.respostas[6] == 'SIM':
        score_cardiaco -= 3
    elif score_cardiaco <=10 and st.session_state.respostas[6] == 'SIM':
        score_cardiaco -= 2
    else:
        score_cardiaco += 12

    #score_cardiaco = max(-20, score_cardiaco)

#DEFINE O SCORE GLOBAL
    score_global = score_quest + score_cardiaco + score_biometria

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric('Idade', f'{dados['Idade']} anos')
    c2.metric('Peso', f'{dados['Peso']} kg')
    c3.metric('IMC', f'{imc:.1f}')
    c4.metric('Dias Taquicardia Basal', f'{dias_taquicardia} dias')
    c5.metric('Dias em pico crítico', f'{dias_criticos} dias')

    st.divider()

    st.write('Detalhamento dos componentes do Score: ')
    st.write(f'Score do questionário preliminar (Anamnese): **{score_quest}** pontos')
    if dias_criticos <=5 and st.session_state.respostas[6] == 'SIM':
        st.write(f'Score de frequência cardíaca: **{score_cardiaco}** pontos, apesar de seu relatório cardíaco apresentar dias em picos críticos isso está, provavelmente, atrelado ao esforço físico.')
    else:
        st.write(f'Score de frequência cardíaca: **{score_cardiaco}** pontos')
    st.write(f'Score de variáveis biométricas (Idade + Peso): **{score_biometria}** pontos')

    if motivos_biometria:
        with st.expander('Ver alertas de idade e peso'):
            for motivo in motivos_biometria:
                st.warning(motivo)

    st.divider()

    st.header(f'Score global de risco: **{score_global}**')

    if score_global <= 5:
        st.success('Risco Baixo: Indicadores fisiológicos e anamnese dentro dos limites de segurança esperados.')
    
    elif score_global <=15:
        st.warning('Risco Moderado: Presença de taquicardia basal recorrente e/ou fatores de sobrecarga por peso/substâncias. Recomenda-se moderação e exames preventivos')

    else:
        st.error('Risco Crítico Cardiovascular: Sinais severos de superdosagem de estimulantes/ergogênicos, picos perigosos para a idade e sobrecarga miocárdica. Suspensão imediata dos ergogênicos e consulta cardiológica urgente são fortemente recomendadas.')
        
    if st.button('Realizar nova triagem'):
        st.session_state.clear()
        st.rerun()

    st.divider()

    with st.expander('Distribuição da Frequência Cardíaca'):
   
        st.caption("O gráfico abaixo mostra a quantidade de registros em cada faixa de batimento. Barras após a linha tracejada indicam esforço crítico.")
    
        fig, ax = plt.subplots(figsize=(10, 4))
    
        ax.hist(
            df['Frequencia_Cardiaca_BPM'], 
            bins=40, 
            color="#ef4444",      
            edgecolor="white",    
            alpha=0.85            
        )
    
        ax.set_title("Frequência dos Batimentos Registrados", fontsize=12, fontweight='bold', pad=10)
        ax.set_xlabel("Frequência Cardíaca (BPM)", fontsize=10)
        ax.set_ylabel("Quantidade de Registros (Amostras)", fontsize=10)
    
        ax.axvline(
            x=lim_critico, 
            color="orange", 
            linestyle="--", 
            linewidth=2, 
            label=f"Limite Crítico ({int(lim_critico)} BPM)"
        )
    
        ax.grid(axis='y', linestyle=':', alpha=0.6)
        ax.legend(loc="upper right")
    
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
    
        st.pyplot(fig)
