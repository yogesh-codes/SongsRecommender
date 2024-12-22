import streamlit as st
import pandas as pd

# Load the similarity matrix and dataset
sm: pd.DataFrame = pd.read_pickle("export_similarity_matrix.pkl")  # Your pre-saved matrix
dataset: pd.DataFrame = pd.read_csv("export_dataset.csv")  # Your original dataset with track details

st.write(sm.head(2))
st.write(dataset.head(2))
# Define recommendation function


def recommend_songs(track_index: int, similarity_matrix: pd.DataFrame, df: pd.DataFrame, top_n=5):
    if track_index not in similarity_matrix.index:
        raise Exception(f"Track index '{track_index}' not found in the dataset.")

    # Get similarity scores and sort
    similar_tracks_ids = (similarity_matrix.loc[track_index].sort_values(ascending=False).iloc[1:top_n + 1]).index

    st.write(similar_tracks_ids)

    details = df.loc[similar_tracks_ids]

    return details


def display_recommendations(details: pd.DataFrame):
    for _, row in details.iterrows():
        col1, col2 = st.columns([1, 2])  # Adjust width ratio if needed

        # Column 1: Display the image
        with col1:
            st.image(row['artwork_url'], use_container_width=True)

        # Column 2: Display the details
        with col2:
            st.write(f"**Track:** {row['track_name']}")
            st.write(f"**Artist:** {row['artist_name']}")
        st.write("---")  # Optional separator for visual clarity


def display_one(row):

    col1, col2 = st.columns([1, 2])  # Adjust width ratio if needed

    # Column 1: Display the image
    with col1:
        st.image(row['artwork_url'], use_container_width=True)

    # Column 2: Display the details
    with col2:
        st.write(f"**Track:** {row['track_name']}")
        st.write(f"**Artist:** {row['artist_name']}")
    st.write("---")  # Optional separator for visual clarity

# App UI


st.title("🎵 Music Recommendation System")
textbox_track_index = st.text_input("Enter a relative Track index:")
slider_top_n = st.slider("Number of Recommendations:", min_value=1, max_value=10, value=5)

if st.button("Recommend"):
    try:
        track_index_ = int(textbox_track_index)
        number_of_results=int(slider_top_n)
    except ValueError:
        st.error("Enter an integer for track id or slider.")
        track_index_ = None

    recommendation_details: pd.DataFrame = recommend_songs(track_index=track_index_, similarity_matrix=sm, df=dataset, top_n=number_of_results)
    # if isinstance(recommendations, str):
    #    st.error(recommendations)  # Show error if track ID not found
    # else:

    your_song_details = dataset.loc[track_index_]

    display_one(your_song_details)
    display_recommendations(recommendation_details)
    # st.write(recommendations)  # Show recommendations

