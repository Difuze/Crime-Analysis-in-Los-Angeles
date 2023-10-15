import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from folium.plugins import HeatMap
from folium.plugins import HeatMapWithTime
from streamlit_folium import st_folium


st.set_page_config(layout="wide",page_title= "Crime Analysis")
df = pd.read_csv("los_angele.csv")


Underage = df[df["Age_Grp"] == "Underage"]
Underage_c = Underage["Crm Cd Desc"].value_counts().sort_values(ascending=False).head(5)

Adult = df[df["Age_Grp"] == "Adult"]
Adult_c = Adult["Crm Cd Desc"].value_counts().sort_values(ascending=False).head(5)

Senior = df[df["Age_Grp"] == "Senior"]
Senior_c = Senior["Crm Cd Desc"].value_counts().sort_values(ascending=False).head(5)




Underage_F = Underage[Underage["Vict Sex"] == "F"]["Crm Cd Desc"].value_counts().head(5)
Underage_M = Underage[Underage["Vict Sex"] == "M"]["Crm Cd Desc"].value_counts().head(5)

Senior_F = Senior[Senior["Vict Sex"] == "F"]["Crm Cd Desc"].value_counts().head(5)
Senior_M = Senior[Senior["Vict Sex"] == "M"]["Crm Cd Desc"].value_counts().head(5)

Adult_F = Adult[Adult["Vict Sex"] == "F"]["Crm Cd Desc"].value_counts().head(5)
Adult_M = Adult[Adult["Vict Sex"] == "M"]["Crm Cd Desc"].value_counts().head(5)

def load_overall():

    st.title("Overall Analysis")

    col1,col2 = st.columns(2)
    col3,col4 = st.columns(2)
    col5,col6 = st.columns(2)


    with col1:
        st.subheader("Number of Crime Happend with sex")
        temp_df1 = df[df['Vict Sex'] != "H"]
        sex_count = temp_df1["Vict Sex"].value_counts()
        fig,ax = plt.subplots(figsize = (6,6))
        ax.bar(sex_count.index,sex_count.values)
        ax.set_xlabel("Sex")
        ax.set_ylabel("Number of Crimes")
        st.pyplot(fig)

    with col2:
        st.subheader("Crime on Various Ethnicity")
        descent_count = df['Vict Descent'].value_counts().head(5)
        fig1, ax1 = plt.subplots(figsize=(6, 6))
        ax1.plot(descent_count.index , descent_count.values , color = "red",marker = "o", linewidth=2, markersize = 12)
        ax1.set_xlabel("Ethnicity")
        ax1.set_ylabel("Number of Crimes")
        st.pyplot(fig1)

    with col3:
        st.subheader("Most common crime types ")
        x = df["Crm Cd Desc"].value_counts().head()
        fig2,ax2 = plt.subplots(figsize = (6,6))
        sns.barplot(data=df, x=x.index, y=x.values , ax = ax2)
        st.pyplot(fig2)

    with col4:
        st.subheader("Number of Crimes with time")
        time_c = df["Time_grp"].value_counts()
        fig3, ax3 = plt.subplots(figsize=(6, 6))
        ax3.pie(time_c, autopct="%.1f%%", labels=time_c.index)
        st.pyplot(fig3)

    with col5:
        st.subheader("Top area where crime has occured most")
        top_area = df["AREA NAME"].value_counts().head().reset_index().rename(
            columns={'index': 'city', "AREA NAME": "No. of Crimes"})
        st.dataframe(top_area,width=450, height=250)


