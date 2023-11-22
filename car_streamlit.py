import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go


link = "https://raw.githubusercontent.com/murpi/wilddata/master/quests/cars.csv"
df_cars = pd.read_csv(link)
#st.write(df_cars)

# créer liste des années pour définir les ticks des graphs par la suite
years = list(pd.unique(df_cars['year']))

# créer colonne puissance moyenne par an
df_cars['moyenne_puissance_an'] = df_cars.groupby('year')['hp'].transform('mean')

heatmap_correlation = plt.figure(figsize=(10, 4))
sns.heatmap(df_cars.corr(), center=0, cmap = sns.color_palette("vlag", as_cmap=True), annot = True)
plt.title("Corrélations")
st.pyplot(heatmap_correlation.figure)


# création d'un dropdown pour filtrer les graphs par la suite
tickers = df_cars["continent"].unique().tolist()
continents = st.multiselect('Sélectionner les continents:', tickers)

if not continents:
        st.error("Please select at least one country.")

else:
	selection_df = df_cars[df_cars['continent'].isin(continents) if continents else True]

# histo avec nb de voitures par an et par continent - multiple stack empêche mélange des couleurs
	hist_car_year = plt.figure(figsize=(10, 4))
	sns.histplot(selection_df, x = 'year',  binwidth= 1, hue= 'continent', multiple = 'stack')
	plt.xticks(years)
	plt.title("Nombre de voitures par an")
	st.pyplot(hist_car_year)


# créer colonne puissance moyenne par an
df_cars['moyenne_puissance_an'] = df_cars.groupby('year')['hp'].transform('mean')

# courbe de l'évolution de la puissance moyenne des voitures
evol_puissance = plt.figure(figsize=(10, 4))
sns.lineplot(x = df_cars["year"], y = df_cars['moyenne_puissance_an'], data = df_cars)
plt.title("Evolution de la puissance (hp)")
plt.xticks(years)
st.pyplot(evol_puissance)



df_cars['moyenne_poids_an'] = df_cars.groupby('year')['weightlbs'].transform('mean')

evol_poids = plt.figure(figsize=(10, 4))
sns.lineplot(x = df_cars["year"], y = df_cars['moyenne_poids_an'], data = df_cars)
plt.title("Evolution du poids des voitures")
plt.xticks(years)
st.pyplot(evol_poids)

st.write("Les 2 précédentes courbes nous permettent de constater que puissance et poids des voitures sont corrélés positivement et qu'ils ont globalement diminué entre 1971 et 1983")


distrib_puissance = plt.figure(figsize=(10, 4))
sns.boxplot(data= df_cars, x="continent", y="hp")
plt.title("Distribution des puissances des voitures")
st.pyplot(distrib_puissance)


distrib_cylindree = plt.figure(figsize=(10, 4))
sns.violinplot(data= df_cars, x="continent", y="cylinders")
plt.title("Distribution des cylindrées des voitures")
st.pyplot(distrib_cylindree)


distrib_mpg = plt.figure(figsize=(10, 4))
sns.boxplot(data= df_cars, x="continent", y="mpg")
plt.title('Distribution des voitures selon le "miles par gallon"')
st.pyplot(distrib_mpg)

st.write("Nous pouvons en conclure que : ")
st.write("Les voitures américaines sont globalement plus puissantes.")
st.write("Les voitures américaines sont globalement de plus grosse cylindrée.")
st.write("Les voitures américaines sont plus consommatrices en carburant. Les plus économes sont les voitures européennes.")

# st.write(df_cars)
