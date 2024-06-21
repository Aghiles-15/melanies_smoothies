  # Importer les packages nécessaires
import streamlit as st
from snowflake.snowpark.session import Session
from snowflake.snowpark.functions import col
import requests  # Déplacer l'instruction d'importation en haut

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
st.title(":cup_with_straw: Personnalisez votre smoothie! :cup_with_straw:")
st.write("Choisissez les fruits que vous voulez dans votre smoothie personnalisé!")

name_on_order = st.text_input("Nom sur le smoothie")
st.write("Le nom sur votre smoothie sera :", name_on_order)

# Utiliser la session active
session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON')).to_pandas()
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()
pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()

ingredients_list = st.multiselect('Choisissez les 5 meilleurs ingrédients :', my_dataframe['FRUIT_NAME'], max_selections=5)

if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutrition Information')
        fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{fruit_chosen.lower()}")
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

    st.write(ingredients_string)

    my_insert_stmt = f"INSERT INTO smoothies.public.orders (ingredients, name_on_order) VALUES ('{ingredients_string.strip()}', '{name_on_order}')"
    st.write(my_insert_stmt)

time_to_insert = st.button('Soumettre la commande')

if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Votre smoothie est commandé!', icon="✅")
