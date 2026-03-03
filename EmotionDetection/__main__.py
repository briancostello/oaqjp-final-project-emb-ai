from .emotion_detection import emotion_detector

def main():
    text = input("Enter text to analyze emotions: ")
    result = emotion_detector(text)
    print(result)

if __name__ == "__main__":
    main()