

  # Importer les packages nécessaires
import streamlit as st
import pandas as pd  # Ajout de l'importation de pandas
from snowflake.snowpark.session import Session
from snowflake.snowpark.functions import col
import requests

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
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON')).to_pandas()

# Afficher le DataFrame Pandas dans l'application Streamlit
st.dataframe(my_dataframe)

ingredients_list = st.multiselect('Choisissez les 5 meilleurs ingrédients :', my_dataframe['FRUIT_NAME'], max_selections=5)

if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
      
        search_on = my_dataframe.loc[my_dataframe['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen, ' is ', search_on, '.')
      
        st.subheader(fruit_chosen + ' Nutrition Information')
        fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{fruit_chosen.lower()}")
        if fruityvice_response.status_code == 200:
            fv_df = pd.json_normalize(fruityvice_response.json())
            st.dataframe(fv_df)
        else:
            st.write("Information nutritionnelle non disponible pour ", fruit_chosen)
    
    st.write(ingredients_string)

    my_insert_stmt = f"INSERT INTO smoothies.public.orders (ingredients, name_on_order) VALUES ('{ingredients_string.strip()}', '{name_on_order}')"
    st.write(my_insert_stmt)

time_to_insert = st.button('Soumettre la commande')

if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Votre smoothie est commandé!', icon="✅")
