import speech_recognition as sr
import pyttsx3
import wikipedia
import webbrowser
import datetime

word_to_number = {
    "zero": "0", "one": "1", "two": "2", "three": "3", "four": "4",
    "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9",
    "plus": "+", "minus": "-", "multiplied": "*",
    "divided": "/", "over": "/", "into": "*", "power": "**"
}




#Initialize text to speech library
engine = pyttsx3.init()
engine.setProperty('rate',175)  #speaking rate for jaarvis
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)    #Male voice for female voice [1]

def  speak(text):
    engine.say(text)
    engine.runAndWait()

def greet_user():
    hour = datetime.datetime.now().hour     #to get the time when you open it 0-23
    if 0<=hour<12:
        speak("Good Morning sir")
    elif 12<=hour<18:
        speak("Good Afternoon sir")
    else:
        speak("Good Evening sir")

#Main function on which jarvis works
def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        recognizer.pause_threshold = 1  #It will start processing input if you stopped for 2sec
        audio = recognizer.listen(source)
    try:
        print("Recognizing....")
        query = recognizer.recognize_google(audio , language='en-us') #sends input to google's api
        print(f"You said : {query}")
        return query.lower()
    except Exception as e:
        return speak("Sorry i did not get that please say again")



def words_to_expression(query):
    ignore_words = {"calculate", "what", "is", "the"}
    words = query.lower().split()
    expression = ""

    for word in words:
        if word in ignore_words:
            continue
        elif word in word_to_number:
            expression += word_to_number[word]
        elif word.isdigit():
            expression += word
        else:
            expression += f" {word} "  # provide space for proper readability

    return expression.strip()

def do_math_from_speech(query):
    expression = words_to_expression(query)
    try:
        result = eval(expression)
        spoken_expression = query.replace("calculate", "").strip()
        final_response = f"{spoken_expression} equals {result}"
        speak(final_response)
        return final_response
    except Exception as e:
        error_msg = f"Sorry, I couldn't calculate that. Error: {e}"
        speak(error_msg)
        return error_msg



def execute_command(query):
    if 'wikipedia' in query:
        speak("Searching Wikipedia")
        query = query.replace("wikipedia", "").strip()

        try:
            result = wikipedia.summary(query, sentences=5)
            speak(result)
        except wikipedia.exceptions.DisambiguationError as e:
            speak("Your query is too vague. Please be more specific.")
            print(f"DisambiguationError: {e}")
    elif 'hello how are you' in query:
        speak('I am fine thank you')
    elif 'open youtube' in query:
        speak("Opening youtube")
        webbrowser.open("https://youtube.com")
    elif 'open google' in query:
        speak("opening google")
        webbrowser.open("https://google.com")
    elif 'calculate' in query or any(op in query for op in ["plus", "minus", "into", "divided"]):
         do_math_from_speech(query)
    elif 'tell current time' in query:
        current_time = datetime.datetime.now().strftime('%H:%M:%S')
        speak(f"Yes sir the current time is {current_time}")
        print(f"{current_time}")
    elif 'quit' in query or 'exit' in query:
        speak("GoodBye sir meet you soon")


if __name__ == "__main__":
    greet_user()
    try:
        while True:
            command = listen_command()
            if command:
                execute_command(command)
    except KeyboardInterrupt:
        speak("Goodbye sir. Shutting down.")
