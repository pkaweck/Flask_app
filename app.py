from flask import Flask, render_template, request
import numpy as np
import pandas as pd
import json
import plotly
import plotly.express as px
import pickle
import plotly.graph_objects as go
import pyodbc
import requests
#from dash.dependencies import Input, Output


def ValuePredictor(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1, 9)
    loaded_model = pickle.load(open("model.pkl", "rb"))
    prediction = loaded_model.predict(to_predict)[0]
    return prediction


PASSWORD='PASSWORD'
LOGIN='Login'


#connection_string = f"Driver={{ODBC Driver 13 for SQL Server}};Server=tcp:project-se-server.database.windows.net,1433;Database=project-se-db;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;Authentication=ActiveDirectoryMsi" #authentication=ActiveDirectoryIntegrated
connection_string = f"Driver={{ODBC Driver 13 for SQL Server}};Server=tcp:project-se-server.database.windows.net,1433;Database=project-se-db;Uid={LOGIN};Pwd={PASSWORD};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
cnxn = pyodbc.connect(connection_string)
#cursor = cnxn.cursor()

df = pd.read_csv("C:/Users/Paweł/PycharmProjects/Flask_app/three_class_dataframe_performance.csv")
df_2 = pd.DataFrame({'count' : df.groupby('class')['body_fat_perc'].mean()}).reset_index() 

app = Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def index():
    return render_template('FLASK.html')

@app.route('/results', methods = ['POST', 'GET'])
def results():
    if request.method == 'POST':
        to_predict_dict = request.form.to_dict()
        to_predict_list = list(to_predict_dict.values())
        to_predict_list = list(map(int, to_predict_list))
        prediction = ValuePredictor(to_predict_list)
    
        for keys in to_predict_dict:
            to_predict_dict[keys] = float(to_predict_dict[keys])
        to_predict_dict["class"] = prediction[0]
        html_logics ='https://prod-225.westeurope.logic.azure.com:443/workflows/55ab791140d24da8ac50e8b954781586/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=vr_1CSTIeN0Aqf_5A7x9FwJaxWncXJOQJYYrWWg6K1Q'
        requests.post(html_logics,json=to_predict_dict)


 # WYKRES 1
    sql_query = pd.read_sql_query ('''
        SELECT class, lower_limit as bmi ,count(per.id) as 'count'
        from [dbo].[tbl_performance] as per
        join [dbo].[tbl_range] as rng
        on per.bmi > rng.lower_limit and per.bmi <= rng.upper_limit
        group by class, lower_limit
        order by class asc, lower_limit asc
        '''
        ,cnxn)
    sub_fig1 = px.bar(sql_query,x='bmi',y='count', color='class')
    sub_fig1.update_traces(opacity = 0.75)
    sub_fig1.update_layout(barmode='overlay')
    sub_fig1.add_vline(x=to_predict_dict["bmi"], line_dash = 'dash', line_color = 'firebrick')
    #sub_fig1 = px.histogram(sql_query, x= 'bmi', color = 'class')
    # ,xbins=dict( 
    #     start=15.0,
    #     end=40.0,
    #     size=
    #     0.5
    # ))

    sql_query = pd.read_sql_query ('''
        SELECT class, grip_force, sit_ups, broad_jump_cm, body_fat
        from [dbo].[tbl_performance]
        '''
        ,cnxn)

# WYKRES 2
    # SELECT
    sub_fig2 = px.scatter(sql_query, x="sit_ups", y="broad_jump_cm", color="class", marginal_y="violin",
           marginal_x="box", trendline="ols", template="simple_white")

# WYKRES 3
    df_2 = pd.DataFrame({'count' : sql_query.groupby('class')['body_fat'].mean()}).reset_index() 
    sub_fig3 = px.bar(df_2, x = 'class', y = 'count', color = 'class')

# WYKRES 4
    # SELECT 
    sub_fig4 = px.scatter(sql_query, x="grip_force", y="sit_ups", color="class",size='grip_force', hover_data=['grip_force'])


    graphJSON1 = json.dumps(sub_fig1, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON2 = json.dumps(sub_fig2, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON3 = json.dumps(sub_fig3, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON4 = json.dumps(sub_fig4, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('dashboard.html',graphJSON1 = graphJSON1,
        graphJSON2 = graphJSON2, graphJSON3 = graphJSON3,
        graphJSON4 = graphJSON4, prediction = prediction[0] )



if __name__ == "__main__":
    app.run()

