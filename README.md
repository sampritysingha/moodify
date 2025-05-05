# 🎵 MOODIFY - Predicting Genre and Mood from Audio Features

Welcome to **Moodify**, a music discovery app that helps you explore songs based on mood, energy, and genre using interactive visualizations and machine learning. Whether you're chilling, partying, or just vibing, Moodify curates playlists and insights that match your emotions.

---

## 🌟 Features

### 🎛️ Real-time Mood Detection and Recommendations
- Interactive mood slider that dynamically suggests playlists.
- Real-time matching of songs with `Calm`, `Energetic`, or `Happy` moods.

### 🧭 Interactive Song Explorer
- Use sliders to filter songs by:
  - `Danceability`
  - `Acousticness`
  - `Loudness`
  - `Energy`
  - `Liveness`
- View the **Top 5 Matching Songs** based on selected audio features.

### 🎼 Time Travel Through Music
- Animated visualization of how key audio features evolved across decades.
- Insights into trends for:
  - `Danceability`
  - `Tempo`
  - `Energy`
  - `Liveness`

### 🔍 Song Feature Visualizer
- Select a song and view bar charts of its:
  - `Danceability`
  - `Energy`
  - `Loudness`
  - `Valence`

### ⚡ Energy Level Interpretation
- Color-coded bar chart and description based on the selected song's energy.

### 🎯 Playlist Recommendations
- Generate playlists by:
  - **Mood**
  - **Genre**
- Dual dropdowns for choosing preferred combinations.

### 🎶 Filtered Songs Section
- Filter and display top songs based on **selected mood and genre**.

### 🎵 Vibe Matching Quiz
- Multi-step quiz that asks about:
  - Mood
  - Weekend habits
  - Rhythm preference
  - Speech style
  - Chaos level
- Recommends songs that match the user's vibe by filtering dataset with custom mappings.

### 🔀 Random Mood Song Generator 
- Suggests a random song from a specific mood category (e.g., Sad, Party, Chill, etc.).

---

## 🧠 How It Works

- **Data:** Uses a curated dataset `data/data_moods.csv` containing audio features, mood, and genre info.
- **ML Model:** A pre-trained mood classification model `mood_predictor.pkl` is used for mood inference.
- **Frameworks & Libraries:**
  - `Streamlit` for UI
  - `Plotly` for visualizations
  - `Pandas` for data manipulation
  - `Pickle` for loading ML model

---

## Installation
1. Clone the repository: `git clone https://github.com/sampritysingha/moodify.git`
2. Install the required dependencies:  
   `pip install -r requirements.txt`

## Usage
Run the Streamlit app:  
`streamlit run app.py`

## License
This project is licensed under the MIT License.

---

## 📈 Future Improvements
- Integrate Spotify API for live song search.An example has been added for the song "shape of you" by ed sheeran.
- Add emotion recognition from lyrics or voice.
- Collaborative filtering for better recommendations.
- Check the notebook named "Mood_Analysis" for the complete IDE of the dataset used along analysis and visualisations of the different audio features. Spotify API "spotipy" use case also included for future integrations.

---

## 👨‍💻 Author

**Samprity Singha**  
Data Science & ML Enthusiast  
[GitHub Profile](https://github.com/sampritysingha) | [LinkedIn](https://linkedin.com/in/sampritysingha29)  

