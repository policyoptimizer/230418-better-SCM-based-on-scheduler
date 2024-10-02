import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import json

# Load your data into a DataFrame
equipment_products_df = pd.DataFrame({
    '제품': ['PBX', 'PBX', 'PBX', 'PBX', 'PBX', 'PBX', 'FPESA', 'FPESA', 'FPESA', 'FPESA'],
    '공정': ['ROH용해', 'ROH적가/반응', 'Filter/TOL증류/결정화', '여액증류', 'DMAc증류', '건조', 'FPA/ NaOCl적가/WU', 'TOL증류', 'FPE/MAC적가/WU/냉각', 'FPESC/Cl2적가'],
    '설비1': ['R-5705', 'R-5501', 'R-5703', 'R-5701', 'R-5704', 'FD-5701', 'R-5701', 'R-5501', 'R-5504', 'R-5503'],
    '설비2': ['R-5504', 'R-5501', 'R-5803', 'R-5804', 'R-5503', 'FD-5800', '', '', '', '']
})

equipment_list = [
    'R-5501', 'R-5502', 'R-5503', 'R-5504', 'R-5601', 'R-5603', 'R-5604', 'R-5605',
    'R-5701', 'R-5702', 'R-5703', 'R-5704', 'R-5705', 'R-5801', 'R-5802', 'R-5803',
    'R-5804', 'FC-5501', 'FC-5502', 'FD-5501', 'FD-5601', 'FD-5701', 'FD-5800'
]

#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.Div(id='external-events', children=[
        html.Div('PBX', className='fc-event product-event event-PBX', id={'type': 'product-event', 'index': 'PBX'}),
        html.Div('FPESA', className='fc-event product-event event-FPESA', id={'type': 'product-event', 'index': 'FPESA'}),
        html.Div('FTS', className='fc-event product-event event-FTS', id={'type': 'product-event', 'index': 'FTS'}),
        html.Div('TMCA-Cl', className='fc-event product-event event-TMCA-Cl', id={'type': 'product-event', 'index': 'TMCA-Cl'}),
        html.Div('FP', className='fc-event product-event event-FP', id={'type': 'product-event', 'index': 'FP'}),
        html.Div('IKF-916', className='fc-event product-event event-IKF-916', id={'type': 'product-event', 'index': 'IKF-916'}),
        html.Div('CCA', className='fc-event product-event event-CCA', id={'type': 'product-event', 'index': 'CCA'}),
        html.Div('PC', className='fc-event product-event event-PC', id={'type': 'product-event', 'index': 'PC'}),
        html.Div('ICP 정제', className='fc-event product-event event-ICP', id={'type': 'product-event', 'index': 'ICP 정제'}),
        html.Div('MXL 정제', className='fc-event product-event event-MXL', id={'type': 'product-event', 'index': 'MXL 정제'}),
        html.Div('DCZ 정제', className='fc-event product-event event-DCZ', id={'type': 'product-event', 'index': 'DCZ 정제'}),
    ], style={'display': 'flex', 'justifyContent': 'center', 'gap': '10px', 'padding': '10px'}),
    html.Div(id='calendar'),
    html.Div(id='equipment-list', style={'position': 'absolute', 'right': '0', 'top': '100px', 'width': '200px', 'padding': '10px'}),
    # Hidden divs for storing data
    html.Div(id='events-data', style={'display': 'none'}),
    html.Div(id='equipment-status', style={'display': 'none'}, children=json.dumps({eq: 'idle' for eq in equipment_list})),
    # Modal for selecting process and equipment
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("공정 및 설비 선택")),
        dbc.ModalBody([
            html.Div(id='process-equipment-selection')
        ]),
        dbc.ModalFooter(
            dbc.Button("확인", id="close-modal", className="ms-auto", n_clicks=0)
        ),
    ], id='modal', is_open=False),
])

