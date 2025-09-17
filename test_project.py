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


def test_add_keywords_to_sentiment():
    """Test that keywords are assigned correctly for each sentiment."""
    positive_keywords = ["good mood", "happy", "chill vibes", "feel good", "relaxing"]
    negative_keywords = ["sad song", "blue", "heart break", "memories"]
    neutral_keywords = ["inspo", "lofi", "nature", "mood", "calm"]

    assert project.add_keywords_to_sentiment("Positive") in positive_keywords
    assert project.add_keywords_to_sentiment("Negative") in negative_keywords
    assert project.add_keywords_to_sentiment("Neutral") in neutral_keywords


def test_fetch_suggestions_basic():
    """Test fetch_suggestions returns proper structure with real API call."""
    result = project.fetch_suggestions("happy")

    assert isinstance(result, list)
    assert len(result) <= 3

    for song in result:
        assert isinstance(song, dict)
        assert "song" in song
        assert "artist" in song
        assert "url" in song
        assert "thumbnail" in song