def load_age_crime():

    st.title('Crime Statistics by Age Group')

    st.subheader("Total Number of Crime Ocuured wiht Underage : " + str(Underage_c.sum()))
    st.subheader("Total Number of Crime Ocuured wiht Adult : " + str(Adult_c.sum()))
    st.subheader("Total Number of Crime Ocuured wiht Senior : " + str(Senior_c.sum()))
    st.subheader("----------------------------------------------------------------------------------------------------------------")

    col3,col4,col5 = st.columns(3)
    col5,col6 = st.columns(2)



    with col3:
        st.subheader("Types of Crime with Underage grp")
        fig4, ax4 = plt.subplots(figsize=(6, 6))
        ax4.bar(Underage_c.index, Underage_c.values, color="red")
        ax4.set_title("Underage vs Crime Type")
        ax4.set_ylabel("Age Count")
        ax4.tick_params(axis='x', rotation=45)
        st.pyplot(fig4)


    with col4:
        st.subheader("Types of Crime with Adult grp")
        fig5, ax5 = plt.subplots(figsize=(6, 6))
        ax5.bar(Adult_c.index, Adult_c.values, color="green")
        ax5.set_title("Adult vs Crime Type")
        ax5.set_ylabel("Age Count")
        ax5.tick_params(axis='x', rotation=45)
        st.pyplot(fig5)

    with col5:
        st.subheader("Types of Crime with Senior grp")
        fig6, ax6 = plt.subplots(figsize=(6, 6))
        ax6.bar(Senior_c.index, Senior_c.values, color="yellow")
        ax6.set_title("Adult vs Crime Type")
        ax6.set_ylabel("Age Count")
        ax6.tick_params(axis='x', rotation=45)
        st.pyplot(fig6)


        # Function to plot and display in Streamlit

    def plot_crime_vs_vict_sex(axes, x, y, title):
        axes.bar(x, y)
        axes.set_xticklabels(x, rotation='vertical')
        axes.set_title(title)

    # Streamlit App
    st.title("Crime Type vs Vict Sex")


    # Plotting in Streamlit
    fig, axs = plt.subplots(3, 2, figsize=(12, 25))

    # Define the data and labels in a structured way
    data = [
        (Adult_F.index, Adult_F.values, "Adult Female vs Crime Type"),
        (Adult_M.index, Adult_M.values, "Adult Male vs Crime Type"),
        (Senior_F.index, Senior_F.values, "Senior Female vs Crime Type"),
        (Senior_M.index, Senior_M.values, "Senior Male vs Crime Type"),
        (Underage_F.index, Underage_F.values, "Underage Female vs Crime Type"),
        (Underage_M.index, Underage_M.values, "Underage Male vs Crime Type")
    ]


    for i, (x, y, title) in enumerate(data):
        plot_crime_vs_vict_sex(axs[i // 2, i % 2], x, y, title)
    st.pyplot(fig)

def load_monthly_crimes():
    pass



option = st.sidebar.selectbox("Select One",["Overall","Age and Crime type","Monthly Crimes","Los Angeles Map"])

if option == "Overall":
    btn1 = st.sidebar.button("Overall Details")
    if btn1:
        load_overall()

if option == "Age and Crime type":
    btn2 = st.sidebar.button("Age and Crimes")
    if btn2:
        load_age_crime()

if option == "Monthly Crimes":
    user_input_year = st.text_input("Enter the year (in YYYY format) for which you want to display the HeatMap:")
    user_input_month = st.text_input("Enter the month (in MM format) for which you want to display the HeatMap:")

    st.subheader("If You want monthly wise area crimes than enter tha name of area here : ")
    user_input_area = st.text_input("Enter the name of Area in los Angeles: ")


    if user_input_year and user_input_month:
        try:
            selected_year = int(user_input_year)
            selected_month = int(user_input_month)
        except ValueError:
            st.error("Invalid input format. Please enter valid integers for year and month.")
            st.stop()
    else:
        st.warning("Please enter values for both year and month.")
        st.stop()

    # Convert 'DATE OCC' to datetime
    df['DATE OCC'] = pd.to_datetime(df['DATE OCC'])

    # Filter data based on user input
    selected_data = df[
        (df['DATE OCC'].dt.year == selected_year) &
        (df['DATE OCC'].dt.month == selected_month)
        ]


    # Display HeatMap
    if not selected_data.empty:
        st.subheader(f"Crimes of year {selected_year} and month {selected_month}")
        heatmap_data = selected_data["Age_Grp"].value_counts().reset_index()
        st.bar_chart(heatmap_data.set_index('index'))
    else:
        st.warning("No data available for the selected year and month.")


    # Filter data based on user input
    selected_data = df[
        (df['DATE OCC'].dt.year == selected_year) &
        (df['DATE OCC'].dt.month == selected_month) &
        (df["AREA NAME"] == user_input_area)
        ]

    if not selected_data.empty:
        crime_area_c = selected_data["AREA NAME"].value_counts()
        st.subheader(f"Total number of Cimes in {user_input_area} in year of {user_input_year} and month {user_input_month} :  " + str(crime_area_c))
        st.subheader("------------------------------------------------------------------------------------------------------")
        daa = selected_data["Time_grp"].value_counts().reset_index().rename({"index":"Time","Time_grp":"Crime Counts"})
        st.subheader(f"Number of Crimes Ocuured on the basis of time in : {user_input_area} ")
        st.dataframe(daa , width=450, height=250)
    else:
        st.warning("No data available for the selected year and month.")



if option == "Los Angeles Map":
    st.title("HeatMap for Crime Data in Los Angeles")

    # Create a base map centered around Los Angeles
    la_map = folium.Map(location=[34.0522, -118.2437], zoom_start=12)

    # Add a HeatMap layer
    heat_data = [[point['LAT'], point['LON']] for index, point in df.iterrows()]
    HeatMap(heat_data).add_to(la_map)

    # Display the map in Streamlit
    st.markdown(f"### HeatMap for Crime Data in Los Angeles")
    st_folium(la_map, width=1000 )

    st.subheader("-------------------------------------------------------------------------------------------")

    st.subheader("Check monhly wise los angeles Crime Heat Map")

    user_input_year = st.number_input("Enter the year (in YYYY format) for which you want to display the HeatMap: ")
    user_input_month = st.number_input("Enter the month (in MM format) for which you want to display the HeatMap: ")


    df['DATE OCC'] = pd.to_datetime(df['DATE OCC'])
    selected_data = df[
        (df['DATE OCC'].dt.year == selected_year) &
        (df['DATE OCC'].dt.month == selected_month)
        ]

    la_map = folium.Map(location=[34.0522, -118.2437], zoom_start=12)

    heat_data = [[point['LAT'], point['LON']] for _, point in selected_data.iterrows()]

    HeatMapWithTime([heat_data], auto_play=True).add_to(la_map)

    st_folium(la_map, width=1000 )















