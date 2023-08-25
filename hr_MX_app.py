import pandas as pd
import streamlit as st
import requests
import hierarchical_review_plots as hrp


conn = requests.get("http://104.248.109.197:6969/v1/percentile_with_league_id")
larga = pd.DataFrame.from_dict(conn.json())
mp = pd.read_csv("static/minutes_played_23.csv")
names_teams = pd.read_csv("static/names_262_2022.csv")


def list_of_players_in_ws_and_as(longer, played_minutes):
    return [
        jugador
        for jugador in longer.Player.unique().tolist()
        if jugador in played_minutes.player.to_list()
    ]


"""
Esta es una revisión a diferentes niveles.
Primero, seleccionamos la liga.
Una vez que configuremos la liga, en la segunda pestaña podemos ver los equipos de esa liga.
Ya con el equipo, podemos seleccionar a los jugadores de la última pestaña.
"""

league_id_from_name = {"Liga MX": 262, "Liga Expansión": 263, "Liga MX Femenil": 673}
list_of_league = list(league_id_from_name.keys())
player, otro = st.tabs(["Jugador", "Otro"])

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
    radar_player = st.selectbox(f"Seleccciona un jugador:", wy_players)
    player_t = league_players[league_players.Player == radar_player]
    minutes_played = mp[mp.Player == radar_player]["Minutes played"].values[0]
    team_name = mp[(mp.Player == radar_player) & (mp.league_id == league_id)]["Team"].values[0]
    scotland_logo = logo[league_id]
    ac_milan_logo = f"logo_{team_id}"
    pizza_plot = hrp.make_bar_plot_player(
        larga[(larga.Player == radar_player) & (larga.league_id == league_id)],
        radar_player,
        minutes_played,
        team_name,
        league_logo=scotland_logo,
        team_logo=ac_milan_logo,
    )
    st.plotly_chart(pizza_plot, use_container_width=True)

with otro:
    st.subheader("Gráficas de desempeño")


st.markdown("Hecho con 💖 por [nies.futbol](https://nies.futbol)")
