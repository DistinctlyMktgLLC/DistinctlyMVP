# Streamlit App: Interactive Visualization and Storytelling
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import plotly.express as px
import plotly.graph_objects as go
import json
from fpdf import FPDF
import os
st.write("Files in data directory:", os.listdir('data'))



# 1. Load the Consolidated Data and Pivots
# ------------------------------------
@st.cache_data
def load_data():
    main_data = pd.read_csv('/workspaces/Models/data/People_Data_wave1.csv')
    return main_data

@st.cache_data
def load_pivots():
    income_pivot = pd.read_csv('/workspaces/Models/data/pivots/income_pivot.csv')
    family_influence_pivot = pd.read_csv('/workspaces/Models/data/pivots/family_influence_pivot.csv')
    temporal_pivot = pd.read_csv('/workspaces/Models/data/pivots/temporal_pivot.csv')
    behavioral_pivot = pd.read_csv('/workspaces/Models/data/pivots/behavioral_insights_pivot.csv')
    geographical_pivot = pd.read_csv('/workspaces/Models/data/pivots/geographical_pivot.csv')
    segment_influence_pivot = pd.read_csv('/workspaces/Models/data/pivots/segment_influence_pivot.csv')
    return income_pivot, family_influence_pivot, temporal_pivot, behavioral_pivot, geographical_pivot, segment_influence_pivot

main_data = load_data()
income_pivot, family_influence_pivot, temporal_pivot, behavioral_pivot, geographical_pivot, segment_influence_pivot = load_pivots()

# Load Query Database
with open('config/query.db.json') as f:
    query_db = json.load(f)

# 2. Create the Folium Map
# --------------------------
st.title('Exploring Respondent Clusters on the Map')

# Folium Map Initialization
map_center = [main_data['Latitude'].mean(), main_data['Longitude'].mean()]
folium_map = folium.Map(location=map_center, zoom_start=5)

# Add Markers to the Map
marker_cluster = folium.plugins.MarkerCluster().add_to(folium_map)

for idx, row in main_data.iterrows():
    popup_content = f"""
        <b>{row['Kind of Person']}</b><br>
        Race: {row['Race']}<br>
        Income Level: {row['Income Level']}<br>
        Decision Style: {row['Are gut feelings your go-to when making a big decision']}<br>
        <i>{row['Distinctly Segment Name']}</i>
    """
    folium.Marker(location=[row['Latitude'], row['Longitude']],
                  popup=popup_content).add_to(marker_cluster)

# Display Map
folium_static(folium_map)

# 3. Create Sunburst Chart for Hierarchical Segmentation
# -------------------------------------------------------
st.title('Segment Hierarchy Visualization')

# Creating Sunburst Chart with Plotly
fig_sunburst = px.sunburst(
    income_pivot,
    path=['Income Level', 'Are gut feelings your go-to when making a big decision'],
    values='Count',
    title='Income Levels and Decision-Making Segmentation'
)

# Display Sunburst Chart
st.plotly_chart(fig_sunburst, use_container_width=True)

# 4. Create Sankey Diagram for Flow Relationships
# ------------------------------------------------
st.title('Behavioral Flow Analysis')

# Creating Sankey Diagram with Plotly Graph Objects
group_labels = list(family_influence_pivot['How much do your familys opinions weigh in on your decisions'].unique()) + list(family_influence_pivot['Are gut feelings your go-to when making a big decision'].unique())

source_indices = family_influence_pivot['How much do your familys opinions weigh in on your decisions'].apply(lambda x: group_labels.index(x))
target_indices = family_influence_pivot['Are gut feelings your go-to when making a big decision'].apply(lambda x: group_labels.index(x))

fig_sankey = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=group_labels
    ),
    link=dict(
        source=source_indices,
        target=target_indices,
        value=family_influence_pivot['Count']
    )
)])

fig_sankey.update_layout(title_text='Flow of Family Influence and Decision-Making', font_size=10)

# Display Sankey Diagram
st.plotly_chart(fig_sankey, use_container_width=True)

# 5. Tooltip Story Integration (FPDF PDF Generator)
# -------------------------------------------------
st.sidebar.title('Generate Report')
selected_person = st.sidebar.selectbox('Select a Respondent for a Story:', main_data['Kind of Person'].unique())

if st.sidebar.button('Tell Me a Story'):
    # Generate a personalized PDF using FPDF
    story_data = main_data[main_data['Kind of Person'] == selected_person].iloc[0]
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Personalized Story Report", ln=True, align='C')
    pdf.ln(10)
    pdf.multi_cell(0, 10, txt=f"Name: {story_data['Kind of Person']}\nRace: {story_data['Race']}\nIncome Level: {story_data['Income Level']}\nDecision Style: {story_data['Are gut feelings your go-to when making a big decision']}\nStory Narrative: {story_data['Distinctly Segment Name']}")

    # Save and Offer Download
    pdf.output(f"{selected_person}_story_report.pdf")
    with open(f"{selected_person}_story_report.pdf", "rb") as pdf_file:
        st.sidebar.download_button('Download Story Report', pdf_file, file_name=f"{selected_person}_story_report.pdf")

# 6. Query Database Implementation for Seamless User Experience
# --------------------------------------------------------------
st.title('Ask a Question')
question = st.text_input('Ask about behaviors, segments, or regions (e.g., "Who prefers delayed gratification in Chicago?")')

if question:
    # Map user query to pre-defined pivots in query DB
    response = next((item['description'] for item in query_db['queries'] if question.lower() in item['question'].lower()), "No matching data found.")
    st.write(response)

# This script is an architectural blueprint to get started with the MVP for beta users, considering econometric factors in all derived insights.
