import altair as alt


def make_heat_map_of_sonsistent(data, team, color):
    played_minutes = data[data.team == team]
    chart = (
        alt.Chart(played_minutes, title=f"Minutes Played by Player and Match: \n{team}")
        .mark_rect()
        .encode(
            alt.X("match:N", sort=alt.EncodingSortField(field="date", order="ascending")).title(
                "Match"
            ),
            alt.Y(
                "player:N",
                sort=alt.EncodingSortField(field="minutes", op="sum", order="descending"),
                title="Player",
            ),
            alt.Color("minutes:Q", scale=alt.Scale(scheme=color)).title("Minutes"),
            tooltip=[
                alt.Tooltip("match:N", title="Match"),
                alt.Tooltip("player:N", title="Player"),
                alt.Tooltip("minutes:Q", title="Minutes"),
            ],
        )
        .configure_view(step=13, strokeWidth=0)
        .configure_axis(domain=False, labelFontSize=10)
    )
    return chart
