import requests 
import json

def emotion_detector(text_to_analyse): 
    # URL of the emotion detector service 
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'

    # Constructing the request payload in the expected format 
    myobj = { "raw_document": { "text": text_to_analyse } }

    # Custom header specifying the model ID for the sentiment analysis service 
    header = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}

    # Sending a POST request to the emotion detection analysis API 
    response = requests.post(url, json=myobj, headers=header)

    # Parsing the JSON response from the API 
    formatted_response = json.loads(response.text)

    # Extracting emotions scores from the response 
    emotions = formatted_response['emotionPredictions'][0]['emotion']  # often a list
    anger_score = emotions['anger']
    disgust_score = emotions['disgust']
    fear_score = emotions['fear']
    joy_score = emotions['joy']
    sadness_score = emotions['sadness']

    # Extracting dominant emotion from the response
    dominant_emotion = max(emotions, key=emotions.get)

    # Returning a dictionary containing emotion results 
    return {
        'anger': anger_score,
        'disgust': disgust_score,
        'fear': fear_score,
        'joy': joy_score,
        'sadness': sadness_score,
        "dominant_emotion": dominant_emotion
    }