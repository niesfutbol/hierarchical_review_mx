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
This is a hierarchical review.
First, we select the league of our interest.
Once the league is configured, in the second tab, we can see the teams in that league.
Once we choose the team, we can see the members of that team in the last tab.
"""

league_id_from_name = {"Liga MX": 262}
list_of_league = list(league_id_from_name.keys())
league, team, player = st.tabs(["Liga", "Equipo", "Jugador"])

with league:
    st.subheader("Tilt and pressure indices")
    """
    The tilt tells us about the possession of a team's ball in an area where it can do damage, the last third of the pitch.
    The definition of tilt is the percentage of total passes that a team made in the final third of the field.
    For example, suppose that there were ten passes in the last third of the pitch in a game.
    Let's say the home team made seven passes, and the away team made 3.
    So the home team's tilt would be 70%, and the away team's 30%.

    The PPDA is a metric that we use to evaluate the defensive pressure of a team on the opposing
    team. The PPDA measures the number of passes the defending team allows before it takes defensive
    action. These defensive actions can be a steal attempt, an interception, or a foul.

    BDP (Build-Up Disruption) is a metric to measure a team's ability to disrupt the opposing team's
    build-up game. The name refers to the interruption in the construction phase of the play.

    You will find the full description in the blog notes [The inclination and pressure for Napoles](https://www.nies.futbol/2023/05/la-inclinacion-y-la-presion-para-el.html)
    and [Pressure indices: PPDA and Build-Up Disruption](https://www.nies.futbol/2023/04/indices-de-presion-ppda-y-build-up.html).
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
    st.subheader("Consistency in lineups")
    """
    In the figure below, we show a heat map.
    We can see the team's players (including the substitutes) in the lines.
    The columns correspond to the matches played.
    Thus, the color of each box represents the minutes played in a match by each player.

    You will find the complete description in the entry [Consistency in
    lineups](https://www.nies.futbol/2023/08/consistencia-en-las-alineaciones-la.html).
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
    st.subheader("Player performance graph")
    """
    These graphs have a set of metrics selected from artificial intelligence techniques.
    Each bar represents the relative strength of the player in each of the metrics.
    The distance from the bar to the center indicates the percentile compared to the complete database.

    You will find the full description in the entry [Player performance
    graph](https://www.nies.futbol/2023/07/grafica-de-desempeno-de-jugadores.html).
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
