import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle
import os

# Load your dataset
df = pd.read_csv('data/data_moods.csv')

# Select features and target
features = ['danceability', 'energy', 'loudness', 'valence']
X = df[features]
y = df['mood']  # or 'genre' if you're predicting genre

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save model
os.makedirs('models', exist_ok=True)
with open('models/mood_predictor.pkl', 'wb') as f:
    pickle.dump(model, f)

print("✅ Model trained and saved to models/mood_predictor.pkl")
