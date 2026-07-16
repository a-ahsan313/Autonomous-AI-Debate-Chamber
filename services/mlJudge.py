import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

_POSITIVE_WORDS = {
    "good", "great", "effective", "clearly", "strong", "benefit", "benefits",
    "proven", "essential", "valuable", "improve", "improves", "success",
    "successful", "advantage", "advantages", "right", "true", "sound",
    "reasonable", "compelling", "wins", "win", "positive", "better", "best",
}
_NEGATIVE_WORDS = {
    "bad", "wrong", "flawed", "fails", "fail", "risk", "risky", "danger",
    "dangerous", "weak", "false", "unproven", "problem", "problems",
    "harmful", "harm", "worse", "worst", "negative", "reckless", "ignores",
    "loses", "lose", "unreasonable", "misleading",
}

class DebateRegressionJudge:
    def __init__(self):
        self.model = None # Your sklearn model will live here
        self.feature_columns = ["word_count", "complexity_score", "sentiment"] # Add more features as you implement them
        
    def extract_NLP_features(self, text):
        """
        Machine Learning models require NUMBERS, not text.
        Convert the raw text into mathematical features.
        """

        words = text.split()
        word_count = len(words)

        if word_count > 0:
            cleaned = [word.lower().strip(".,!?;:()[]{}\"'") for word in words]
            cleaned = [w for w in cleaned if w]  # Remove empty strings
            complexity_score = (
                round(sum(len(w) for w in cleaned) / len(cleaned), 2)
                if cleaned
                else 0.0
            )
        else:
            complexity_score = 0.0

        if word_count > 0:
            lowered = [w.strip(".,!?;:\"'()").lower() for w in words]
            pos = sum(1 for w in lowered if w in _POSITIVE_WORDS)
            neg = sum(1 for w in lowered if w in _NEGATIVE_WORDS)
            sentiment = round((pos - neg) / word_count * 5, 3)
            sentiment = max(-1.0, min(1.0, sentiment))
        else:
            sentiment = 0.0



        return {
            "word_count": word_count,
            "complexity_score": complexity_score,
            "sentiment": sentiment,
        }

    def train_model(self, dataset_path):
        """
        Trains the Regression Model to score debates perfectly based on human data.
        """
        print(f"Loading dataset from {dataset_path}...")

        df = pd.read_csv(dataset_path)
        missing = [c for c in self.feature_columns + ["human_persuasiveness_score"] if c not in df.columns]

        if missing:
            raise ValueError(f"Dataset is missing required columns: {missing}")
        
        X = df[self.feature_columns]
        y = df["human_persuasiveness_score"]
 
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        model = RandomForestRegressor(n_estimators=200, random_state=42)
        model.fit(X_train, y_train)
 
        predictions = model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        r2 = r2_score(y_test, predictions)
 
        self.model = model
        print(f"Model Trained! MSE={mse:.4f}, R2={r2:.4f}")
 
        return {"mse": round(float(mse), 4), "r2_score": round(float(r2), 4)}
        

    def predict_score(self, text):
        """
        This is called live during the AI debate to judge the LLM's argument.
        """
        if self.model is None:
            raise Exception("Model is not trained yet!")
        
        features = self.extract_NLP_features(text)
        feature_row = pd.DataFrame([[features[col] for col in self.feature_columns]], columns=self.feature_columns)

        raw_score = self.model.predict(feature_row)[0]
            
        score = max(1.0, min(10.0, float(raw_score)))
        return round(score, 2)
