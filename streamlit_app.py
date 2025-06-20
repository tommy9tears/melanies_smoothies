# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session (only in SiS)
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f"Customize Your Smoothie :cup_with_straw:") #{st.__version__}
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """)

name_on_order = st.text_input('Name on Smoothie:')
st.write("The name on the Smoothie will be: ", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
# session = get_active_session() - only in SiS, required code for SniS above
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections = 5
)
if ingredients_list:
    #st.text(ingredients_list)

    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    #st.text(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders
            values (ORDER_SEQ.nextval, DEFAULT, '"""  + name_on_order + """','""" + ingredients_string + """', DEFAULT""" +  """)"""
    
    time_to_insert = st.button('Submit Order ')
    
    #st.write(my_insert_stmt)
    #st.stop
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered ' + name_on_order + '!', icon="✅")


#New section to display smoothie nutrition information
import requests
smoothiefriit_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
#st.text(smoothiefriit_response.json())
sf_df = st.dataframe(data=smoothiefriit_response.json(), use_container_width=True)
