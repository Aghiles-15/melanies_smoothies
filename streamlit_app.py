# Importer les packages nécessaires
import streamlit as st
from snowflake.snowpark.session import Session
from snowflake.snowpark.functions import col

# Définir la fonction pour obtenir une session active
def get_active_session():
    connection_parameters = {
        "account": "BAMQRAZ-AY21624",
        "user": "AGHIL",
        "password": "123Azerty123**",
        "role": "SYSADMIN",
        "warehouse": "COMPUTE_WH",
        "database": "SMOOTHIES",
        "schema": "PUBLIC"
    }
	

	
	
    session = Session.builder.configs(connection_parameters).create()
    return session

# Écrire directement dans l'application
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input("Name on Smoothie")
st.write("The name in your smoothie will be:", name_on_order)

# Utiliser la session active
session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')).to_pandas()
st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect('Choose the top 5 ingredients:', my_dataframe['FRUIT_NAME'], max_selections=5)

if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)
    st.write(ingredients_string)

    my_insert_stmt = f"INSERT INTO smoothies.public.orders (ingredients, name_on_order) VALUES ('{ingredients_string}', '{name_on_order}')"
    st.write(my_insert_stmt)

time_to_insert = st.button('Submit Order')

if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#st.text(fruityvice_response.json())
fv_df = st.dataframe(data=fruityvice_response.jason(),use_container_width=true)
