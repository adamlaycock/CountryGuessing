import streamlit as st
import pandas as pd
import plotly.express as px
import levenshtein as levenshtein

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

progress = len(st.session_state.guesses) / 55
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
        # new code -> uses Levenshtein distance to find the closest match to allow for a typo in the guess
        best_match = None
        min_distance = float('inf')
        for country in countries['name_lower']:
            dist = levenshtein.levenshtein_distance(guess_input, country)
            if dist < min_distance:
                min_distance = dist
                best_match = country

        # If the best match has a Levenshtein distance below a threshold, accept it
        threshold = 2  #Currently set to 2 -> 2 edits of a country name is still accepted -> can be changed to be more or less strict
        if min_distance <= threshold:
            if best_match in st.session_state.guesses:
                st.warning(f'Already guessed "{best_match.title()}".')
            else:
                st.session_state.guesses.append(best_match)
                st.rerun()
        else:
            st.error(f'"{guess_input}" not found in the database. Did you mean "{best_match.title()}"?')