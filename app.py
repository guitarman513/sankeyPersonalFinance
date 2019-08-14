import dash
from dash.dependencies import Input, Output, State
import dash_table
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

SOURCE = [0,0,0,1,3,3,2,2,4,4,4,6,11,6,5,5,5,5,5,5,5,5,5]
TARGET = [4,5,6,5,4,5,4,5,9,8,7,10,10,12,13,14,15,16,17,18,19,20,21]
VALUE = [800,1800,400,1000,5,70,25,75,100,500,230,200,100,200,300,170,1200,250,240,100,400,100,185]
COLORS = ["blue","blue","blue","blue","orange","green","blue",
          "orange","orange","orange","blue","blue","blue","purple",
          "purple","purple","orange","red","red","red","red","red"]
LABELS = ['Job','Parents','Work_Study','Investment_Returns','Tax','Net',
          'Deductions','Social_Security','Federal','State','401k',
          '401k_match','IRA','Groceries','Gas','Rent','Bills','Drinks',
          'Takeout','Shopping','Uber','Other']

data = pd.DataFrame(index=['SOURCE','TARGET','VALUE'], data=[SOURCE,TARGET,VALUE])
data = data.transpose()

namedData = pd.DataFrame(index=['SOURCE','VALUE','TARGET'], data=[
    ['Job','Job','Job','Parents','Investment_Returns','Investment_Returns','Work_Study','Work_Study','Tax','Tax','Tax','Deductions','401k_match','Deductions','Net','Net','Net','Net','Net','Net','Net','Net','Net'],
    VALUE,
    ['Tax','Net','Deductions','Net','Tax','Net','Tax','Net','State','Federal','Social_Security','401k','401k','IRA','Groceries','Gas','Rent','Bills','Drinks','Takeout','Shopping','Uber','Other']]
)
namedData = namedData.transpose()

names = set()
names.update(namedData['SOURCE'].to_list())
names.update(namedData['TARGET'].to_list())

nameList = list(names)
colors2 = []
for name in nameList:
    c_idx = LABELS.index(name)
    colors2.append(COLORS[c_idx])




nameAndColor = pd.DataFrame(index=['NAME','COLOR'],data=[nameList,colors2])
nameAndColor = nameAndColor.transpose()

app.layout = html.Div([

    html.H1("Interactive Personal Finance Visualization"),
    html.P("Many new grads could benefit from a structured budget plan. Especially people who are strapped for cash, it is difficult to allocate your funds. Personal finance is a difficult concept to visualize. An organized diagram with flow sizes corresponding to dollar amounts is easier for people to digest than numbers on a spreadsheet."),
    html.P("The below diagram is an easy way to visualize just how one’s finances are spent. Editing the tables below will live-update the diagram. The tables are filled in with some example text to get you started."),




    html.Div([
    html.Div([
    dcc.Graph(
        id='SANKEY',
        figure = dict(
            data = 
            [
            dict(
                type='sankey',
                domain = dict(
                    x =  [i for i in range(len(data))],
                    y =  [i for i in range(len(data))]
                ),
                label = LABELS,
                color = COLORS,
                node = dict(
                    pad = 40,
                    thickness = 40,
                    line = dict(color = "black", width = 0.5),
                    label = LABELS,
                    color = COLORS
                ),
                link = dict(
                    source = data['SOURCE'].dropna(axis=0, how='any'),
                    target = data['TARGET'].dropna(axis=0, how='any'),
                    value = data['VALUE'].dropna(axis=0, how='any'),
                    #color = data['COLORS'].dropna(axis=0, how='any'),
                )
            )
            ]
        )
    ),
    ],className="twelve columns"),
    ],className="row"),

    # tables
    html.Div([
        html.Div([
        dash_table.DataTable(
            id='flowTable',
            data=namedData.to_dict('records'),
            columns=[{'id': c, 'name': c} for c in data.columns],
            editable=True,
            row_deletable=True
        ),
        ],className="six columns"),
        
        html.Div([
        dash_table.DataTable(
            id='colorTable',
            data=nameAndColor.to_dict('records'),
            columns=[{'id': c, 'name': c} for c in nameAndColor.columns],
            editable=True,
            row_deletable=True
        ),
        ],className="six columns"),
    ],className="row"),
    # buttons
    html.Div([
        html.Div([
        html.Button('Add Flow', id='FLOW_BTN', n_clicks=0),
        ],className="six columns"),
        
        html.Div([
        html.Button('Add Item', id='ITEM_BTN', n_clicks=0),
        ],className="six columns"),
    ],className="row"),

])

@app.callback(
    Output('flowTable', 'data'),
    [Input('FLOW_BTN', 'n_clicks')],
    [State('flowTable', 'data'),
     State('flowTable', 'columns')])
def add_row(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c['id']: '' for c in columns})
    return rows

@app.callback(
    Output('colorTable', 'data'),
    [Input('ITEM_BTN', 'n_clicks')],
    [State('colorTable', 'data'),
     State('colorTable', 'columns')])
def add_row2(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c['id']: '' for c in columns})
    return rows




@app.callback(
    Output('SANKEY', 'figure'),
    [Input('flowTable', 'data'),
     Input('colorTable', 'data')])
def display_output(flows_, colors_):
    # print(len(colors_),colors_)
    # print('\n\n\n')
    # print(len(flows_),flows_)

    LABELS = []
    COLORS = []
    names = set()
    # get all names
    for i in range(len(colors_)):
        dict_ = colors_[i]
        LABELS.append(dict_['NAME'])
        COLORS.append(dict_['COLOR'])

    # loop through all rows of the colors table which has unique labels as well
    for i in range(len(colors_)):
        dict_ = colors_[i]
        LABELS.append(dict_['NAME'])
        COLORS.append(dict_['COLOR'])
    
    source = []
    target = []
    value = []
    # loop through all rows of the flows table to update sankey
    for i in range(len(flows_)):
        dict_ = flows_[i]
        source.append( LABELS.index(dict_['SOURCE'])   )# sankey needs integers
        value.append( dict_['VALUE']   )
        target.append( LABELS.index(dict_['TARGET'])   )
    #print("source: ",source)
    #print("target: ",target)

    return {
        'data': 
            [
            dict(
                type='sankey',
                domain = dict(
                    x =  [i for i in range(len(colors_))],
                    y =  [i for i in range(len(colors_))]
                ),
                #label = LABELS,
                #color = COLORS,
                node = dict(
                    pad = 40,
                    thickness = 40,
                    line = dict(color = "black", width = 0.5),
                    label = LABELS,
                    color = COLORS
                ),
                link = dict(
                    source = source,
                    target = target,
                    value = value,
                    #color = data['COLORS'].dropna(axis=0, how='any'),
                )
            )
            ]
    }


if __name__ == '__main__':
    app.run_server(debug=False)