import project
import pytest
from unittest.mock import Mock


def test_analyze_sentiment_positive():
    """Test that clearly positive text returns 'Positive'."""
    result = project.analyze_sentiment("I absolutely love this! It's amazing and wonderful!")
    assert result == "Positive"


def test_analyze_sentiment_negative():
    """Test that clearly negative text returns 'Negative'."""
    result = project.analyze_sentiment("I hate this so much. It's terrible and awful.")
    assert result == "Negative"


def test_analyze_sentiment_neutral():
    """Test that neutral text returns 'Neutral'."""
    result = project.analyze_sentiment("The sky is blue. Cars are parked.")
    assert result == "Neutral"


def test_analyze_sentiment_boundary_positive():
    """Test the positive boundary (0.25)."""
    assert project.analyze_sentiment("This is great!") == "Positive"


def test_analyze_sentiment_boundary_negative():
    """Test the negative boundary (-0.25)."""
    assert project.analyze_sentiment("This is bad") == "Negative"


def test_add_keywords_to_sentiment_positive():
    """Test that positive sentiment returns valid positive keywords."""
    positive_keywords = ["good mood", "happy", "chill vibes", "feel good", "relaxing"]
    result = project.add_keywords_to_sentiment("Positive")
    assert result in positive_keywords


def test_add_keywords_to_sentiment_negative():
    """Test that negative sentiment returns valid negative keywords."""
    negative_keywords = ["sad song", "blue", "heart break", "memories"]
    result = project.add_keywords_to_sentiment("Negative")
    assert result in negative_keywords


def test_add_keywords_to_sentiment_neutral():
    """Test that neutral sentiment returns valid neutral keywords."""
    neutral_keywords = ["inspo", "lofi", "nature", "mood", "calm"]
    result = project.add_keywords_to_sentiment("Neutral")
    assert result in neutral_keywords
