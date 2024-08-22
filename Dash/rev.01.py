import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import datetime

# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# 이벤트 데이터를 저장할 데이터프레임
events_df = pd.DataFrame(columns=["id", "title", "start"])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H4("생산 제품"),
            dbc.Button("EBX", id="add-ebx", color="primary", className="mb-2"),
            dbc.Button("IKF-916", id="add-ikf", color="success", className="mb-2"),
            dbc.Button("CCA", id="add-cca", color="danger", className="mb-2"),
            dbc.Button("PC", id="add-pc", color="warning", className="mb-2"),
        ], width=2),
        dbc.Col([
            dcc.Graph(id="calendar", config={"displayModeBar": False}),
        ], width=10)
    ])
])

@app.callback(
    Output("calendar", "figure"),
    Input("add-ebx", "n_clicks"),
    Input("add-ikf", "n_clicks"),
    Input("add-cca", "n_clicks"),
    Input("add-pc", "n_clicks"),
    State("calendar", "figure"),
)
def update_calendar(ebx_clicks, ikf_clicks, cca_clicks, pc_clicks, figure):
    ctx = dash.callback_context

    if not ctx.triggered:
        return figure
   
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    title = button_id.split("-")[-1].upper()

    # 유니크한 ID 생성 및 현재 시간에 이벤트 추가
    event_id = len(events_df) + 1
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
   
    new_event = pd.DataFrame({
        "id": [event_id],
        "title": [title],
        "start": [start_time]
    })

    global events_df
    events_df = pd.concat([events_df, new_event], ignore_index=True)

    # 캘린더 그래프 업데이트
    figure = {
        "data": [{
            "x": events_df["start"],
            "y": events_df["title"],
            "mode": "markers+text",
            "marker": {"size": 15},
            "text": events_df["title"],
            "textposition": "top center",
        }],
        "layout": {
            "xaxis": {"title": "날짜 및 시간"},
            "yaxis": {"title": "제품"},
            "title": "생산 스케줄",
        }
    }

    return figure

if __name__ == '__main__':
    app.run_server(debug=True)
