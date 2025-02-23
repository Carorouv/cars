import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import numpy as np


link = "https://raw.githubusercontent.com/murpi/wilddata/master/quests/cars.csv"
df_cars = pd.read_csv(link)
#st.write(df_cars)

# créer liste des années pour définir les ticks des graphs par la suite
years = list(pd.unique(df_cars['year']))

# créer colonne puissance moyenne par an
#df_cars['moyenne_puissance_an'] = df_cars.groupby('year')['hp'].transform('mean')


# Ajoutez le code pour afficher les boutons de navigation
st.sidebar.markdown('<style>.sidebar .sidebar-content { width: 100%; } .sidebar .sidebar-content .block-container {display: none;}</style>', unsafe_allow_html=True)
selected_page = st.sidebar.radio("", ['Accueil', 'Corrélations', 'Distributions' ,'Distribution par année', 'Evolutions'])



# Contenu des boutons


# Bouton / page Accueil

if selected_page == "Accueil":
  # Titre et premier paragraphe
  st.markdown("""
    <div style="text-align: center;">
        <h1 style="font-size: 30px;"><strong>Bienvenue sur mon application d'analyse des voitures à travers le temps et les pays</strong></h1>
        </div>
    """, unsafe_allow_html=True)

  st.markdown("""
    <div style="text-align: justify;">
        <p style="font-size: 18px;">Dans cette application, je vous propose plusieurs analyses graphiques réalisées
         à partir d'un jeu de données concernant les voitures sorties entre 1971 et 1983 aux Etats-Unis, en Europe et au Japon. <br>
         La table compte 8 colonnes et 261 entrées.</p>
        <p style="font-size: 18px;font-weight: bold;">Premières entrées de la table utilisée </p>
    </div>
    """, unsafe_allow_html=True)

  st.table(df_cars.head())  

  st.markdown("""
    <div style="text-align: justify;">
        <p style="font-size: 18px;font-weight: bold;">Définition des variables</p>
    </div>
    """, unsafe_allow_html=True)

  # création d'un dictionnaire pour définir les variables
  dico_variables = {'mpg': "Miles per Gallon.Distance effectuée en miles pour une consommation d'un volume de carburant (1 gallon)"
        ,"cylinders": "Nombre de cylindres" 
        ,"cubicinches": "Cylindrée" 
        ,"hp": "Horse power. Puissance" 
        ,"weightlbs": "Poids en livre"
        ,"time-to-60": "Temps nécessaire pour passer de 0 à 60 miles par heure (accélération)" 
        ,"year": "Année de sortie du modèle"
        ,"continent": "Continent de sortie du modèle" }

  # création d'une dataframe à partir du dictionnaire des variables
  df_variables = pd.DataFrame.from_dict(dico_variables, orient='index', columns= ['Définition'])
  
  # affichage de la dataframe de définition des variables
  st.table(df_variables)


# Bouton / page Corrélations


if selected_page == "Corrélations":

  st.markdown("""
    <div style="text-align: center;">
        <h1 style="font-size: 30px;"><strong>Etude des corrélations observables entre les différentes variables</strong><br><br></h1>
        </div>
    """, unsafe_allow_html=True)

  corr = df_cars.corr()
  # Getting the Upper Triangle of the co-relation matrix
  matrix = np.triu(corr)

  heatmap_correlation = plt.figure(figsize=(10, 4))
  sns.heatmap(df_cars.corr(), center=0, cmap = sns.color_palette("vlag", as_cmap=True), mask=matrix, annot = True)
  plt.title("Corrélations")
  st.pyplot(heatmap_correlation.figure)

  # Commentaire
  st.markdown("""
    <div style="text-align: justify;">    
        <p style="font-size: 18px;">Nous pouvons observer :<br>
        - Une corrélation négative forte entre la distance parcourue avec un volume de carburant (mpg) et le poids de la voiture.<br>
        - Une corrélation positive forte entre le nombre de cylindres et respectivement: la cylindrée, la puissance et le poids du véhicule.<br></p>
    </div>
       """, unsafe_allow_html=True)

# Bouton / page Distributions

if selected_page == "Distributions":
  st.markdown("""
    <div style="text-align: center;">
        <h1 style="font-size: 30px;"><strong>Etude de la distribution des variables puissance, 
        nombre de cylindres et mpg pour chaque continent</strong><br><br></h1>
        </div>
    """, unsafe_allow_html=True)


  distrib_puissance = plt.figure(figsize=(10, 4))
  sns.boxplot(data= df_cars, x="continent", y="hp")
  plt.title("Distribution des puissances des voitures")
  st.pyplot(distrib_puissance)


  distrib_cylindree = plt.figure(figsize=(10, 4))
  sns.violinplot(data= df_cars, x="continent", y="cylinders")
  plt.title("Distribution des nombre des cylindres des voitures")
  st.pyplot(distrib_cylindree)


  distrib_mpg = plt.figure(figsize=(10, 4))
  sns.boxplot(data= df_cars, x="continent", y="mpg")
  plt.title('Distribution des voitures selon le "miles par gallon"')
  st.pyplot(distrib_mpg)

  # Note 
  #st.write("Note: le mpg - miles per gallon est la distance effectuée en miles pour une consommation d'un volume de carburant (1 gallon)")
  
  #distrib_cubicinches = plt.figure(figsize=(10, 4))
  #sns.boxplot(data= df_cars, x="continent", y="cubicinches")
  #plt.title('Distribution des cylindrées"')
  #st.pyplot(distrib_cubicinches)


  # Commentaire
  st.markdown("""
    <div style="text-align: left;">    
        <p style="font-size: 18px;">Nous pouvons en conclure que, dans l'échantillon étudié :<br>
        - Les voitures américaines sont globalement plus puissantes.<br>
        - Les voitures américaines ont globalement plus de cylindres.<br>
        - Les voitures américaines sont plus consommatrices en carburant. <br>
        - Les plus économes sont les voitures japonaises. </p>
    </div>
       """, unsafe_allow_html=True)


