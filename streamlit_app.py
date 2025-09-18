# streamlit_app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# -----------------------------
# 1️⃣ Load dataset
# -----------------------------
try:
    df = pd.read_csv('metadata.csv')
    st.success("Dataset loaded successfully!")
except FileNotFoundError:
    st.error("CSV file 'metadata.csv' not found in the folder!")
    st.stop()

# -----------------------------
# 2️⃣ Check columns (optional)
# -----------------------------
st.write("Columns in dataset:", df.columns.tolist())

# -----------------------------
# 3️⃣ Create 'year' column safely
# -----------------------------
if 'publish_time' in df.columns:
    df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
    df['year'] = df['publish_time'].dt.year
else:
    st.error("Column 'publish_time' not found in CSV!")
    st.stop()

# -----------------------------
# 4️⃣ Interactive year slider
# -----------------------------
min_year = int(df['year'].min())
max_year = int(df['year'].max())
year_range = st.slider("Select year range", min_year, max_year, (min_year, max_year))

# Filter data based on selected year range
filtered_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]
st.write(f"Papers between {year_range[0]} and {year_range[1]}: {len(filtered_df)}")

# Show first 5 rows
st.subheader("Sample of filtered data")
st.dataframe(filtered_df.head())

# -----------------------------
# 5️⃣ Basic Visualization
# -----------------------------
st.subheader("Publications by Year")
year_counts = filtered_df['year'].value_counts().sort_index()
fig, ax = plt.subplots()
ax.bar(year_counts.index, year_counts.values)
ax.set_xlabel("Year")
ax.set_ylabel("Number of Publications")
ax.set_title("Publications by Year")
st.pyplot(fig)

# -----------------------------
# 6️⃣ Top journals visualization
# -----------------------------
st.subheader("Top 10 Journals by Publication Count")
if 'journal' in df.columns:
    top_journals = filtered_df['journal'].value_counts().head(10)
    fig2, ax2 = plt.subplots()
    ax2.barh(top_journals.index[::-1], top_journals.values[::-1])
    ax2.set_xlabel("Number of Papers")
    ax2.set_ylabel("Journal")
    ax2.set_title("Top 10 Journals")
    st.pyplot(fig2)
else:
    st.info("Column 'journal' not found in dataset.")

# -----------------------------
# 7️⃣ Word Cloud for titles
# -----------------------------
st.subheader("Word Cloud of Paper Titles")
if 'title' in df.columns:
    text = " ".join(str(title) for title in filtered_df['title'].dropna())
    if text.strip() != "":
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
        fig3, ax3 = plt.subplots(figsize=(10,5))
        ax3.imshow(wordcloud, interpolation='bilinear')
        ax3.axis('off')
        st.pyplot(fig3)
    else:
        st.info("No titles found for word cloud.")
else:
    st.info("Column 'title' not found in dataset.")
