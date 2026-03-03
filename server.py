
"""
Flask server for the Emotion Detector application.

This module exposes two routes:
- /emotionDetector: Accepts text input and returns emotion analysis results.
- /: Renders the index page for the web application.
"""

from flask import Flask, render_template, request, make_response
from EmotionDetection.emotion_detection import emotion_detector

app = Flask("Emotion Detector")


@app.route("/emotionDetector")
def emot_detector():
    """Analyze input text for emotions and return a formatted response.

    Returns:
        flask.Response: Plain text response for invalid input, or an HTML-formatted
        string containing emotion scores and the dominant emotion.
    """
    text_to_analyze = request.args.get("textToAnalyze", "")

    # Helper: always return a response the UI will show, and prevent caching
    def invalid_text_response():
        """Create a non-cached, plain-text response for invalid input.

        Returns:
            flask.Response: Response containing an invalid-text message.
        """
        resp = make_response("Invalid text! Please try again!", 200)
        resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        resp.headers["Pragma"] = "no-cache"
        resp.headers["Expires"] = "0"
        resp.mimetype = "text/plain"
        return resp

    # 1) Blank input → return message (200 so UI updates)
    if not text_to_analyze.strip():
        return invalid_text_response()

    # 2) Call emotion detector
    result = emotion_detector(text_to_analyze)

    # 3) API returned 400 → your detector returns dict with dominant_emotion=None
    if not isinstance(result, dict) or result.get("dominant_emotion") is None:
        return invalid_text_response()

    # 4) Successful response
    anger = result["anger"]
    disgust = result["disgust"]
    fear = result["fear"]
    joy = result["joy"]
    sadness = result["sadness"]
    dominant = result["dominant_emotion"]

    resp = make_response(
        "For the given statement, the system response is "
        f"'anger': {anger}, 'disgust': {disgust}, 'fear': {fear}, "
        f"'joy': {joy} and 'sadness': {sadness}. "
        f"The dominant emotion is <strong>{dominant}</strong>.",
        200
    )
    resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "0"
    return resp


@app.route("/")
def render_index_page():
    """Render the home page for the Emotion Detector web application.

    Returns:
        str: Rendered HTML template for the index page.
    """
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
