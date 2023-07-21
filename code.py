import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="River Water Quality",
                   page_icon="💧",
                   layout="wide")

st.title("QUALITAS AIR SUNGAI CODE")
st.subheader("Visualisasi data yang ditampilkan berdasarkan titik sample yang diambil di Kota Jogja")

# Load dataset from csv
df = pd.read_csv("data.csv")

# Rename the 'Latitude' column to 'LAT' or 'latitude'
df.rename(columns={'Latitude': 'LAT'}, inplace=True)  # Rename to 'LAT'
# df.rename(columns={'Latitude': 'latitude'}, inplace=True)  # Rename to 'latitude'

def filter_data(df, years, places, parameters):
    filtered_data = df[(df['Tahun'].isin(years)) & (df['Nama Lokasi'].isin(places)) & (df['Parameter'].isin(parameters))]
    return filtered_data

# Function to plot average concentration for a given dataset
def plot_avg_concentration(filter_data, years, places, parameters):
    for parameter in parameters:
        params = filter_data[filter_data['Parameter'] == parameter]
        # Calculate the average concentration for each month
        avg_concentration_by_month = params.groupby('Bulan')['Konsentrasi'].mean().reset_index()

        # Create a plot using seaborn
        plt.figure(figsize=(10, 6))

        sns.barplot(x='Bulan', y='Konsentrasi', data=avg_concentration_by_month)
        plt.title(f'Average Concentration for Parameter: {parameter}\n At {", ".join(places)} Year {", ".join(str(year) for year in years)}\n')
        plt.xlabel('Month')
        plt.ylabel('Average Concentration')
        plt.xticks(rotation=45)

        st.pyplot(plt)  # Display the plot using Streamlit

# Streamlit app
def main():
    st.sidebar.title('Pilih Tahun, Lokasi dan Parameter untuk Menampilkan Hasil Visualisi')

    # Filter unique values of 'Place', 'Year', and 'Parameter'
    unique_years = df['Tahun'].unique()
    unique_places = df['Nama Lokasi'].unique()
    unique_parameters = df['Parameter'].unique()

    # Multiselect to choose the 'Year', 'Place', and 'Parameter'
    selected_years = st.sidebar.multiselect('Pilih Tahun', unique_years)
    selected_places = st.sidebar.multiselect('Pilih Lokasi', unique_places)
    selected_parameters = st.sidebar.multiselect('Pilih Parameter', unique_parameters)

    # Filter the data based on selected 'Place', 'Year', and 'Parameter'
    filtered_data = filter_data(df, selected_years, selected_places, selected_parameters)

    # Display the plot for the filtered data
    if not filtered_data.empty:  # Check if filtered_data is not empty
        plot_avg_concentration(filtered_data, selected_years, selected_places, selected_parameters)
    else:
        st.write("No data available for the selected filters.")

    # Display the map with 'Latitude' and 'Longitude'
    st.map(filtered_data, use_container_width=True)

    # Display scatter plot on the map using 'Latitude' and 'Longitude'
    st.subheader("Map with Scatter Plot")
    st.map(filtered_data, use_container_width=True, layer="scatter", color="red")

if __name__ == '__main__':
    main()
