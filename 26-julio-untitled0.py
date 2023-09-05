import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Create the dropdown menu options
dropdown_options = [
    {'label': 'Estadísticas anuales', 'value': 'Yearly Statistics'},
    {'label': 'Estadísticas del periodo de recesión', 'value': 'Recession Period Statistics'}
]

year_list = [i for i in range(1980, 2024, 1)]

app.layout = html.Div([
    # Título del dashboard
    html.H1("Tablero de Estadísticas de Automóviles"),

    # Menús desplegables
    html.Label("Seleccione las Estadísticas:"),
    dcc.Dropdown(
        id='statistics_dropdown',
        options=dropdown_options,
        value='Yearly Statistics',
        placeholder='Seleccione una opción'
    ),

    html.Label("Seleccione el Año:"),
    dcc.Dropdown(
        id='year_dropdown',
        options=[{'label': i, 'value': i} for i in year_list],
        value=1980
    ),

    # Contenedor de salida
    html.Div(id='output_container', className='row', style={'marginTop': 20}),
])

@app.callback(
    Output(component_id='output_container', component_property='children'),
    [Input(component_id='statistics_dropdown', component_property='value'),
    Input(component_id='year_dropdown',component_property='value')])

def update_output_container(selected_statistics, selected_year):
    if selected_statistics == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]
        
        # Gráfico de ventas de automóviles durante el periodo de recesión
        recession_chart = dcc.Graph(
            id='recession_graph',
            figure=px.bar(recession_data, x='Year', y='Sales', color='Recession', title="Ventas de Automóviles durante la Recesión")
        )

        # Gráfico del número medio de vehículos vendidos por tipo de vehículo
        avg_sales = recession_data.groupby('Type')['Sales'].mean().reset_index()
        avg_sales_chart = dcc.Graph(
            id='avg_sales_graph',
            figure=px.bar(avg_sales, x='Type', y='Sales', title="Número medio de vehículos vendidos por tipo de vehículo durante la Recesión")
        )
        
        # Gráfico de pastel de la participación total del gasto en publicidad por tipo de vehículo
        total_ad_exp = recession_data.groupby('Type')['Advertisement_budget'].sum().reset_index()
        ad_exp_chart = dcc.Graph(
            id='ad_exp_graph',
            figure=px.pie(total_ad_exp, values='Advertisement_budget', names='Type', title="Participación total del gasto en publicidad por tipo de vehículo durante la Recesión")
        )

        return html.Div([recession_chart, avg_sales_chart, ad_exp_chart])

    elif selected_statistics == 'Yearly Statistics':
        yearly_data = data[data['Year'] == selected_year]

        # Gráfico de ventas de automóviles por año
        yearly_chart = dcc.Graph(
            id='yearly_graph',
            figure=px.bar(yearly_data, x='Year', y='Sales', color='Type', title=f"Ventas de Automóviles por Año: {selected_year}")
        )

        # Gráfico de la tasa de desempleo por año
        unemployment_rate_chart = dcc.Graph(
            id='unemployment_rate_graph',
            figure=px.line(yearly_data, x='Year', y='Unemployment_rate', title=f"Tasa de desempleo por año: {selected_year}")
        )

        return html.Div([yearly_chart, unemployment_rate_chart])

    else:
        return None

if __name__ == '__main__':
    app.run_server(debug=True)
    
    