@app.callback(
    Output('modal', 'is_open'),
    Output('process-equipment-selection', 'children'),
    [Input({'type': 'product-event', 'index': dash.dependencies.ALL}, 'n_clicks')],
    [State('modal', 'is_open')]
)
def display_modal(n_clicks_list, is_open):
    ctx = dash.callback_context
    if not ctx.triggered:
        return is_open, dash.no_update

    # Determine which product was clicked
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if 'product-event' in triggered_id:
        index = json.loads(triggered_id)['index']
        product_name = index

        # Filter processes for the selected product
        processes = equipment_products_df[equipment_products_df['제품'] == product_name]['공정'].unique()
        process_options = [{'label': proc, 'value': proc} for proc in processes]

        return True, [
            html.Label('공정 선택'),
            dcc.Dropdown(id='process-dropdown', options=process_options, value=process_options[0]['value']),
            html.Br(),
            html.Label('설비 선택'),
            dcc.Dropdown(id='equipment-dropdown', multi=True),
        ]
    return is_open, dash.no_update

@app.callback(
    Output('equipment-dropdown', 'options'),
    Input('process-dropdown', 'value'),
    State('process-dropdown', 'options'),
    State('modal', 'is_open')
)
def update_equipment_dropdown(selected_process, process_options, is_open):
    if not is_open or not selected_process:
        return []
    # Get equipment for the selected process
    equipment_df = equipment_products_df[equipment_products_df['공정'] == selected_process]
    equipment_set = set(equipment_df['설비1'].dropna()).union(set(equipment_df['설비2'].dropna()))
    equipment_options = [{'label': eq, 'value': eq} for eq in equipment_set]
    return equipment_options

@app.callback(
    Output('events-data', 'children'),
    Output('equipment-status', 'children'),
    Output('modal', 'is_open'),
    Input('close-modal', 'n_clicks'),
    State('process-dropdown', 'value'),
    State('equipment-dropdown', 'value'),
    State('events-data', 'children'),
    State('equipment-status', 'children'),
    State('modal', 'is_open'),
    prevent_initial_call=True
)
def add_event(n_clicks, process, equipment_selected, events_data, equipment_status, is_open):
    if n_clicks:
        # Load current events
        if events_data:
            events = json.loads(events_data)
        else:
            events = []
        # Add new event
        new_event = {
            'title': process,
            'start': '2023-01-01',  # You can set the date appropriately
            'equipment': equipment_selected
        }
        events.append(new_event)

        # Update equipment status
        if equipment_status:
            equipment_status_dict = json.loads(equipment_status)
        else:
            equipment_status_dict = {eq: 'idle' for eq in equipment_list}
        for eq in equipment_selected:
            equipment_status_dict[eq] = 'busy'

        return json.dumps(events), json.dumps(equipment_status_dict), False
    return dash.no_update, dash.no_update, is_open

@app.callback(
    Output('calendar', 'children'),
    Input('events-data', 'children')
)
def update_calendar(events_data):
    events = json.loads(events_data) if events_data else []
    # Here, you would render the FullCalendar with the events
    # Since Dash doesn't directly support FullCalendar, you might need to embed it using html.Iframe or other methods
    calendar_html = html.Div(id='full-calendar')
    # For simplicity, we'll just display the events as a list
    event_list = html.Ul([html.Li(f"{event['title']} on {event['start']}") for event in events])
    return html.Div([calendar_html, event_list])

@app.callback(
    Output('equipment-list', 'children'),
    Input('equipment-status', 'children')
)
def update_equipment_list(equipment_status):
    equipment_status_dict = json.loads(equipment_status) if equipment_status else {eq: 'idle' for eq in equipment_list}
    equipment_items = []
    for eq in equipment_list:
        status = equipment_status_dict.get(eq, 'idle')
        color = 'green' if status == 'idle' else 'red'
        equipment_items.append(html.Div(f"{eq}: {status}", style={'color': color}))
    return equipment_items

if __name__ == '__main__':
    app.run_server(debug=True)

