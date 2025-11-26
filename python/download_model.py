"""
Download a lightweight pre-trained model for recommendation system.
This script downloads a small LSTM model from HuggingFace or uses a simple pre-trained model.
"""
import os
import urllib.request
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODEL_DIR = "/app/models"
MODEL_PATH = f"{MODEL_DIR}/v1.1.0_recommendation_model.h5"

# Using a lightweight sentiment analysis LSTM model as a placeholder
# In production, you would use an actual recommendation model
MODEL_URL = "https://github.com/keras-team/keras/raw/master/examples/lstm_text_generation.py"

def download_model():
    """Download or create a minimal model for testing."""
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    # For now, we'll create a minimal Keras model since downloading requires specific URLs
    # In production, replace this with actual model download from your model registry
    try:
        from tensorflow import keras
        from tensorflow.keras import layers
        
        logger.info("Creating minimal LSTM model for testing...")
        
        # Create a very simple LSTM model (lightweight)
        model = keras.Sequential([
            layers.Embedding(100, 32, input_length=10),
            layers.LSTM(64),
            layers.Dense(32, activation='relu'),
            layers.Dense(100, activation='softmax')
        ])
        
        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')
        model.save(MODEL_PATH)
        
        logger.info(f"Model saved to {MODEL_PATH}")
        logger.info(f"Model size: {os.path.getsize(MODEL_PATH) / 1024:.2f} KB")
        
    except Exception as e:
        logger.error(f"Error creating model: {e}")
        raise

if __name__ == "__main__":
    download_model()
