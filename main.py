from flask import Flask, render_template, request
import pandas as pd
import json
import json
import plotly
import plotly.express as px
import dash
from dash import dcc,html
from dash.dependencies import Input, Output

df = pd.read_csv("C:/Users/Paweł/PycharmProjects/Flask_app/three_class_dataframe_performance.csv")
df_2 = pd.DataFrame({'count' : df.groupby('class')['body fat_%'].mean()}).reset_index() 

prediction = 'HUJ HUJ HUJ HUJ HUJ HUJ'

app = Flask(__name__)

@app.route('/main', methods = ['POST', 'GET'])
def index():
    return render_template('FLASK.html')

@app.route('/results/', methods = ['POST', 'GET'])
def results():
    if request.method == 'POST':
        form_data = request.form
    sub_fig1 = px.histogram(df, x='BMI')
    
    sub_fig2 = px.bar(df_2, x = 'class', y = 'count')
    # app.layout = html.Div(children=[
    # # elements from the top of the page
    # html.Div([
    #     html.H1(children='Dash app1'),
    #     html.Div(children='''
    #     Dash: First graph.'''),

    #     dcc.Graph(
    #         id='graph1',
    #         figure=sub_fig1
    #     ),
    # ]),
    # # New Div for all elements in the new 'row' of the page
    # html.Div([
    #     html.H1(children='Dash app2'),
    #     html.Div(children='''
    #     Dash: Second graph. '''),

    #     dcc.Graph(
    #         id='graph2',
    #         figure=sub_fig2
    #     ),
    # ]),
    # ])
    graphJSON1 = json.dumps(sub_fig1, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON2 = json.dumps(sub_fig2, cls=plotly.utils.PlotlyJSONEncoder)


    return render_template('dashboard.html',graphJSON1 = graphJSON1,graphJSON2 = graphJSON2, prediction = prediction)



if __name__ == "__main__":
    app.run(debug=True)

