import pandas as pd
import streamlit as st
import requests
import hierarchical_review_plots as hrp


conn = requests.get("http://104.248.109.197:6969/v1/percentile_with_league_id")
larga = pd.DataFrame.from_dict(conn.json())
mp = pd.read_csv("static/minutes_played_23.csv")


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

league_id_from_name = {"Liga MX": 262}
list_of_league = list(league_id_from_name.keys())
league, team, player = st.tabs(["Liga", "Equipo", "Jugador"])

with league:
    st.subheader("Inclinación e índices de presión")
    """
    La inclinación nos habla de la posesión del balón que un equipo tiene en una zona en la que puede hacer daño, el último tercio de la cancha.
    La definición de la inclinación es el porcentaje de los pases totales que hizo un equipo en el último tercio de la cancha.
    Por ejemplo, supongamos que en un partido hubo en total 10 pases en el último tercio de la cancha.
    Digamos que el equipo local hizo 7 pases y el equipo visitante hizo 3.
    Entonces la inclinación del equipo local sería del 70% y del equipo visitante del 30%.

    El PPDA es una métrica que utilizamos para evaluar la presión defensiva de un equipo sobre el equipo contrario.
    El PPDA mide la cantidad de pases que permite el equipo defensor antes de que lleve a cabo una acción defensiva.
    Estas acciones defensivas pueden ser un intento de robo de balón, una intercepción o una falta.

    La BDP (_Build-Up Disruption_) es una métrica que utilizamos para medir la capacidad que tiene un
    equipo para interrumpir el juego de construcción del equipo contrario.
    El nombre hace referencia a la interrupción en la fase de construcción de la jugada, también
    conocida como "_build-up_" en inglés.

    Encontrarás la descripción completa en las notas: [La inclinación y la presión para el Napoles](https://www.nies.futbol/2023/05/la-inclinacion-y-la-presion-para-el.html)
    e [Índices de presión: PPDA y Build-Up Disruption](https://www.nies.futbol/2023/04/indices-de-presion-ppda-y-build-up.html).
    """
    league_name = st.selectbox("Select a team:", list_of_league)
    tilt_ppda = pd.read_csv(f"static/xG_build-up_ppda_tilt_{league_id_from_name[league_name]}.csv")
    weighted = pd.read_csv(f"static/weighted_g_and_xg_{league_id_from_name[league_name]}.csv")
    # -------- plot league indices --------
    options = hrp.select_pression_index()
    ppda_plot = hrp.make_tilt_ppda_build_up_disruption(tilt_ppda, options)
    st.altair_chart(ppda_plot)
    # ---------- plot weight --------------
    weight_plot = hrp.make_weighted(weighted)
    st.plotly_chart(weight_plot, use_container_width=True)

with team:
    st.subheader("Consistencia en las alineaciones")
    """
    En la figura de abajo mostramos un mapa de calor.
    En los renglones podemos ver a los jugadores del equipo (incluyendo a los sustitutos).
    Las columnas corresponden a los partidos disputados.
    Así, el color de cada cuadro representa los minutos disputados en un partido por cada jugador.

    Encontrarás la descripción completa en la nota: [Consistencia en las alineaciones](https://www.nies.futbol/2023/08/consistencia-en-las-alineaciones-la.html).
    """
    data = pd.read_csv(f"static/played_minutes_{league_id_from_name[league_name]}.csv")
    teams = data.team.unique().tolist()
    teams.sort()
    team = st.selectbox("Select a team:", teams)
    color = "blues"
    played_minutes = data[data.team == team]
    wy_players = list_of_players_in_ws_and_as(larga, played_minutes)
    # Crear el gráfico de Altair
    hm_consistent = hrp.make_heat_map_of_consistent(data, team, color)
    st.altair_chart(hm_consistent)

with player:
    st.subheader("Gráficas de desempeño")
    """
    Estas gráficas tienen un conjunto de métricas seleccionadas a partir de técnicas de inteligencia
    artificial.
    Cada barra representa la fuerza relativa del jugador en cada una de las métricas.
    La distancia que existe de la barra al centro indica el percentil comparado con la base de datos completa.

    Encontrarás la descripción completa en la nota: [Gráfica de desempeño de jugadores](https://www.nies.futbol/2023/07/grafica-de-desempeno-de-jugadores.html).
    """
    # ------------- game start ------------
    logo = {262: "logo_liga_mx", 135: "logo_serie_a"}
    radar_player = st.selectbox(f"Select a {team}'s player:", wy_players)
    player_t = larga[larga.Player == radar_player]
    minutes_played = mp[mp.Player == radar_player]["Minutes played"].to_list()[0]
    team_id = weighted[weighted.names == team]["team_id"].to_list()[0]
    scotland_logo = f"{logo[league_id_from_name[league_name]]}"
    ac_milan_logo = f"logo_{team_id}"
    pizza_plot = hrp.make_bar_plot_player(
        larga,
        radar_player,
        minutes_played,
        team,
        league_logo=scotland_logo,
        team_logo=ac_milan_logo,
    )
    st.plotly_chart(pizza_plot, use_container_width=True)


st.markdown("Hecho con 💖 por [nies.futbol](https://nies.futbol)")
