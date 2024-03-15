import streamlit as st
from streamlit_option_menu import option_menu

import pandas as pd
import plotly.express as px
import pymysql
import json
import requests
import PIL
from PIL import Image


# SQL connection
mydb = pymysql.connect(
    host="localhost",
    user="root",
    password="MYSQL0507",
    database="PhonepeData"
)
cursor = mydb.cursor()



#aggregated insurance
cursor.execute("SELECT * FROM aggregated_insurance")
table1 = cursor.fetchall()
mydb.commit()

# Create DataFrame
Aggre_insurance = pd.DataFrame(table1, columns=("States", "Years", "Quarter", "Transaction_type",
                                                "Transaction_count", "Transaction_amount"))

#aggregated transaction
cursor.execute("SELECT * FROM aggregated_transaction")
table2 = cursor.fetchall()
mydb.commit()

# Create DataFrame
Aggre_transaction = pd.DataFrame(table2, columns=("States", "Years", "Quarter", "Transaction_type",
                                                "Transaction_count", "Transaction_amount"))


#aggregated user
cursor.execute("SELECT * FROM aggregated_user")
table3 = cursor.fetchall()
mydb.commit()

# Create DataFrame
Aggre_user = pd.DataFrame(table3, columns=("States", "Years", "Quarter", "Brands",
                                                "Transaction_count", "Percentage"))


 #map insurance
cursor.execute("SELECT * FROM map_insurance")
table4 = cursor.fetchall()
mydb.commit()

# Create DataFrame
map_insurance = pd.DataFrame(table4, columns=("States", "Years", "Quarter", "Districts",
                                                "Transaction_count", "Transaction_amount"))


#map transaction
cursor.execute("SELECT * FROM map_transaction")
table5 = cursor.fetchall()
mydb.commit()

# Create DataFrame
map_transaction = pd.DataFrame(table5, columns=("States", "Years", "Quarter", "Districts",
                                                "Transaction_count", "Transaction_amount"))


#map user
cursor.execute("SELECT * FROM map_user")
table6 = cursor.fetchall()
mydb.commit()

# Create DataFrame
map_user = pd.DataFrame(table6, columns=("States", "Years", "Quarter", "Districts",
                                                "RegisteredUser", "AppOnes"))


#top insurance
cursor.execute("SELECT * FROM top_insurance")
table7 = cursor.fetchall()
mydb.commit()

# Create DataFrame
top_insurance = pd.DataFrame(table7, columns=("States", "Years", "Quarter", "Pincodes",
                                                "Transaction_count", "Transaction_amount"))

#top transaction
cursor.execute("SELECT * FROM top_transaction")
table8 = cursor.fetchall()
mydb.commit()

# Create DataFrame
top_transaction = pd.DataFrame(table8, columns=("States", "Years", "Quarter", "Pincodes",
                                                "Transaction_count", "Transaction_amount"))


#top user
cursor.execute("SELECT * FROM top_user")
table9 = cursor.fetchall()
mydb.commit()

# Create DataFrame
top_user = pd.DataFrame(table9, columns=("States", "Years", "Quarter", "Pincodes",
                                                "RegisteredUsers"))





