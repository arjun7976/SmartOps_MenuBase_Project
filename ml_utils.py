"""Machine learning utilities for the Streamlit app."""
import streamlit as st
import numpy as np
import pandas as pd

class TrainingProgress:
    """Custom callback for training progress with Streamlit UI updates."""
    def __init__(self, progress_bar, status_text, total_epochs):
        self.progress_bar = progress_bar
        self.status_text = status_text
        self.total_epochs = total_epochs
        self._active = True
        
    def on_train_begin(self, logs=None):
        self._active = True
        
    def on_train_end(self, logs=None):
        self._active = False
        
    def on_epoch_end(self, epoch, logs=None):
        if not self._active:
            return
            
        try:
            if logs is None:
                logs = {}
                
            # Calculate progress safely
            progress = min(1.0, max(0.0, (epoch + 1) / max(1, self.total_epochs)))
            
            # Update progress bar if it exists and is valid
            if hasattr(self.progress_bar, 'progress'):
                try:
                    self.progress_bar.progress(progress)
                except Exception as e:
                    print(f"Progress bar update error: {e}")
                    self._active = False
                    return
            
            # Prepare status message
            status = (
                f"Epoch {epoch + 1}/{self.total_epochs} - "
                f"Loss: {logs.get('loss', 0):.4f}, "
                f"Accuracy: {logs.get('accuracy', 0):.4f}, "
                f"Val Loss: {logs.get('val_loss', 0):.4f}"
            )
            
            # Update status text
            if hasattr(self.status_text, 'text'):
                try:
                    self.status_text.text(status)
                except Exception as e:
                    print(f"Status text update error: {e}")
                    self._active = False
                    
        except Exception as e:
            print(f"Error in TrainingProgress callback: {e}")
            self._active = False

def get_tensorflow():
    """Lazy load TensorFlow to prevent recursion issues."""
    try:
        import tensorflow as tf
        return tf
    except ImportError as e:
        st.error("❌ TensorFlow is not installed. Please install it first.")
        return None

def train_model(X_train, y_train, epochs=20):
    """Train a neural network model with the given data."""
    tf = get_tensorflow()
    if tf is None:
        return None, None
    
    try:
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(16, activation='relu', input_shape=(X_train.shape[1],)),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(8, activation='relu'),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])
        
        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        return model, None
    except Exception as e:
        st.error(f"❌ Error creating model: {str(e)}")
        return None, None