# Bouton / page Distribution par année

if selected_page == "Distribution par année":

  st.markdown("""
    <div style="text-align: center;">
        <h1 style="font-size: 30px;"><strong>Etude du nombre de modèles sortis chaque année, par continent</strong><br><br></h1>
        </div>
    """, unsafe_allow_html=True)

  # création d'un dropdown pour filtrer les graphs par la suite
  tickers = df_cars["continent"].unique().tolist()
  continents = st.multiselect('Sélectionner les continents:', tickers)

  if not continents:
    st.error("Please select at least one country.")
  else:
    selection_df = df_cars[df_cars['continent'].isin(continents) if continents else True]


# histogramme avec nb de voitures par an et par continent - multiple stack empêche mélange des couleurs
    hist_car_year = plt.figure(figsize=(10, 4))
    sns.histplot(selection_df, x = 'year',  binwidth= 1, hue= 'continent', multiple = 'stack')
    plt.xticks(years)
    plt.title("Nombre de voitures par an")
    st.pyplot(hist_car_year)


# Bouton / page Evolutions

if selected_page == "Evolutions":

  st.markdown("""
    <div style="text-align: center;">
        <h1 style="font-size: 30px;"><strong>Etude de l'évolution des variables puissance, poids et distance parcourue avec un gallon au fil des années</strong><br><br></h1>
        </div>
    """, unsafe_allow_html=True)

  # créer dans la table, les colonnes puissance moyenne / poids moyen et mpg moyen par an
  df_cars['moyenne_puissance_an'] = df_cars.groupby('year')['hp'].transform('mean')
  df_cars['moyenne_poids_an'] = df_cars.groupby('year')['weightlbs'].transform('mean')
  df_cars['moyenne_mpg_an'] = df_cars.groupby('year')['mpg'].transform('mean')


  # courbe de l'évolution de la puissance moyenne des voitures
  #evol_puissance = plt.figure(figsize=(10, 4))
  #sns.lineplot(x = df_cars["year"], y = df_cars['moyenne_puissance_an'], data = df_cars)
  #plt.title("Evolution de la puissance (hp)")
  #plt.xticks(years)
  #st.pyplot(evol_puissance)

  #evol_poids = plt.figure(figsize=(10, 4))
  #sns.lineplot(x = df_cars["year"], y = df_cars['moyenne_poids_an'], data = df_cars)
  #plt.title("Evolution du poids des voitures")
  #plt.xticks(years)
  #st.pyplot(evol_poids)

  

  col1, col2 = st.columns(2, gap = 'medium')

# Premier graphique : Évolution de la puissance moyenne des voitures
  with col1:
    fig1, ax1 = plt.subplots(figsize=(15, 8))
    sns.lineplot(x=df_cars["year"], y=df_cars["moyenne_puissance_an"], ax=ax1)
    ax1.set_title("Évolution de la puissance (hp)", fontdict = { 'fontsize': 40})
    ax1.set_xticks(years)
    ax1.set_ylabel('puissance moyenne', fontsize = 30)
    ax1.set_xlabel('année', fontsize = 30)
    ax1.tick_params(axis='y', labelsize= 30)
    ax1.tick_params(axis='x', labelsize= 22)
    st.pyplot(fig1)

# Deuxième graphique : Évolution du poids des voitures
  with col2:
    fig2, ax2 = plt.subplots(figsize=(15, 8))
    sns.lineplot(x=df_cars["year"], y=df_cars["moyenne_poids_an"], ax=ax2)
    ax2.set_title("Évolution du poids des voitures", fontdict = { 'fontsize': 40})
    ax2.set_xticks(years)
    ax2.set_ylabel('poids moyen', fontsize = 30)
    ax2.set_xlabel('année', fontsize = 30)
    ax2.tick_params(axis='y', labelsize= 30)
    ax2.tick_params(axis='x', labelsize= 22)
    st.pyplot(fig2)






  # Commentaire
  st.markdown("""
    <div style="text-align: justify;">    
        <p style="font-size: 18px;">Les 2 précédentes courbes nous permettent de constater 
        que puissance et poids des voitures sont corrélés positivement et qu'ils ont globalement diminué entre 1971 et 1983. <br><br>
        </p>
    </div>
       """, unsafe_allow_html=True)




  evol_mpg = plt.figure(figsize=(10, 4))
  sns.lineplot(x = df_cars["year"], y = df_cars['moyenne_mpg_an'], data = df_cars)
  plt.title("Evolution de la distance parcourue avec un gallon de carburant")
  plt.xticks(years)
  plt.xlabel('année')
  plt.ylabel('mpg moyen')
  st.pyplot(evol_mpg)


  # Commentaire
  st.markdown("""
    <div style="text-align: justify;">    
        <p style="font-size: 18px;">En parallèle, on observe qu'au fil des années, 
        on parcourt une distance de plus en plus longue avec la même quantité de carburant. <br><br>
        </p>
    </div>
       """, unsafe_allow_html=True)