def Transaction_amount_count_Y(df,year):
    #dataframe
    X=df[df["Years"]==year]
    X.reset_index(drop = True, inplace=True)

    X1=X.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    X1.reset_index(inplace=True)

    #streamlit
    col1,col2=st.columns(2)
    with col1:
        figamount=px.bar(X1,x="States",y="Transaction_amount",title=f"{year} TRANSACTION_AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
        st.plotly_chart(figamount)

    with col2:
        figcount=px.bar(X1,x="States",y="Transaction_count",title=f"{year} TRANSACTION_COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered_r,height=650,width=600)
        st.plotly_chart(figcount)

    
    #indiamap
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data1 = json.loads(response.content)
        states_name = []
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()
    col1,col2=st.columns(2)
    with col1:
        figindia = px.choropleth(X1, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_amount", color_continuous_scale="Rainbow",
                                range_color=(X1["Transaction_amount"].min(), X1["Transaction_amount"].max()), 
                                hover_name="States", title=f"{year} TRANSACTION AMOUNT", fitbounds="locations",
                                height=650, width=600)

        figindia.update_geos(visible=False)
        st.plotly_chart(figindia)

    with col2:
            
        figindia2 = px.choropleth(X1, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_count", color_continuous_scale="Rainbow",
                                range_color=(X1["Transaction_count"].min(), X1["Transaction_count"].max()), 
                                hover_name="States", title=f"{year} TRANSACTION COUNT", fitbounds="locations",
                                height=650, width=600)

        figindia2.update_geos(visible=False)
        st.plotly_chart(figindia2)

        return X

def Transaction_amount_count_Y_Q(df, quarter):
    X = df[df["Quarter"] == quarter]
    X.reset_index(drop=True, inplace=True)

    X1 = X.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    X1.reset_index(inplace=True)


    col1,col2=st.columns(2)
    with col1:

        figamount = px.bar(X1, x="States", y="Transaction_amount", title=f"{X['Years'].unique()} Year {quarter} QUARTER TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, height=650, width=600)
        st.plotly_chart(figamount)

    with col2:
        figcount = px.bar(X1, x="States", y="Transaction_count", title=f"{X['Years'].unique()} Year {quarter} QUARTER TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height=650, width=600)
        st.plotly_chart(figcount)


    col1,col2=st.columns(2)
    with col1:
    
    #india map                                                                                                                                                                             
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data1 = json.loads(response.content)
        states_name = []
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        figindia = px.choropleth(X1, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_amount", color_continuous_scale="Rainbow",
                                range_color=(X1["Transaction_amount"].min(), X1["Transaction_amount"].max()), 
                                hover_name="States", title=f"{X['Years'].unique()} Year {quarter} QUARTER TRANSACTION AMOUNT", fitbounds="locations",
                                height=650, width=600)

        figindia.update_geos(visible=False)
        #figindia.show()
        st.plotly_chart(figindia)


    with col2:
        figindia2 = px.choropleth(X1, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_count", color_continuous_scale="Rainbow",
                                range_color=(X1["Transaction_count"].min(), X1["Transaction_count"].max()), 
                                hover_name="States", title=f"{X['Years'].unique()} Year {quarter} QUARTER TRANSACTION COUNT", fitbounds="locations",
                                height=650, width=600)

        figindia2.update_geos(visible=False)
        #figindia2.show()
        st.plotly_chart(figindia2)
    return X



def Aggre_tran_Transaction_type(df,state):

    X=TAC2[TAC2["States"]== "West Bengal"]
    X.reset_index(drop= True, inplace=True)

    X1=X.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    X1.reset_index(inplace=True)
    #X1

    col1,col2=st.columns(2)
    with col1:
        figpie1=px.pie(data_frame=X1,names="Transaction_type",values="Transaction_amount",
                        width=600,title=f"{state.upper()} TRANSACTION AMOUNT",hole=0.5)
        st.plotly_chart(figpie1)#.show()

    with col2:
        figpie2=px.pie(data_frame=X1,names="Transaction_type",values="Transaction_count",
                        width=600,title=f"{state.upper()} TRANSACTION COUNT",hole=0.5)
        st.plotly_chart(figpie2)#.show()


#AGG_USER_ANALYSIS_1
def Aggre_user_plot_1(df,year):
    AGUY=Aggre_user[Aggre_user["Years"]==year]
    AGUY.reset_index(drop=True,inplace=True)

    AGUYG=pd.DataFrame(AGUY.groupby("Brands")["Transaction_count"].sum())
    AGUYG.reset_index(inplace=True)

    figbar1=px.bar(AGUYG,x="Brands",y="Transaction_count",title=f"{year} BRANDS AND TRANSACTION COUNT",
                width=750,color_discrete_sequence=px.colors.sequential.haline,hover_name="Brands")

    #figbar1.show()
    st.plotly_chart(figbar1)
    return AGUY

#AGGREGATED ANALYSIS USER 2
def Aggre_user_plot_2(df,quarter):
    AGUYQ=df[df["Quarter"]==quarter]
    AGUYQ.reset_index(drop=True,inplace=True)
    

    AGUYQG=pd.DataFrame(AGUYQ.groupby("Brands")["Transaction_count"].sum())
    AGUYQG.reset_index(inplace= True)
    


    figbar1=px.bar(AGUYQG,x="Brands",y="Transaction_count",title=f"{quarter}QUARTER, BRANDS AND TRANSACTION COUNT",
                width=750,color_discrete_sequence=px.colors.sequential.haline,hover_name="Brands")
    st.plotly_chart(figbar1)
    return AGUYQ
#aggregaed user 3
def Aggre_user_plot_3(df, state):
    AGUYQS = df[df["States"] == state] 
    AGUYQS.reset_index(drop=True, inplace=True)

    figline1 = px.line(AGUYQS, x="Brands", y="Transaction_count", hover_data="Percentage",
                       title=f"{state.upper()} BRANDS, TRANSACTION COUNT, PERCENTAGE", width=1000, markers=True)
    st.plotly_chart(figline1)#.show()

#Transaction type 
def Map_ins_dist(df,state):

    X=df[df["States"]== state]
    X.reset_index(drop= True, inplace=True)

    X1=X.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    X1.reset_index(inplace=True)
    #X1

    col1,col2=st.columns(2)
    with col1:
        figpie1=px.bar(data_frame=X1,y="Districts",x="Transaction_amount",orientation="h",height=600,
                        title=f"{state.upper()} DISTRICT AND TRANSACTION AMOUNT",color_discrete_sequence=px.colors.sequential.Mint_r)

        st.plotly_chart(figpie1)#.show()

    with col2:
        figpie2=px.bar(data_frame=X1,y="Districts",x="Transaction_count",orientation="h",height=600,
                        title=f"{state.upper()} DISTRICT AND TRANSACTION COUNT",color_discrete_sequence=px.colors.sequential.Bluered)
        st.plotly_chart(figpie2)#.show()

#Map user plot 1
def map_user_plot1(df,year):
    MUY=df[df["Years"]==year]
    MUY.reset_index(drop=True,inplace=True)

    MUYG=pd.DataFrame(MUY.groupby("States")[["RegisteredUser","AppOnes"]].sum())
    MUYG.reset_index(inplace=True)


    figline1 = px.line(MUYG, x="States", y=["RegisteredUser","AppOnes"],
                        title=f"{year} RESIDTERED USER, APPOPENS", width=700,height=800, markers=True)
    st.plotly_chart(figline1)#.show()

    return MUY

#Map user plot 2
def map_user_plot2(df,quarter):
    MUYQ=df[df["Quarter"]==quarter]
    MUYQ.reset_index(drop=True,inplace=True)

    MUYQG=MUYQ.groupby("States")[["RegisteredUser","AppOnes"]].sum()
    MUYQG.reset_index(inplace=True)


    figline1 = px.line(MUYQG, x="States", y=["RegisteredUser","AppOnes"],
                        title=f"{quarter} REGISTERED USER, APPOPENS", width=1000,height=800, markers=True,
                        color_discrete_sequence=px.colors.sequential.Rainbow)
    st.plotly_chart(figline1)#.show()

    return MUYQ

#map user plot 3
def map_user_plot3(df,states):
    MUYQS=df[df["States"]== states]
    MUYQS.reset_index(drop=True,inplace=True)

    col1,col2=st.columns(2)   
    with col1:  
        figMUbar1=px.bar(MUYQS, x="RegisteredUser",y="Districts",orientation="h",
                        title=f"{states.upper()}REGISTERED USER",height=750, color_discrete_sequence=px.colors.sequential.Aggrnyl)

        st.plotly_chart(figMUbar1)#.show()
    with col2:
        figMUbar2=px.bar(MUYQS, x="AppOnes",y="Districts",orientation="h",
                        title=f"{states.upper()}APP OPENS",height=750, color_discrete_sequence=px.colors.sequential.Aggrnyl)

        st.plotly_chart(figMUbar2)#.show()
        
    #TOP INSURANCE PLOT 1
def Top_ins_plot1(df,state):   
    tiy=df[df["States"]==state]
    tiy.reset_index(drop=True,inplace=True)
    #tiy
    tiyg=pd.DataFrame(tiy.groupby("Pincodes")[["Transaction_count","Transaction_amount"]].sum())
    tiyg.reset_index(inplace=True)
    col1,col2=st.columns(2)
    with col1:
        figTIbar1=px.bar(tiy, y="Transaction_amount",x="Quarter",hover_data="Pincodes",
                        title=f"{state.upper()} TRANSACTION AMOUNT",height=550,width=500, color_discrete_sequence=px.colors.sequential.Aggrnyl_r)

        st.plotly_chart(figTIbar1)#.show()
    with col2:
        figTIbar2=px.bar(tiy, y="Transaction_count",x="Quarter",hover_data="Pincodes",
                        title=f"{state.upper()} TRANSACTION COUNT",height=550,width=500, color_discrete_sequence=px.colors.sequential.Aggrnyl)

        st.plotly_chart(figTIbar2)#.show()
            
#TOP_USER_ANALYSIS_1
def top_user_plot_1(df,year):
    TUY=top_user[top_user["Years"]==year]
    TUY.reset_index(drop=True,inplace=True)

    TUYG=pd.DataFrame(TUY.groupby(["States","Quarter"])["RegisteredUsers"].sum())
    TUYG.reset_index(inplace=True)

    figbar1=px.bar(TUYG,x="States",y="RegisteredUsers",color="Quarter",title=f"{year} REGISTERED USERS",hover_name="States",          
                    width=750,height=700,color_discrete_sequence=px.colors.sequential.Burgyl)
    st.plotly_chart(figbar1)#.show()
    
    return TUY

#top user plot 2
def top_user_plot_2(df,state):    
    TUYS=df[df["States"]==state]
    TUYS.reset_index(drop=True,inplace=True)
    
    figbar1=px.bar(TUYS,x="Quarter",y="RegisteredUsers",color="RegisteredUsers",title=f"{state}REGISTERED USERS/PINCODES/QUARTER",hover_data="Pincodes", 
                    width=750,height=700,color_discrete_sequence=px.colors.sequential.Magenta)
    st.plotly_chart(figbar1)

def TOPCHARTTA(tablename):
    mydb = pymysql.connect(
        host="localhost",
        user="root",
        password="MYSQL0507",
        database="PhonepeData"
    )
    cursor = mydb.cursor()

    query1=f'''SELECT States,SUM(Transaction_amount) as Transaction_amount
                FROM {tablename}
                GROUP BY States
                ORDER BY Transaction_amount DESC
                LIMIT 10;'''
    st.write(query1)
    cursor.execute(query1)
    table=cursor.fetchall()
    mydb.commit()

    df1=pd.DataFrame(table,columns=("States","Transaction_amount"))

    col1,col2=st.columns(2)
    with col1:
        figamount1=px.bar(df1,x="States",y="Transaction_amount",title="TOP 10 TRANSACTION_AMOUNT",hover_name="States",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl,height=450,width=600)
        st.plotly_chart(figamount1)#.show()

    #query2
    query2=f'''SELECT States,SUM(Transaction_amount) as Transaction_amount
                FROM {tablename}
                GROUP BY States
                ORDER BY Transaction_amount 
                LIMIT 10;'''
    cursor.execute(query2)
    table2=cursor.fetchall()
    mydb.commit()

    df2=pd.DataFrame(table2,columns=("States","Transaction_amount"))

    with col2:
        figamount2=px.bar(df2,x="States",y="Transaction_amount",title="LEAST 10 TRANSACTION_AMOUNT",hover_name="States",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=450,width=600)
        st.plotly_chart(figamount2)#.show()

    #query
    query3=f'''SELECT States,AVG(Transaction_amount) as Transaction_amount
                FROM {tablename}
                GROUP BY States
                ORDER BY Transaction_amount;'''
    cursor.execute(query3)
    table3=cursor.fetchall()
    mydb.commit()

    df3=pd.DataFrame(table3,columns=("States","Transaction_amount"))
    figamount3=px.bar(df3,y="States",x="Transaction_amount",title="AVG TRANSACTION_AMOUNT",hover_name="States",orientation="h",
                        color_discrete_sequence=px.colors.sequential.Bluered,height=550,width=600)
    st.plotly_chart(figamount3)#.show()

def TOPCHARTTC(tablename):
    mydb = pymysql.connect(
        host="localhost",
        user="root",
        password="MYSQL0507",
        database="PhonepeData"
    )
    #cursor = connection.cursor()
    cursor = mydb.cursor()

    query1=f'''SELECT States,SUM(Transaction_count) as Transaction_count
                FROM {tablename}
                GROUP BY States
                ORDER BY Transaction_count DESC
                LIMIT 10;'''
    cursor.execute(query1)
    table=cursor.fetchall()
    mydb.commit()

    df1=pd.DataFrame(table,columns=("States","Transaction_count"))
    col1,col2=st.columns(2)
    with col1:
        figamount1=px.bar(df1,x="States",y="Transaction_count",title="TOP 10 TRANSACTION_COUNT",hover_name="States",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl,height=450,width=600)
        st.plotly_chart(figamount1)#.show()

    #query2
    query2=f'''SELECT States,SUM(Transaction_count) as Transaction_count
                FROM {tablename}
                GROUP BY States
                ORDER BY Transaction_count 
                LIMIT 10;'''
    cursor.execute(query2)
    table2=cursor.fetchall()
    mydb.commit()

    df2=pd.DataFrame(table2,columns=("States","Transaction_count"))
    with col2:
    
        figamount2=px.bar(df2,x="States",y="Transaction_count",title="LEAST 10 TRANSACTION_COUNT",hover_name="States",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=450,width=600)
        st.plotly_chart(figamount2)#.show()

    #query
    query3=f'''SELECT States,AVG(Transaction_count) as Transaction_count
                FROM {tablename}
                GROUP BY States
                ORDER BY Transaction_count;'''
    cursor.execute(query3)
    table3=cursor.fetchall()
    mydb.commit()

    df3=pd.DataFrame(table3,columns=("States","Transaction_count"))
    figamount3=px.bar(df3,y="States",x="Transaction_count",title=" AVG TRANSACTION_COUNT",hover_name="States",orientation="h",
                        color_discrete_sequence=px.colors.sequential.Bluered,height=550,width=600)
    st.plotly_chart(figamount3)#.show()
def TOPCHARTRU(tablename,state):
    mydb = pymysql.connect(
        host="localhost",
        user="root",
        password="MYSQL0507",
        database="PhonepeData"
    )
    cursor = mydb.cursor()

    query1=f'''SELECT districts,SUM(registereduser) as registereduser
                FROM {tablename}
                WHERE states='{state}'
                GROUP BY districts
                ORDER BY registereduser DESC
                LIMIT 10;'''
    cursor.execute(query1)
    table=cursor.fetchall()
    mydb.commit()

    df1=pd.DataFrame(table,columns=("districts","registereduser"))
    col1,col2=st.columns(2)
    with col1:
        figamount1=px.bar(df1,x="districts",y="registereduser",title="TOP 10 OF REGISTERED USER",hover_name="districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl,height=450,width=600)
        st.plotly_chart(figamount1)#.show()

    #query2
    query2=f'''SELECT districts,SUM(registereduser) as registereduser
                FROM {tablename}
                WHERE states='{state}'
                GROUP BY districts
                ORDER BY registereduser 
                LIMIT 10;'''
    cursor.execute(query2)
    table2=cursor.fetchall()
    mydb.commit()

    df2=pd.DataFrame(table2,columns=("districts","registereduser"))
    with col2:
        figamount2=px.bar(df2,x="districts",y="registereduser",title="LEAST 10 OF REGISTERED USER",hover_name="districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=450,width=600)
        st.plotly_chart(figamount2)#.show()

    #query
    query3=f'''SELECT districts,SUM(registereduser) as registereduser
                FROM {tablename}
                WHERE states='{state}'
                GROUP BY districts
                ORDER BY registereduser;
                '''
    cursor.execute(query3)
    table3=cursor.fetchall()
    mydb.commit()

    df3=pd.DataFrame(table3,columns=("districts","registereduser"))
    figamount3=px.bar(df3,y="districts",x="registereduser",title="AVERAGE OF REGISTERED USER",hover_name="districts",orientation="h",
                        color_discrete_sequence=px.colors.sequential.Bluered,height=550,width=1000)
    st.plotly_chart(figamount3)#.show()

def TOPCHARTAO(tablename,state):
    mydb = pymysql.connect(
        host="localhost",
        user="root",
        password="MYSQL0507",
        database="PhonepeData"
    )
    cursor = mydb.cursor()

    query1=f'''SELECT districts,SUM(appopens) as appopens
                FROM {tablename}
                WHERE states='{state}'
                GROUP BY districts
                ORDER BY appopens DESC
                LIMIT 10;'''
    cursor.execute(query1)
    table=cursor.fetchall()
    mydb.commit()

    df1=pd.DataFrame(table,columns=("districts","appopens"))

    col1,col2=st.columns(2)
    with col1:
        figamount1=px.bar(df1,x="districts",y="appopens",title="TOP 10 OF APPOPENS",hover_name="districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl,height=450,width=600)
        st.plotly_chart(figamount1)#.show()

    #query2
    query2=f'''SELECT districts,SUM(appopens) as appopens
                FROM {tablename}
                WHERE states='{state}'
                GROUP BY districts
                ORDER BY appopens
                LIMIT 10;'''
    cursor.execute(query2)
    table2=cursor.fetchall()
    mydb.commit()

    df2=pd.DataFrame(table2,columns=("districts","appopens"))
    with col2:
        figamount2=px.bar(df2,x="districts",y="appopens",title="LEAST 10 OF APPOPENS",hover_name="districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=450,width=600)
        st.plotly_chart(figamount2)#.show()

    #query
    query3=f'''SELECT districts,SUM(appopens) as appopens
                FROM {tablename}
                WHERE states='{state}'
                GROUP BY districts
                ORDER BY appopens;
                '''
    cursor.execute(query3)
    table3=cursor.fetchall()
    mydb.commit()

    df3=pd.DataFrame(table3,columns=("districts","appopens"))
    figamount3=px.bar(df3,y="districts",x="appopens",title="AVERAGE OF APPOPENS",hover_name="districts",orientation="h",
                        color_discrete_sequence=px.colors.sequential.Bluered,height=550,width=1000)
    st.plotly_chart(figamount3)#.show()

def TOPCHARTRUs(tablename):
    mydb = pymysql.connect(
        host="localhost",
        user="root",
        password="MYSQL0507",
        database="PhonepeData"
    )
    cursor = mydb.cursor()

    query1=f'''SELECT states,SUM(registeredusers) as registeredusers
                FROM {tablename}
                GROUP BY states
                ORDER BY registeredusers DESC
                LIMIT 10;'''
    cursor.execute(query1)
    table=cursor.fetchall()
    mydb.commit()

    df1=pd.DataFrame(table,columns=("states","registeredusers"))
    col1,col2=st.columns(2)
    with col1:
        figamount1=px.bar(df1,x="states",y="registeredusers",title="TOP 10 OF REGISTERED USER",hover_name="states",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=450,width=600)
        st.plotly_chart(figamount1)#.show()

    #query2
    query2=f'''SELECT states,SUM(registeredusers) as registeredusers
                FROM {tablename}
                GROUP BY states
                ORDER BY registeredusers
                LIMIT 10;'''
    cursor.execute(query2)
    table2=cursor.fetchall()
    mydb.commit()

    df2=pd.DataFrame(table2,columns=("states","registeredusers"))
    with col2:
        figamount2=px.bar(df2,x="states",y="registeredusers",title="LEAST 10 OF REGISTERED USER",hover_name="states",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=450,width=600)
        st.plotly_chart(figamount2)#.show()

    #query
    query3=f'''SELECT states,SUM(registeredusers) as registeredusers
                FROM {tablename}
                GROUP BY states
                ORDER BY registeredusers;
                '''
    cursor.execute(query3)
    table3=cursor.fetchall()
    mydb.commit()

    df3=pd.DataFrame(table3,columns=("states","registeredusers"))
    figamount3=px.bar(df3,y="states",x="registeredusers",title="AVERAGE OF REGISTERED USER",hover_name="states",orientation="h",
                        color_discrete_sequence=px.colors.sequential.Bluered,height=550,width=1000)
    st.plotly_chart(figamount3)#.show()   

#Streamlit part
st.set_page_config(layout="wide")
st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")

with st.sidebar:
    #st.write("maha")
    select=option_menu("Main Menu",["HOME","DATA EXPLORATION","TOP CHARTS"])

if select=="HOME":
    col1,col2 = st.columns(2)
    with col1:
        #st.image(Image.open(r"C:\Users\ADMIN\Desktop\Project1\phonepepic.jpeg file"), width=500)
        st.image(Image.open(r"C:\Users\ADMIN\Desktop\Project1\phonepepic.jpeg"), width=500)

    with col2:
        st.title(':violet[PHONEPE PULSE DATA VISUALISATION]')
        st.subheader(':violet[Phonepe Pulse]:')
        st.write('PhonePe Pulse is a feature offered by the Indian digital payments platform called PhonePe.PhonePe Pulse provides users with insights and trends related to their digital transactions and usage patterns on the PhonePe app.')
        st.subheader(':violet[Phonepe Pulse Data Visualisation]:')
        st.write('Data visualization refers to the graphical representation of data using charts, graphs, and other visual elements to facilitate understanding and analysis in a visually appealing manner.'
                 'The goal is to extract this data and process it to obtain insights and information that can be visualized in a user-friendly manner.')
        st.markdown("## :violet[Done by] : MAHADEVAN A")
        st.markdown("[Inspired from](https://www.phonepe.com/pulse/)")
        st.markdown("[Githublink](https://github.com/Mahadevan0507)")
        st.markdown("[LinkedIn](https://www.linkedin.com/in/mahadevan-arunachalam-8a8b21217)")
    st.write("---")

elif select=="DATA EXPLORATION":

     tab1,tab2,tab3=st.tabs(["Aggregated Analysis","Map Analysis","Top Analysis"])

     with tab1:
         
         method=st.radio("Select The Method",["Insurance Analysis","Transaction Analysis","User Analysis"])

         if method=="Insurance Analysis":
             
            col1,col2=st.columns(2)
            
            with col1:
                 years=st.slider("Select The Year",Aggre_insurance["Years"].min(),Aggre_insurance["Years"].max(),Aggre_insurance["Years"].min())
            TAC=Transaction_amount_count_Y(Aggre_insurance,years)

            col1,col2=st.columns(2)
            
            with col1:
                 quarters=st.slider("Select The Quarter",TAC["Quarter"].min(),TAC["Quarter"].max(),TAC["Quarter"].min())

            Transaction_amount_count_Y_Q(TAC, quarters)

         
         elif method=="Transaction Analysis":
             
             col1,col2=st.columns(2)
             with col1:
                 
                  years=st.slider("Select the Year",Aggre_transaction["Years"].min(),Aggre_transaction["Years"].max(),Aggre_transaction["Years"].min())
                  TAC2=Transaction_amount_count_Y(Aggre_transaction,years)
             
             col1,col2=st.columns(2)
             with col1:
                states=st.selectbox("Select The State",TAC2["States"].unique())

             Aggre_tran_Transaction_type(TAC2,states)

             col1,col2=st.columns(2)
            
             with col1:
                 quarters=st.slider("Select The Quarter",TAC2["Quarter"].min(),TAC2["Quarter"].max(),TAC2["Quarter"].min())

             ATTYQ=Transaction_amount_count_Y_Q(TAC2, quarters)

             col1,col2=st.columns(2)
             with col1:
                states=st.selectbox("Select The State_TY",ATTYQ["States"].unique())
                Aggre_tran_Transaction_type(ATTYQ,states)

         
         elif method=="User Analysis":
             
             col1,col2=st.columns(2)
             with col1:                
                  years=st.slider("Select the Year",Aggre_user["Years"].min(),Aggre_user["Years"].max(),Aggre_user["Years"].min())
             Aggre_user_Y=Aggre_user_plot_1(Aggre_user,years)

             col1,col2=st.columns(2)
            
             with col1:
                 quarters=st.slider("Select The Quarter",Aggre_user_Y["Quarter"].min(),Aggre_user_Y["Quarter"].max(),Aggre_user_Y["Quarter"].min())
             Aggre_user_Y_Q=Aggre_user_plot_2(Aggre_user_Y, quarters)

            
             col1,col2=st.columns(2)
             with col1:
                states=st.selectbox("Select The State",Aggre_user_Y_Q["States"].unique())

             Aggre_user_plot_3(Aggre_user_Y_Q,states)


    
     with tab2:
         
         method2=st.radio("Select The Method",["Map Insurance","Map Transaction","Map User"])

         if method2=="Map Insurance":
             
             col1,col2=st.columns(2)
             with col1:
                 
                  years=st.slider("Select the Year",map_insurance["Years"].min(),map_insurance["Years"].max(),map_insurance["Years"].min())
                  MITY=Transaction_amount_count_Y(map_insurance,years)

             col1,col2=st.columns(2)
             with col1:
                states=st.selectbox("Select The State_MAPINSURANCE",MITY["States"].unique())
             Map_ins_dist(MITY,states)

            
             col1,col2=st.columns(2)
            
             with col1:
                 quarters=st.slider("Select The Quarter_MI",MITY["Quarter"].min(),MITY["Quarter"].max(),MITY["Quarter"].min())
             MITYQ=Transaction_amount_count_Y_Q(MITY, quarters)

             col1,col2=st.columns(2)
             with col1:
                states=st.selectbox("Select The State_st",MITYQ["States"].unique())
             Map_ins_dist(MITYQ,states)


         elif method2=="Map Transaction":
             col1,col2=st.columns(2)
             with col1:
                 
                  years=st.slider("Select the Year",map_transaction["Years"].min(),map_transaction["Years"].max(),map_transaction["Years"].min())
                  MTTY=Transaction_amount_count_Y(map_transaction,years)

             col1,col2=st.columns(2)
             with col1:
                states=st.selectbox("Select The State_MT",MTTY["States"].unique())
             Map_ins_dist(MTTY,states)

            
             col1,col2=st.columns(2)
            
             with col1:
                 quarters=st.slider("Select The Quarter_MT",MTTY["Quarter"].min(),MTTY["Quarter"].max(),MTTY["Quarter"].min())
             MTTYQ=Transaction_amount_count_Y_Q(MTTY, quarters)

             col1,col2=st.columns(2)
             with col1:
                states=st.selectbox("Select The State_st",MTTYQ["States"].unique())
             Map_ins_dist(MTTYQ,states)
         
         elif method2=="Map User":
             
             col1,col2=st.columns(2)
             with col1:                
                  years=st.slider("Select the Year_MU",map_user["Years"].min(),map_user["Years"].max(),map_user["Years"].min())
                  MUY1=map_user_plot1(map_user,years)
            
             
             col1,col2=st.columns(2)
             with col1:
                 quarters=st.slider("Select The Quarter_MU",MUY1["Quarter"].min(),MUY1["Quarter"].max(),MUY1["Quarter"].min())
                 MUYQ1=map_user_plot2(MUY1, quarters)

             col1,col2=st.columns(2)
             with col1:
                states=st.selectbox("Select The State_MU",MUYQ1["States"].unique())
                MUYQS=map_user_plot3(MUYQ1,states)
         

     with tab3:
         
         method3=st.radio("Select The Method",["Top Insurance","Top Transaction","Top User"])

         if method3=="Top Insurance":
             col1,col2=st.columns(2)
             with col1:                 
                  years=st.slider("Select the Year_TI",top_insurance["Years"].min(),top_insurance["Years"].max(),top_insurance["Years"].min())
                  tITY=Transaction_amount_count_Y(top_insurance,years)

             col1,col2=st.columns(2)
             with col1:
                states=st.selectbox("Select The State_TI",tITY["States"].unique())
                Top_ins_plot1(tITY,states)
         
             col1,col2=st.columns(2)
             with col1:
                 quarters=st.slider("Select The Quarter_TI",tITY["Quarter"].min(),tITY["Quarter"].max(),tITY["Quarter"].min())
                 tIYQ1=Transaction_amount_count_Y_Q(tITY, quarters)

         
         elif method3=="Top Transaction":
             col1,col2=st.columns(2)
             with col1:                 
                  years=st.slider("Select the Year_TT",top_transaction["Years"].min(),top_transaction["Years"].max(),top_transaction["Years"].min())
                  tTTY=Transaction_amount_count_Y(top_transaction,years)

             col1,col2=st.columns(2)
             with col1:
                states=st.selectbox("Select The State_TT",tTTY["States"].unique())
                Top_ins_plot1(tTTY,states)
         
             col1,col2=st.columns(2)
             with col1:
                 quarters=st.slider("Select The Quarter_TT",tTTY["Quarter"].min(),tTTY["Quarter"].max(),tTTY["Quarter"].min())
                 tTYQ1=Transaction_amount_count_Y_Q(tTTY, quarters)

         
         elif method3=="Top User":
             col1,col2=st.columns(2)
             with col1:                 
                  years=st.slider("Select the Year_TT",top_user["Years"].min(),top_user["Years"].max(),top_user["Years"].min())
                  tUY=top_user_plot_1(top_user,years)

             col1,col2=st.columns(2)
             with col1:
                states=st.selectbox("Select The State_TU",tUY["States"].unique())
                top_user_plot_2(tUY,states)
         
         



elif select=="TOP CHARTS":
    
    question=st.selectbox("Select the Question",["1.Transaction amount and count of Aggregated insurance",
                                                 "2.Transaction amount and count of Map Insurance",
                                                 "3.Transaction amount and count of Top Insurance",
                                                 "4.Transaction amount and count of Aggregated Transaction",
                                                 "5.Transaction amount and count of Map Transaction",
                                                 "6.Transaction amount and count of Top Transaction",
                                                 "7.Transaction count of Aggregated User",
                                                 "8.Registered users of Map User",
                                                 "9.App opens of Map User",
                                                 "10.Registerd users of Top User",
                                                 ])
     
    if question == "1.Transaction amount and count of Aggregated insurance":

        st.subheader("TRANSACTION AMOUNT")
        TOPCHARTTA("aggregated_insurance")
        
        st.subheader("TRANSACTION COUNT")
        TOPCHARTTC("aggregated_insurance")

    elif question == "2.Transaction amount and count of Map Insurance":

        st.subheader("TRANSACTION AMOUNT")
        TOPCHARTTA("map_insurance")
        
        st.subheader("TRANSACTION COUNT")
        TOPCHARTTC("map_insurance")
    
    elif question == "3.Transaction amount and count of Top Insurance":

        st.subheader("TRANSACTION AMOUNT")
        TOPCHARTTA("top_insurance")
        
        st.subheader("TRANSACTION COUNT")
        TOPCHARTTC("top_insurance")
    
    elif question == "4.Transaction amount and count of Aggregated Transaction":

        st.subheader("TRANSACTION AMOUNT")
        TOPCHARTTA("aggregated_transaction")
        
        st.subheader("TRANSACTION COUNT")
        TOPCHARTTC("aggregated_transaction")
    
    elif question == "5.Transaction amount and count of Map Transaction":

        st.subheader("TRANSACTION AMOUNT")
        TOPCHARTTA("map_transaction")
        
        st.subheader("TRANSACTION COUNT")
        TOPCHARTTC("map_transaction")

    elif question == "6.Transaction amount and count of Top Transaction":

        st.subheader("TRANSACTION AMOUNT")
        TOPCHARTTA("top_transaction")
        
        st.subheader("TRANSACTION COUNT")
        TOPCHARTTC("top_transaction")
    
    elif question == "7.Transaction count of Aggregated User":

        st.subheader("TRANSACTION COUNT")
        TOPCHARTTC("aggregated_user")

    elif question == "8.Registered users of Map User":

        states=st.selectbox("Select the States ",map_user["States"].unique())
        st.subheader("REGISTERED USERS")
        TOPCHARTRU("map_user",states)

    elif question == "9.App opens of Map User":

        states=st.selectbox("Select the States ",map_user["States"].unique())

        st.subheader("APPOPENS")
        TOPCHARTAO("map_user",states)
        
    elif question =="10.Registerd users of Top User":


        st.subheader("REGISTERED USERS")
        TOPCHARTRUs("top_user")
