import dash                              
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input, State
import pickle
from dash_extensions import Lottie      
import praw
import pandas_datareader.data as web
import dash_bootstrap_components as dbc
import plotly.express as px             
import pandas as pd                     
import datetime
from datetime import datetime, date
import calendar
import dash_table 
import plotly.graph_objs as go


options = dict(loop=True, autoplay=True, rendererSettings=dict(
    preserveAspectRatio='xMidYMid slice'))


# Import  data from pickled dumps **************************************


df = pd.read_pickle("data/aapl_bssg_df")
df_income_statement = pd.read_pickle("data/aapl_income_statement")

df3 = pd.read_pickle("data/income_statements_mix")

df = df.reset_index()
azza = df3.columns.values


today = datetime.today().strftime('%Y-%m-%d')
start = datetime(2016, 1, 1).strftime('%Y-%m-%d')



app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )



# ************************************************************************
app.layout = dbc.Container([

    dbc.Row(
        dbc.Col([
            html.H1("Stock Market Dashboard",
                        className='text-center text-primary mb-4 py-1'),
            dcc.Dropdown(id='stock_selector_MASTER', value="AAPL",
                         options=[{'label': x, 'value': x}
                                  for x in df3.symbol.unique()],
                         style={'color': 'black'
                                }
                        )
                ],
                width={"size": 6, "offset": 3}, 
                ), style={'padding-top': "50px"
                          }
    ),   
    
    dbc.Row([

        dbc.Col([html.P("Stock Price: ",
                        style={"textDecoration": "underline"}),

            dcc.Graph(id='line-fig3', figure={}, style={"height": "100%"})
                 ],  # width={'size':5, 'offset':0, 'order':1},
                xs=10, sm=10, md=10, lg=10, xl=10,  
                style={'opacity': .8, "height": "100%"}
                ),

    ], no_gutters=False, justify='center', className="h-75"),
    
    # 
    dbc.Row([

        dbc.Col([html.P("Company Revenues: ",
                        style={"textDecoration": "underline"}),
                
            dcc.Graph(id='line-fig', figure={})
                 ],  # width={'size':5, 'offset':0, 'order':1},
                xs=12, sm=12, md=12, lg=5, xl=5,  style={'opacity': .8}
                ),

        dbc.Col([
            html.P("Company Operating Income: ",
                   style={"textDecoration": "underline"}),
           
            dcc.Graph(id='line-fig2', figure={})
        ],  # width={'size':5, 'offset':6, 'order':2},
            xs=12, sm=12, md=12, lg=5, xl=5,  style={'opacity': .8}
        ),

    ], no_gutters=False, justify='center', style={'padding-top': "35px"
                                                  }), 

    dbc.Row([
        dbc.Col([
            html.P("Select Company Financial Indicator: ",
                   style={"textDecoration": "underline"}),
            dcc.Dropdown(id='my-checklist',  
                         options=[{'label': x, 'value': x} for x in azza],
                         style={'color': 'black'
                                }
                         ),
            dcc.Graph(id='my-hist', figure={})
        ],  # width={'size':5, 'offset':1},
            xs=12, sm=12, md=12, lg=5, xl=5,  style={'opacity': .8}
        ),
        dbc.Col([
            html.P("Select Company Financial Indicator: ",
                   style={"textDecoration": "underline"}),
            dcc.Dropdown(id='my-checklist2', 
                         options=[{'label': x, 'value': x} for x in azza],
                         style={'color': 'black'
                                }
                         ), 
            dcc.Graph(id='my-hist2', figure={

            })
        ],  # width={'size':5, 'offset':1},
            xs=12, sm=12, md=12, lg=5, xl=5,  style={'opacity': .8}
        ),
    ], align="center", justify='center'),  # Vertical: start, center, end
    
#table row
    dbc.Row(
        dbc.Col([
            html.H1("Reddit News: ",
                    className='text-center text-primary mb-4 py-1'),
            dcc.Dropdown(id='subreddit',   
                         options=[
                             {'label': 'Value Investing', 'value': 'valueinvesting'},
                             {'label': 'Stocks', 'value': 'stocks'}
                                 ],
                         value=["valueinvesting", "stocks"],
                         style={'color': 'black'
                                }
                         ),
            dash_table.DataTable(
                id='mydatatable',
                columns=[],
                data=(),
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'center', 
                            'padding': '5px', 
                            'minWidth': '180px', 'width': '180px', 'maxWidth': '360px',
                            'whiteSpace': 'normal',
                            'height': 'auto',
                            'lineHeight': '15px'},
                style_as_list_view=True,
                style_header={
                    'backgroundColor': 'white',
                    'fontWeight': 'bold'
                },
                page_size=10,
                fixed_rows={'headers': True},
                virtualization=True)



        ], xs=10, sm=10, md=10, lg=10, xl=10, style={'height':'100%'}, 
        ),  no_gutters=False, justify='center', style={'padding-top': "35px",
                                                       'height': '800px'
                                                       }
    )
 #endtable   
], fluid=True, style={"height": "100vh"},)





