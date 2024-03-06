import pandas as pd
import streamlit as st
import requests
import hierarchical_review_plots as hrp
import plotly.express as px
from PIL import Image


conn = requests.get("http://104.248.109.197:6969/v1/percentile_with_league_id")
larga = pd.DataFrame.from_dict(conn.json())
mp = pd.read_csv("static/minutes_played_23.csv")
groups_and_positions = pd.read_csv("static/groups_players_and_x_y.csv")
groups_and_positions["grupos"] = [
    chr(64 + grupo) for grupo in groups_and_positions["grupos"].to_list()
]

PAGE_TITLE = "Liga MX"
PAGE_ICON = "🇲🇽"
st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)

def list_of_players_in_ws_and_as(longer, played_minutes):
    return [
        jugador
        for jugador in longer.Player.unique().tolist()
        if jugador in played_minutes.player.to_list()
    ]


"""
El objetivo de este análisis es caracterizar el estilo de los jugadores a partir de sus acciones
en el campo de juego.

En la primer pestaña encontrarás un resumen visual del desempeño de las jugadoras y jugadores de las
ligas mexicanas. Estas gráficas mostrarán distintas métricas dependiendo de la categoría a la que
pertenezca cada jugador.

En la segunda pestaña presentamos un resumen de los detalles técnicos del análisis. En NIES
esperamos que esta información sea de su interés.
"""

league_id_from_name = {"Liga MX": 262, "Liga Expansión": 263, "Liga MX Femenil": 673}
list_of_league = list(league_id_from_name.keys())
player, otro = st.tabs(["Jugador", "Explicación"])

with player:
    st.subheader("Gráficas de desempeño")
    league_name = st.selectbox("Selecciona una liga:", list_of_league)
    league_id = league_id_from_name[league_name]
    names_teams = pd.read_csv(f"static/names_{league_id}_2022.csv")
    list_of_teams = names_teams.names.to_list()
    team_name = st.selectbox("Selecciona un equipo:", list_of_teams)
    team_id = names_teams[names_teams.names == team_name]["ids"].to_list()[0]
    league_players = mp[(mp.league_id == league_id) & (mp.Team == team_name)]
    wy_players = league_players["Player"].unique().tolist()
    """
    Estas gráficas tienen un conjunto de métricas seleccionadas a partir de técnicas de inteligencia
    artificial.
    Cada barra representa la fuerza relativa del jugador en cada una de las métricas.
    La distancia que existe de la barra al centro indica el percentil comparado con la base de datos completa.

    Encontrarás la descripción completa en la nota: [Gráfica de desempeño de jugadores](https://www.nies.futbol/2023/07/grafica-de-desempeno-de-jugadores.html).
    """
    # ------------- game start ------------
    logo = {262: "logo_liga_mx", 263: "logo_expansion", 673: "logo_liga_mx_femenil"}
    radar_player = st.selectbox(f"Selecciona un jugador:", wy_players)
    player_id = league_players[league_players.Player == radar_player]["ID"].values[0]
    minutes_played = league_players[league_players.Player == radar_player]["Minutes played"].values[0]
    team_name = league_players[league_players.Player == radar_player]["Team"].values[0]
    scotland_logo = logo[league_id]
    ac_milan_logo = f"logo_{team_id}"
    pizza_plot = hrp.make_bar_plot_player_2(
        larga[larga.ID == player_id],
        radar_player,
        minutes_played,
        team_name,
        league_logo=scotland_logo,
        team_logo=ac_milan_logo,
    )
    st.plotly_chart(pizza_plot, use_container_width=True)

with otro:
    st.subheader("Macro grupo")
    """
    Dividimos al total de jugadores de la base de datos en cinco grupos. Esta clasificación la
    hicimos a partir de técnicas de Inteligencia Artificial. Utilizamos más de 100 mediciones
    que tenemos de cada jugador. Nuestro algoritmo entrenado decidió cuáles eran las variables
    relevantes para agrupar jugadores dependiendo de sus números.

    Utilizamos la base completa que incluye los datos de cerca de 8,000 desempeños anuales, de
    difernetes ligas. Tenemos 3 temporadas de las principales ligas europeas y ligas mexicanas.
    Aquí tenemos dos restricciones, solo aparecen jugadores con más de 900 minutos disputados en una
    temporada y quitamos a los porteros.
    
    En la figura de abajo podemos ver los cinco macrogrupos en los que clasificamos a los jugadores.
    Cada punto representa el desempeño anual de algún jugador. Así, podríamos tener varios puntos
    para un solo jugador, un punto por cada temporada de la que tenemos registro.
    """
    weight_plot = px.scatter(
        groups_and_positions,
        x="x",
        y="y",
        color="grupos",
        labels={
            "grupos": "Grupo",
            "year": "Temporada",
            "y": "",
            "x": "",
        },
        hover_name="Player",
        hover_data={"year": True, "x": False, "y": False},
    ).add_layout_image(
        dict(
            source=Image.open("static/logos/logo_nies.png"),
            xref="paper",
            yref="paper",
            x=0.7,
            y=0.2,
            sizex=0.2,
            sizey=0.2,
        )
    )
    st.plotly_chart(weight_plot, use_container_width=True)


st.markdown("Hecho con 💖 por [nies.futbol](https://nies.futbol)")
