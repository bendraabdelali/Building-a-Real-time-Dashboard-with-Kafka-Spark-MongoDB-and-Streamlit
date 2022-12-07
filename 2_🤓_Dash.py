import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import pymongo

st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")
# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return pymongo.MongoClient(**st.secrets["mongo"])

client = init_connection()

# Pull data from the collection.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=2)
def get_data(collection):
    db = client.Analysis
    items = db[collection].find()
    items = list(items)  
    return items

groupby_column = st.selectbox(
        'What would you like to analyse?',
        ('country', 'gender', 'Product_name'),
    )


items = get_data("CountryAmount")    
if groupby_column == "Product_name":
    items = get_data("ProductAmount")
elif  groupby_column == "gender" :  
    items = get_data("GenderAmount")
else :    
    items = get_data("CountryAmount")

# Print results.
df = pd.DataFrame(items)
df = df.drop(['_id'], axis=1)



# ---- MAINPAGE ----#

st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

# TOP KPI's
total_sales = df["total_order_amount"].sum()
left_column, right_column = st.columns(2)
with left_column:
    st.subheader("Total Sales:")
with right_column:
    st.subheader(f"{total_sales} $")

st.markdown("""---""")


# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
fileds = st.sidebar.multiselect(
    f"Select the {groupby_column}:",
    options=df[groupby_column].unique(),
    default=df[groupby_column].unique()
)

df_selection = df.query(
    f"{groupby_column} == @fileds"
)
# -- PLOT
st.subheader(f"::fireworks:: Sales by {groupby_column}   📈  ")
fig = px.bar(
        df_selection,
        x=groupby_column,
        y='total_order_amount',
        color='total_order_amount',
        color_continuous_scale=['red', 'yellow', 'green'],
        template='plotly_white',
        title=f'<b>Sales & Profit by {groupby_column}</b>'
)
        
# Pie Charts 
fig1 = px.pie(df_selection, values="total_order_amount", names=groupby_column, title=f'<b>Sales & Profit by {groupby_column}</b>')

 
left_column, right_column = st.columns(2)
left_column.plotly_chart(fig, use_container_width=True)
right_column.plotly_chart(fig1, use_container_width=True)



# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
