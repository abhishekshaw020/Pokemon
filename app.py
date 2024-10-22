import streamlit as st
import pandas as pd
import seaborn as sns
import numpy as np
import plotly.express as px
import os
from PIL import Image

# Load the dataset
df = pd.read_csv('pokedex.csv')
df.columns = df.columns.str.strip()
df['Type 2'].fillna('None', inplace=True)

# Streamlit Title
st.title('Pokémon World')

# Sidebar
st.sidebar.header('Options')
display_option = st.sidebar.selectbox("Choose what to display:", ['Pokémon Information', 'Pokémon Stats Visualizations', 'Pokémon Type Comparison'])

# Function to display Pokémon image along with some stats
def show_pokemon_info(index):
    pokemon = df.iloc[index]
    st.subheader(f"Name: {pokemon['Name']}")
    st.write(f"Type 1: {pokemon['Type 1']}, Type 2: {pokemon['Type 2']}")
    st.write(f"Total Stats: {pokemon['Total']}")
    st.write(f"HP: {pokemon['HP']}, Attack: {pokemon['Attack']}, Defense: {pokemon['Defense']}")
    st.write(f"SP. Atk: {pokemon['SP. Atk.']}, SP. Def: {pokemon['SP. Def']}, Speed: {pokemon['Speed']}")

    img_path = pokemon['Image']
    if os.path.exists(img_path):
        img = Image.open(img_path)
        st.image(img, caption=f"{pokemon['Name']}")
    else:
        st.write(f"Image not found for {pokemon['Name']}")

# Pokémon Stats Visualizations
def visualize_stats():
    # Bar chart of total stats for the first 10 Pokémon
    st.subheader('Total Stats of First 10 Pokémon')
    fig = px.bar(df.head(10), x='Name', y='Total', title='Total Stats of First 10 Pokémon',
                 labels={'Total': 'Total Stats'}, color='Type 1')
    st.plotly_chart(fig)

    # Scatter plot of Attack vs Defense
    st.subheader('Attack vs Defense')
    fig = px.scatter(df, x='Attack', y='Defense', color='Type 1', hover_data=['Name'], title='Attack vs Defense by Pokémon Type')
    st.plotly_chart(fig)

    # Boxplot of Speed Distribution by Type 1
    st.subheader('Speed Distribution by Type 1')
    fig = px.box(df, x='Type 1', y='Speed', title='Speed Distribution by Type 1', color='Type 1')
    st.plotly_chart(fig)

# Function to compare average stats between two Pokémon types
def compare_types(type1, type2):
    # Calculate average stats for selected types
    stats_to_compare = ['HP', 'Attack', 'Defense', 'SP. Atk.', 'SP. Def', 'Speed']
    avg_stats = df.groupby('Type 1')[stats_to_compare].mean().loc[[type1, type2]].reset_index()

    # Bar chart of average stats comparison
    fig = px.bar(avg_stats, x='Type 1', y=stats_to_compare, title=f'Average Stats Comparison: {type1} vs {type2}',
                 labels={'value': 'Average Stats', 'variable': 'Stat'}, barmode='group', height=400)
    st.plotly_chart(fig)

    # Show Pokémon names and images for selected types
    st.subheader(f"Pokémon of Type: {type1}")
    display_pokemon_images(df[df['Type 1'] == type1])

    st.subheader(f"Pokémon of Type: {type2}")
    display_pokemon_images(df[df['Type 1'] == type2])

# Function to display Pokémon names and images
def display_pokemon_images(pokemon_df):
    for index, row in pokemon_df.iterrows():
        img_path = row['Image']
        st.write(row['Name'])
        if os.path.exists(img_path):
            img = Image.open(img_path)
            st.image(img, caption=row['Name'], width=100)  # Displaying a smaller image
        else:
            st.write("Image not found.")

# Main logic
if display_option == 'Pokémon Information':
    search_term = st.sidebar.text_input("Search Pokémon by name")
    if search_term:
        search_results = df[df['Name'].str.contains(search_term, case=False)]
        if not search_results.empty:
            selected_pokemon_index = st.sidebar.selectbox("Select Pokémon", search_results.index)
            show_pokemon_info(selected_pokemon_index)
        else:
            st.write("No Pokémon found with that name.")
    else:
        pokemon_index = st.sidebar.slider('Select Pokémon Index', 0, len(df) - 1, 0)
        show_pokemon_info(pokemon_index)

elif display_option == 'Pokémon Stats Visualizations':
    visualize_stats()

elif display_option == 'Pokémon Type Comparison':
    type1 = st.sidebar.selectbox('Select First Type', df['Type 1'].unique())
    type2 = st.sidebar.selectbox('Select Second Type', df['Type 2'].unique())
    
    if type1 != type2:
        compare_types(type1, type2)
    else:
        st.warning("Please select two different types.")

# Run with `streamlit run app.py`
