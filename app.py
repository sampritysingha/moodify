import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
import random


# Load dataset and model
df = pd.read_csv('data/data_moods.csv')
with open('models/mood_predictor.pkl', 'rb') as f:
    model = pickle.load(f)

# Prepare data for time-based evolution chart
df['year'] = pd.to_datetime(df['release_date'], format='mixed', errors='coerce').dt.year
df['decade'] = (df['year'] // 10) * 10
features_to_plot = ['danceability', 'energy', 'tempo', 'liveness']
agg_df = df.dropna(subset=['decade'])[features_to_plot + ['decade']]
agg_df = agg_df.groupby('decade')[features_to_plot].mean().reset_index().sort_values('decade')

# Set page config
st.set_page_config(page_title="Moodify", layout="wide")

# Gradient Background with CSS
st.markdown("""
    <style>
        body {
            background: linear-gradient(-45deg, #1e3c72, #2a5298, #1e3c72, #0f2027);
            background-size: 400% 400%;
            animation: gradientFlow 15s ease infinite;
            color: #f4f4f4;
        }
        @keyframes gradientFlow {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }
        .stButton>button {
            background-color: #5D3FD3;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 0.6em 1.2em;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #3e2c9d;
            transform: scale(1.05);
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🎵 Moodify")
st.markdown("_welcome to the website that helps you explore the emotional essence of music through mood and genre._")


# ===== Time Travel Through Music =====
with st.expander("🕰️ Time Travel Through Music"):
    st.markdown("_Watch how musical traits changed across decades._")
    long_df = pd.melt(agg_df, id_vars='decade', var_name='Feature', value_name='Value')
    fig4 = px.line(
        long_df,
        x='decade',
        y='Value',
        color='Feature',
        markers=True,
        title='🎼 Evolution of Audio Features Over Time',
        animation_frame='Feature',
        range_y=[0, max(long_df['Value']) + 20 if long_df['Feature'].eq('tempo').any() else 1],
    )
    st.plotly_chart(fig4, use_container_width=True)

# ===== Song Features & Energy Viz =====
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🔍 Explore Song Features")
    song_select = st.selectbox("Select a Song", df['name'].unique())
    song_data = df[df['name'] == song_select].iloc[0] if not df[df['name'] == song_select].empty else None

    if song_data is not None:
        features = ['danceability', 'energy', 'loudness', 'valence']
        fig = px.bar(
            x=features,
            y=[song_data[feat] for feat in features],
            title=f"Audio Features for '{song_select}'",
            labels={'x': 'Feature', 'y': 'Value'}
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data found for the selected song.")

with col2:
    with st.expander("⚡ Energy Visualization for Selected Song"):
        if song_data is not None:
            energy_val = song_data['energy']
            if energy_val < 0.3:
                bar_color = 'green'
                energy_desc = "Relax and unwind with this mellow tune."
            elif 0.3 <= energy_val < 0.7:
                bar_color = 'orange'
                energy_desc = "A balanced vibe — not too slow, not too fast."
            else:
                bar_color = 'red'
                energy_desc = "Get ready to dance with this high-energy track!"

            fig3 = px.bar(x=['Energy'], y=[energy_val], color=['Energy'],
                          color_discrete_sequence=[bar_color],
                          title=f"Energy Level of '{song_select}'")
            st.plotly_chart(fig3, use_container_width=True)
            st.write(f"**Energy Description:** {energy_desc}")
        else:
            st.info("Select a song to view energy visualization.")

# ===== Generate curated playlists based on various features =====
st.markdown("---")
st.markdown("### Generate curated playlists based on various features:")

# ===== Interactive Song Explorer =====
with st.expander("🧭 Interactive Song Explorer"):
    st.markdown("_Drag the filters to discover top tracks that match your vibe._")

    d = st.slider("Danceability", 0.0, 1.0, (0.3, 0.8))
    a = st.slider("Acousticness", 0.0, 1.0, (0.2, 0.9))
    l = st.slider("Loudness", -60.0, 0.0, (-30.0, -5.0))
    e = st.slider("Energy", 0.0, 1.0, (0.2, 0.9))
    lv = st.slider("Liveness", 0.0, 1.0, (0.1, 0.8))

    filtered_songs = df[
        (df['danceability'].between(d[0], d[1])) &
        (df['loudness'].between(l[0], l[1])) &
        (df['energy'].between(e[0], e[1])) &
        (df['liveness'].between(lv[0], lv[1]))
    ].sort_values(by='popularity', ascending=False).head(5)

    st.markdown("#### 🎧 Top 5 Matching Songs")
    st.dataframe(filtered_songs[['name', 'artist', 'album']], use_container_width=True)


# ===== Real-time Mood Slider & Suggestions =====
with st.expander("🎛️ Real-time Mood Slider & Suggestion"):
    st.markdown("_Select your current mood level and get a matching playlist!_")
    mood_slider = st.slider("How do you feel today?", 1, 10, 5)
    if mood_slider <= 3:
        st.info("You're feeling low? Here's a relaxing playlist:")
        st.dataframe(df[df['mood'] == 'Calm'][['name', 'artist', 'album']].head(10))
    elif mood_slider <= 7:
        st.info("You're in a balanced mood! Check out these upbeat tracks.")
        st.dataframe(df[df['mood'] == 'Energetic'][['name', 'artist', 'album']].head(10))
    else:
        st.info("Feeling great? Let's go wild with some high-energy beats!")
        st.dataframe(df[df['mood'] == 'Happy'][['name', 'artist', 'album']].head(10))

# ===== Filtered Songs Section =====
with st.expander("🎶 Filtered Songs"):
    st.markdown("_Filter top songs that according to your selected mood and genres_")
    
    # Filters now placed here (was in sidebar earlier)
    available_moods = df['mood'].dropna().unique()
    available_genres = df['genre'].dropna().unique()
    selected_mood = st.selectbox("Select Mood", available_moods)
    selected_genre = st.selectbox("Select Genre", available_genres)

    # Show top filtered songs
    filtered_df = df[(df['mood'] == selected_mood) & (df['genre'] == selected_genre)]
    st.dataframe(filtered_df[['name', 'artist', 'album']].head(10), use_container_width=True)

# ===== Playlist Recommendations =====
with st.expander("🎯 Playlist Recommendations for separate moods & genres"):
    rec_mood = st.selectbox("Choose Mood for Playlist", available_moods)
    rec_genre = st.selectbox("Choose Genre for Playlist", available_genres)

    if st.button("🎧 Recommend by Mood"):
        st.success(f"Top Songs for Mood: {rec_mood}")
        mood_recs = df[df['mood'] == rec_mood][['name', 'artist', 'album']].head(10)
        st.dataframe(mood_recs)

    if st.button("🎼 Recommend by Genre"):
        st.success(f"Top Songs for Genre: {rec_genre}")
        genre_recs = df[df['genre'] == rec_genre][['name', 'artist', 'album']].head(10)
        st.dataframe(genre_recs)

# Quiz heading
st.markdown("### 🎵 Which Song Matches Your Vibe?")
st.markdown("Take this fun quiz and we’ll match you with songs that reflect your mood and energy!")

# Initialize session state
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False

if "quiz_index" not in st.session_state:
    st.session_state.quiz_index = 0

if "answers" not in st.session_state:
    st.session_state.answers = {}

# Define questions
questions = [
    {
        "question": "Pick your current vibe:",
        "options": ["Chill", "Energetic", "Melancholic", "Romantic", "Uplifting", "Groovy"],
        "key": "mood"
    },
    {
        "question": "Your ideal Saturday night?",
        "options": ["Dancing", "Movie marathon", "Night drive", "Game night", "Quiet reading"],
        "key": "saturday"
    },
    {
        "question": "What kind of rhythm suits your pace?",
        "options": ["Slow and steady", "Smooth groove", "Fast & fun", "Surprising and playful"],
        "key": "rhythm"
    },
    {
        "question": "Pick your talk style:",
        "options": [
            "I talk like a podcast host",
            "I say less, feel more",
            "Balanced and clear",
            "Fast and unfiltered"
        ],
        "key": "speech"
    },
    {
        "question": "Pick your chaos level:",
        "options": [
            "Peaceful and calm",
            "Controlled energy",
            "High energy",
            "Laid-back and minimal"
        ],
        "key": "chaos"
    }
]

# Mapping dictionaries
mood_map = {
    "Chill": "calm",
    "Energetic": "energetic",
    "Melancholic": "sad",
    "Romantic": "dreamy",
    "Uplifting": "happy",
    "Groovy": "party"
}

saturday_map = {
    "Dancing": lambda df: df[df["danceability"] > 0.6],
    "Movie marathon": lambda df: df[df["valence"] < 0.5],
    "Night drive": lambda df: df[df["tempo"] > 100],
    "Game night": lambda df: df[df["energy"] > 0.5],
    "Quiet reading": lambda df: df[df["acousticness"] > 0.4]
}

rhythm_map = {
    "Slow and steady": lambda df: df[df["tempo"] < 85],
    "Smooth groove": lambda df: df[df["danceability"] > 0.6],
    "Fast & fun": lambda df: df[df["tempo"] > 120],
    "Surprising and playful": lambda df: df[df["liveness"] > 0.4]
}

speech_map = {
    "I talk like a podcast host": lambda df: df[df["speechiness"] > 0.4],
    "I say less, feel more": lambda df: df[df["speechiness"] < 0.2],
    "Balanced and clear": lambda df: df[df["speechiness"].between(0.2, 0.4)],
    "Fast and unfiltered": lambda df: df[df["liveness"] > 0.5]
}

chaos_map = {
    "Peaceful and calm": lambda df: df[(df["loudness"] < -9) & (df["energy"] < 0.4)],
    "Controlled energy": lambda df: df[(df["energy"].between(0.4, 0.7))],
    "High energy": lambda df: df[df["energy"] > 0.7],
    "Laid-back and minimal": lambda df: df[(df["acousticness"] > 0.6) & (df["energy"] < 0.5)]
}

mapping_functions = {
    "saturday": saturday_map,
    "rhythm": rhythm_map,
    "speech": speech_map,
    "chaos": chaos_map
}

# Start button
if not st.session_state.quiz_started:
    if st.button("🎯 Start Quiz"):
        st.session_state.quiz_started = True
        st.session_state.quiz_index = 0
        st.session_state.answers = {}
else:
    idx = st.session_state.quiz_index

    # Display quiz only if not done
    if idx < len(questions):
        q = questions[idx]
        st.subheader(f"{idx + 1}. {q['question']}")
        for opt in q["options"]:
            if st.button(opt, key=f"{idx}_{opt}"):
                st.session_state.answers[q["key"]] = opt
                st.session_state.quiz_index += 1
                st.rerun()  # rerun to avoid extra clicks
 # rerun to avoid extra clicks

    # When all questions are answered
    elif len(st.session_state.answers) == len(questions):
        mood_answer = st.session_state.answers["mood"]
        filtered_df = df[df["mood"].str.contains(mood_map[mood_answer], case=False, na=False)]

        for key in ["saturday", "rhythm", "speech", "chaos"]:
            answer = st.session_state.answers[key]
            if answer in mapping_functions[key]:
                filtered_df = mapping_functions[key][answer](filtered_df)

        st.markdown("### 🎧 Your Top Song Matches:")

        if filtered_df.empty:
            st.warning("No perfect match found with all filters. Showing best vibe match instead!")
            fallback_df = df[df["mood"].str.contains(mood_map[mood_answer], case=False, na=False)]
            top_songs = fallback_df.sort_values(by="popularity", ascending=False).head(3)
        else:
            top_songs = filtered_df.sort_values(by="popularity", ascending=False).head(3)

        for i, row in top_songs.iterrows():
            st.markdown(f"**🎵 {row['name']}** by *{row['artist']}*")
            st.markdown(f"🎧 Mood: {row['mood']} | Genre: {row['genre']} | Popularity: {row['popularity']}")
            st.markdown("---")

        if st.button("🔁 Retake Quiz"):
            st.session_state.quiz_started = False
            st.session_state.quiz_index = 0
            st.session_state.answers = {}

# Random Mood Song
st.markdown("### 🎶 Random Mood Match")
if st.button("🎲 Surprise Me with a Mood"):
    random_mood = random.choice(list(df['mood'].unique()))
    st.write(f"🎵 Your mood: **{random_mood}** — Here's a matching track:")
    st.dataframe(df[df['mood'] == random_mood][['name', 'artist', 'album']].sample(1))
# ===== Vibe-Based Recommendations =====
st.markdown("### 🎉 Vibe-Based Song Recommendations")
vibe = st.selectbox("Choose Your Vibe 🎧", ["Partying", "Studying", "Reflecting", "Chilling with Friends", "3AM Cries"])

def get_vibe_recommendations(vibe):
    if vibe == "Partying":
        return df[(df['danceability'] > 0.7) & (df['energy'] > 0.7) & (df['loudness'] > -5)].sort_values(by='popularity', ascending=False).head(5)
    elif vibe == "Studying":
        return df[(df['speechiness'] < 0.1) & (df['tempo'] < 100) & (df['instrumentalness'] > 0.6)].sort_values(by='popularity', ascending=False).head(5)
    elif vibe == "Reflecting":
        return df[(df['acousticness'] > 0.7) & (df['valence'] < 0.4)].sort_values(by='popularity', ascending=False).head(5)
    elif vibe == "Chilling with Friends":
        return df[(df['danceability'] > 0.5) & (df['energy'] > 0.4) & (df['valence'] > 0.5)].sort_values(by='popularity', ascending=False).head(5)
    elif vibe == "3AM Cries":
        return df[(df['valence'] < 0.3) & (df['acousticness'] > 0.6) & (df['tempo'] < 100)].sort_values(by='popularity', ascending=False).head(5)
    else:
        return pd.DataFrame()

recommendations = get_vibe_recommendations(vibe)
st.markdown(f"#### Top Songs for **{vibe}** 🫶")
st.dataframe(recommendations[['name', 'artist', 'album']], use_container_width=True)
