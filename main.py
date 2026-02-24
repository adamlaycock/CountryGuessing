import streamlit as st
import pandas as pd
import plotly.express as px

countries = pd.read_csv('data/countries.csv')
countries['name_lower'] = countries['name'].str.lower()

if 'guesses' not in st.session_state:
    st.session_state.guesses = []

st.title('Country Game')

countries['guessed'] = countries['name_lower'].isin(st.session_state.guesses)

fig = px.choropleth(
    countries,
    locations='ISO-3',
    locationmode='ISO-3',
    scope='africa',
    hover_name='name',
    color='guessed',
    color_discrete_map={
        True: "#3D98E7",
        False: "#E5ECF6"
    },
    height=500
)

fig.update_geos(
    showcountries=True,
    countrycolor="black"
)

fig.update_layout(
    showlegend=False,
    dragmode=False,
    margin=dict(l=0, r=0, t=0, b=0)
)

st.plotly_chart(
    fig,
    use_container_width=True,
    config={'displayModeBar': False}
)

progress = len(st.session_state.guesses) / 54
st.progress(progress, text='Percentage Completion')

with st.form('guess_form', clear_on_submit=True):
    guess_input = st.text_input('Enter country:').lower().strip()
    submit_button = st.form_submit_button("Submit Guess")

if submit_button and guess_input:
    if guess_input in countries['name_lower'].values:
        if guess_input in st.session_state.guesses:
            st.warning(f'Already guessed "{guess_input.title()}".')
        else:
            st.session_state.guesses.append(guess_input)
            st.rerun()
    else:
        st.error(f'"{guess_input}" not found in the database.')