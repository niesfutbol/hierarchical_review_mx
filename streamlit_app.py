import altair as alt
import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit_nies as sn


larga = pd.read_csv("static/larga_player.csv")
data = pd.read_csv("static/played_minutes.csv")
# ----------------- game start --------
radar_player = "J. Musiala"

fig = sn.make_bar_plot_player(larga, radar_player)

league, team, player = st.tabs(["League", "Team", "Player"])

with league:
    st.subheader("Gráficas de desempeño")
    """
    Estas gráficas tienen un conjunto de métricas seleccionadas a partir de técnicas de inteligencia artificial.
    Cada barra representa la fuerza relativa del jugador en cada una de las métricas.
    La distancia que existe de la barra al centro indica el percentil comparado con la base de datos completa.

    La descripción completa la encontrarás en la entrada [Gráfica de desempeño de jugadores](https://www.nies.futbol/2023/07/grafica-de-desempeno-de-jugadores.html).
    """
    st.plotly_chart(fig)

with team:
    st.subheader("Gráficas de consistencia")
    """
    En la figura de abajo mostramos un mapa de calor.
    En los renglones podemos ver a los jugadores del equipo (incluyendo a los sustitutos).
    Las columnas corresponden a los partidos disputados.
    Así, el color de cada cuadro representa los minutos disputados en un partido por cada jugador.

    La descripción completa la encontrarás en la entrada [Consistencia en las alineaciones](https://www.nies.futbol/2023/08/consistencia-en-las-alineaciones-la.html).
    """
    teams = ["Cimarrones", "Cancún", "Mineros de Zacatecas"]
    colours = {"Cimarrones": "oranges", "Cancún": "blues", "Mineros de Zacatecas": "reds"}
    team = st.selectbox("Selecciona un equipo:", teams)
    color = colours[team]
    played_minutes = data[data.team == team]

    # Crear el gráfico de Altair
    hm_consistent = sn.make_heat_map_of_sonsistent(data, team, color)
    st.altair_chart(hm_consistent)

with player:
    st.subheader("Gráficas de desempeño")
    """
    Estas gráficas tienen un conjunto de métricas seleccionadas a partir de técnicas de inteligencia artificial.
    Cada barra representa la fuerza relativa del jugador en cada una de las métricas.
    La distancia que existe de la barra al centro indica el percentil comparado con la base de datos completa.

    La descripción completa la encontrarás en la entrada [Gráfica de desempeño de jugadores](https://www.nies.futbol/2023/07/grafica-de-desempeno-de-jugadores.html).
    """
    fig = sn.add_nies_logo(fig)
    st.plotly_chart(fig)


st.markdown("Made with 💖 by [nies.futbol](https://nies.futbol)")
