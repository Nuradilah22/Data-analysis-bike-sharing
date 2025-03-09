import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# SETUP DASHBOARD 
st.title("🚴 Dashboard Bike Sharing")
st.markdown("Analyzing bike rental trends by date and hour.")

# LOAD DATA 
@st.cache_data
def load_data():
    day_df = pd.read_csv("day.csv")  
    hour_df = pd.read_csv("hour.csv")  
    
    # Convert dteday to datetime
    day_df["dteday"] = pd.to_datetime(day_df["dteday"])
    hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])
    
    return day_df, hour_df

day_df, hour_df = load_data()

# Dataset selection
dataset_option = st.radio("Select Dataset:", ["Daily (day.csv)", "Hourly (hour.csv)"])

# Data selection based on dataset option
if dataset_option == "Daily (day.csv)":
    df = day_df
    st.subheader("📅 Daily Bike Rental Analysis")
else:
    df = hour_df
    st.subheader("🕒 Hourly Bike Rental Analysis")

# Visualization selection
option = st.selectbox("📊 Select Visualization:", ["Rental Trend", "Rental Distribution"])

# SELECT DATE FROM DROPDOWN 
st.sidebar.header("📅 Select Date")
available_dates = day_df["dteday"].dt.strftime("%Y-%m-%d").unique()
selected_date = st.sidebar.selectbox("Select date:", available_dates)

# FILTER DAILY & HOURLY DATA
filtered_day_df = day_df[day_df["dteday"] == pd.to_datetime(selected_date)]
filtered_hour_df = hour_df[hour_df["dteday"] == pd.to_datetime(selected_date)]

# KEY STATISTICS
total_rentals = filtered_day_df["cnt"].sum()
avg_rentals = filtered_day_df["cnt"].mean()
peak_hour = filtered_hour_df.loc[filtered_hour_df["cnt"].idxmax(), "hr"] if not filtered_hour_df.empty else None

# DISPLAY STATISTICS
st.markdown("### 📈 Bike Rental Statistics")
col1, col2, col3 = st.columns(3)
col1.metric("🔹 Total Rentals", f"{total_rentals:,} bikes")
col2.metric("📊 Daily Average", f"{avg_rentals:.0f} bikes")
col3.metric("🚀 Busiest Hour", f"{peak_hour}:00" if peak_hour is not None else "N/A")


# VISUALIZE HOURLY RENTALS
st.markdown("### 🕒 Hourly Bike Rental Trend")
if not filtered_hour_df.empty:
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(x=filtered_hour_df["hr"], y=filtered_hour_df["cnt"], marker="o", color="tab:red", ax=ax)
    ax.set_xticks(range(0, 24))
    ax.set_xlabel("Hour")
    ax.set_ylabel("Rental Count")
    ax.set_title(f"Bike Rental Trend on {selected_date}")
    ax.grid()
    st.pyplot(fig)
else:
    st.warning("⚠ No rental data available for this date.")
    
# VISUALISASI RENTAL DISTRIBUTION
if option == "Rental Distribution":
    st.markdown("### 📊 Bike Rental Distribution")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(day_df["cnt"], bins=30, kde=True, color="tab:green", ax=ax)
    ax.set_xlabel("Rental Count")
    ax.set_ylabel("Frequency")
    ax.set_title("Daily Bike Rental Distribution")
    st.pyplot(fig)

    
# VISUALIZE DAILY RENTALS
st.markdown("### 📈 Daily Bike Rental Trend")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(day_df["dteday"], day_df["cnt"], marker="o", linestyle="-", color="tab:blue")
ax.set_xlabel("Date")
ax.set_ylabel("Rental Count")
ax.set_title("Bike Rental Tren on")
ax.grid()
st.pyplot(fig)

    
# Workday vs Holiday Bike Rental Comparison
st.markdown("### 🔄 Comparing Bike Rentals: Workdays vs Holidays")

# Separate workday and holiday data
workday_rentals = hour_df[hour_df["workingday"] == 1].groupby("hr")["cnt"].mean()
holiday_rentals = hour_df[hour_df["workingday"] == 0].groupby("hr")["cnt"].mean()

# Visualize comparison
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x=workday_rentals.index, y=workday_rentals.values, marker="o", label="Workdays", ax=ax, color="tab:blue")
sns.lineplot(x=holiday_rentals.index, y=holiday_rentals.values, marker="o", label="Holidays", ax=ax, color="tab:orange")

# Customize plot
ax.set_title("Bike Rental Comparison: Workdays vs Holidays")
ax.set_xlabel("Hour of the Day")
ax.set_ylabel("Average Rentals")
ax.legend()
ax.grid()

# Display plot

st.pyplot(fig)


# DISPLAY DATA 
st.markdown("### 📝 Daily Bike Rental Data")
st.dataframe(filtered_day_df)
st.markdown("### 📝 Hourly Bike Rental Data")
st.dataframe(filtered_hour_df)
