from datetime import datetime
import speech_recognition as sr
import pyttsx3  # là một thư viện Python cho phép chúng ta chuyển văn bản thành giọng nói và ngược lại.
import webbrowser
import wikipedia
import wolframalpha
import playsound
from gtts import gTTS


engine = pyttsx3.init()  # pyttsx3.init() là một hàm khởi tạo đối tượng engine
voices = engine.getProperty('voices')  # lấy ra danh sách các giọng nói có sẵn
engine.setProperty('voice', voices[0].id)  # thiết lập giọng nói
# voices[0].id là giọng nói nam
activationWord = "computer"  # từ kích hoạt


def speak(text, rate=120):
    # engine.setProperty('rate', rate)  # tốc độ nói
    # engine.say(text)  # nói
    # engine.runAndWait()  # chạy và đợi
    tts = gTTS(text=text, lang='en')
    tts.save('audio.mp3')
    playsound.playsound('audio.mp3')


# Configure browser
chrome_path = r"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))


def parseCommand():
    listener = sr.Recognizer()
    print("Listening...")

    with sr.Microphone() as source:  # lấy dữ liệu từ microphone
        input_speech = listener.listen(source)  # lắng nghe

        try:
            print('Recognizing...')
            query = listener.recognize_google(input_speech, language='en-gb')  # chuyển đổi thành văn bản
            print(f'You said: {query}\n')
        except Exception as e:
            print('Say that again please...')
            speak('Say that again please...')
            print(e)
            return 'None'
        return query


def search_wikipedia(query=''):
    search_results = wikipedia.search(query)
    if not search_results:
        print('No results found')
        return 'No results found'
    try:
        wiki_page = wikipedia.page(search_results[0])
    except wikipedia.DisambiguationError as e:
        wiki_page = wikipedia.page(e.options[0])
    print(wiki_page.title)
    wiki_summary = str(wiki_page.summary)
    return wiki_summary


# Main loop
if __name__ == '__main__':
    speak('Greeting', 150)

    while True:
        # Parse as a list
        query = parseCommand().lower().split()

        # Check if the activation word is in the query
        if query[0] == activationWord:
            query.pop(0)  # remove the activation word from the query

            # List command
            if query[0] == 'say':
                if 'hello' in query:
                    speak('Greeting, Master')
                else:
                    query.pop(0)
                    speech = ' '.join(query)
                    speak(speech)

            if query[0] == 'go' and query[1] == 'to':
                speak('Opening...')
                url = ' '.join(query[2:])
                webbrowser.get('chrome').open_new(url)

            # Wikipedia
            if query[0] == 'wikipedia':
                query = ' '.join(query[1:])
                speak('According to Wikipedia')
                wikipedia_result = search_wikipedia(query)
                print(wikipedia_result)
                speak(wikipedia_result)

            if query[0] == 'goodbye':
                speak('Goodbye, Master')
                break