# Callback section
# ************************************************************************
#datatable
@app.callback(
    Output("mydatatable", 'data'),
    Output("mydatatable", "columns"),
    Input("subreddit", "value"),
)
def get_reddit_subs(subr):
    reddit = praw.Reddit(
        client_id=my_client_id,
        client_secret=my_client_secret,
        user_agent=my_user_agent)
    topics_dict = {"created": [],
                    "title": [], 
                   "body": []}
    subreddit = reddit.subreddit(subr)
    top_subreddit = subreddit.top(limit=10)
    for submission in top_subreddit:
        topics_dict["title"].append(submission.title)
        topics_dict["created"].append(submission.created)
        topics_dict["body"].append(submission.selftext)
    topics_data = pd.DataFrame(topics_dict)
    topics_data['created'] = pd.to_datetime(topics_data['created'], unit='s')
    columns = [{'name': i, 'id': i, } for i in topics_data.columns]
    return topics_data.to_dict('records'), columns







#Charts


@app.callback(
    Output("line-fig3", 'figure'),
    Input("stock_selector_MASTER", "value")
)
def update_line_chart(valor):
    data = web.DataReader(valor, 'yahoo', start, today)
    data = data.reset_index()
    fig = px.area(data, x="Date", y="Close")
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'plot_bgcolor': 'rgba(0,0,0,0)'

    })
    return fig



@app.callback(
    Output("line-fig", 'figure'),
    Input("stock_selector_MASTER", "value")
)
def update_line_chart(value):
    dff = df3.copy()
    dff = dff[dff["symbol"] == value]
    fig = px.area(dff, x="date", y="revenue")
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'plot_bgcolor': 'rgba(0,0,0,0)'

    })
    return fig


@app.callback(
    Output("line-fig2", 'figure'),
    Input("stock_selector_MASTER", "value")
)
def update_line_chart2(value):
    dff = df3.copy()
    dff = dff[dff["symbol"] == value]
    fig = px.area(dff, x="date", y="operatingIncome")    
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'plot_bgcolor': 'rgba(0,0,0,0)'

    })
    return fig




@app.callback(
    Output('my-hist', 'figure'),
    Input('my-checklist', 'value'),
    Input("stock_selector_MASTER", "value")
)
def update_graph(stock_slctd, value):
    dff = df3.copy()
    dff = dff[dff["symbol"] == value]
    fighist = px.bar(dff, x='date', y=stock_slctd, barmode="group")

    return fighist


@app.callback(
    Output('my-hist2', 'figure'),
    Input('my-checklist2', 'value'),
    Input("stock_selector_MASTER", "value")
)
def update_graph2(stock_slctd,value):
    dff = df3.copy()
    dff = dff[dff["symbol"] == value]
    fighist = px.bar(dff, x='date', y=stock_slctd, barmode="group")


    return fighist


if __name__ == '__main__':
    app.run_server(debug=True, port=8000)
