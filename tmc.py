import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from pathlib import Path

# Call set_page_config at the beginning
st.set_page_config(
    page_title="Transmen Collective",
    page_icon="🏳️‍⚧️"
)

# Inject custom CSS to hide the hamburger menu
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# Define the function to read all sheets from an Excel file
def read_all_sheets_from_excel(path: str) -> dict:
    # Read the Excel file
    xls = pd.ExcelFile(path)
    # Create a dictionary of dataframes, one for each sheet in the Excel file
    df_dict = {sheet_name: xls.parse(sheet_name) for sheet_name in xls.sheet_names}
    return df_dict

# Load data with caching
@st.cache_data
def load_data():
    excel_file = "dr_details.xlsx"
    df = pd.read_excel(excel_file)
    # Clean and convert 'Rating' column to numeric
    df['Rating'] = pd.to_numeric(df['Rating'].str.extract('(\d+\.\d+)')[0], errors='coerce')
    return df

# Option menu for navigation
selected = option_menu(
    menu_title=None,
    options=["Home", "Projects", "Doctor Details", "Contact Us"],
    icons=["house", "book", "bi bi-hospital", "bi bi-chat-heart-fill"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

if selected == "Home":
    st.title("Transmen Collective")
    st.write(
        "Welcome to Transmen Collective! We are a group dedicated to addressing transmasculine issues. "
        "Our mission is to create a supportive and inclusive community while raising awareness and advocating for transmasculine individuals."
    )

elif selected == "Projects":
    st.title(f"{selected}")
    st.write("This is the Projects page content.")

elif selected == "Doctor Details":
    st.title(f"{selected}")
    st.write("Explore information about different doctors and treatments.")

    # Read all sheets from the Excel file
    dataframes = read_all_sheets_from_excel('dr_details.xlsx')

    # Print the names of the dataframes (sheets)
    print('Dataframes in this file:', ', '.join(dataframes.keys()))

    # Add filter widgets in the same line using st.columns
    city_filter, treatment_filter = st.columns(2)
    with city_filter:
        selected_city = st.multiselect("Select City", dataframes['Details']['City'].unique())
    with treatment_filter:
        selected_treatment = st.multiselect("Select Treatment", dataframes['Details']['Specilized'].unique())

    # Apply filters
    filtered_data = dataframes['Details']
    if selected_city:
        filtered_data = filtered_data[filtered_data['City'].isin(selected_city)]
    if selected_treatment:
        filtered_data = filtered_data[filtered_data['Specilized'].isin(selected_treatment)]

    # Display bar chart for ratings using Plotly
    fig_ratings = px.bar(
        filtered_data,
        x='Doctor Name',
        y='Rating',
        color='Specilized',
        title='Doctor Ratings by Specialization',
        labels={'Rating': 'Average Rating', 'Doctor Name': 'Doctor Name'},
        template='plotly',
        height=600,  # Set the height of the chart
    )

    # Set the Y-axis range to start from 0 to 5
    fig_ratings.update_layout(yaxis_range=[0, 5])

    # Show the bar chart
    st.plotly_chart(fig_ratings)

    # Display detailed information for each doctor as a table
    st.subheader("Detailed Doctor Information")
    with st.expander("Data Preview"):
        detailed_info_df = pd.DataFrame(columns=['Doctor Name', 'Specilized', 'Rating', 'City', 'Cost'])
        for _, row in filtered_data.iterrows():
            # Convert the row (Pandas Series) to a DataFrame and then append it
            row_df = pd.DataFrame([row])
            detailed_info_df = pd.concat([detailed_info_df, row_df], ignore_index=True)

        # Display the DataFrame as a table
        st.dataframe(detailed_info_df)

elif selected == "Contact Us":
    st.title(f"{selected}")
    st.write("You can contact us through the following channels:")

    # Email with emoji and customized icon
    st.write('<i class="far fa-envelope"></i> [transmencollective@gmail.com](mailto:transmencollective@gmail.com)', unsafe_allow_html=True, use_container_width=True)

    # Instagram with icon and customized icon
    st.write('<i class="fab fa-instagram"></i> [transmencollective](https://www.instagram.com/transmencollective/)', unsafe_allow_html=True, use_container_width=True)

    # YouTube with icon and customized icon
    st.write('<i class="fab fa-youtube"></i> [transmencollective2059](https://www.youtube.com/@transmencollective2059)', unsafe_allow_html=True, use_container_width=True)
    