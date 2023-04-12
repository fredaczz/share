from dash import Dash, html, dcc, callback, Output, Input, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__)
df = pd.read_excel('sample.xlsx')

app.layout = dbc.Container(
    [
        html.Div([
            html.H1(children='AIA Feedback', style={'textAlign':'center'}),
            dcc.Dropdown(df.journey.unique(), [], id='dropdown-selection', multi=True),
            html.Hr()]), # 空行
        dash_table.DataTable(
            id='dash-table',
            editable=False,
            # page_size=15,  # 设置单页显示15行记录行数
            fixed_rows={'headers': True},  # 滚动的时候每个属性仍然可见
            data = df.to_dict('records'),
            columns=[{'name': column, 'id': column, "type": 'text', "presentation": 'markdown'} for column in df.columns],
            style_table={'height': '600px', 'overflowY': 'auto'},  # 时间滚动条和滚动页面的高度设置 defaults to 500
            style_header={
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
                'maxWidth': 50,
            },
            style_cell={
                'minWidth': 30, 'maxWidth': 60, 'width': 45,
                'textAlign': 'center'  # 文本居中显示
            }
            # style_data_conditional=[
            #     {
            #         'if': {
            #             'filter_query': '{content} contains "AIA"',
            #             'column_id': 'content'
            #         },
            #         'color': 'tomato',
            #         'fontWeight': 'bold'
            #     }]
        )
])

@callback(
    Output('dash-table', 'data'),
    [Input('dropdown-selection', 'value')]
)

def update_table(value):
    # update by choose journey
    if bool(value):
        newdf = df[(df['journey'].isin(value))]
        return newdf.to_dict('records')
    else:
        return df.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)

