import plotly.express as px


def make_bar_plot_player(larga, radar_player):
    fig = _set_up_bar_polar(larga, radar_player)
    return _update_bar_polar(fig)


def add_nies_logo(fig):
    fig.add_layout_image(
        dict(
            source="https://raw.githubusercontent.com/niesfutbol/streamlit_nies/develop/static/logo_serie_a.png",
            xref="paper",
            yref="paper",
            x=0.9,
            y=1.05,
            sizex=0.2,
            sizey=0.2,
            xanchor="right",
            yanchor="bottom",
        )
    ).add_layout_image(
        dict(
            source="https://raw.githubusercontent.com/niesfutbol/streamlit_nies/develop/static/logo_nies.png",
            xref="paper",
            yref="paper",
            x=0.05,
            y=0.05,
            sizex=0.2,
            sizey=0.2,
        )
    )
    return fig


def _set_up_bar_polar(larga, radar_player):
    player_t = larga[larga.Player == radar_player]
    fig = px.bar_polar(
        player_t,
        r="deciles",
        theta="variable",
        color="type_variable",
        title=f"Gráfica Radial de Barras Interactiva de {radar_player}",
    )
    return fig


def _update_bar_polar(fig):
    fig.update_traces(showlegend=False)
    fig.update_polars(radialaxis_showticklabels=True)
    fig.update_layout(
        polar_radialaxis_ticksuffix="",
        polar_angularaxis_rotation=90,
        polar_angularaxis_direction="clockwise",
        polar_radialaxis_dtick=10,
        polar_hole=0.10,
    )
    return fig
