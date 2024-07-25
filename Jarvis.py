
import speech_recognition as sr
import pyttsx3
import openai

# Initializing pyttsx3
listening = True
engine = pyttsx3.init()

# Set your OpenAI API key and customize the ChatGPT role
openai.api_key = "sk-proj-IY99eJ1NSsbUo9l8FRm5T3BlbkFJeRP9F87UfCiUo2to2ute"
messages = [{"role": "system", "content": "Your name is Jarvis. Respond in the same language as the user's input, either Hindi or English. Always prioritize the user's interest. Be loyal to the user."}]

# Customizing the output voice
voices = engine.getProperty('voices')
for voice in voices:
    if "hindi" in voice.name.lower() or "english" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

rate = engine.getProperty('rate')
volume = engine.getProperty('volume')

def get_response(user_input, language):
    messages.append({"role": "user", "content": user_input})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    ChatGPT_reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": ChatGPT_reply})
    return ChatGPT_reply

while listening:
    with sr.Microphone() as source:
        recognizer = sr.Recognizer()
        recognizer.adjust_for_ambient_noise(source)
        recognizer.dynamic_energy_threshold = 3000

        try:
            print("Listening...")
            audio = recognizer.listen(source, timeout=5.0)
            response = recognizer.recognize_google(audio, language="hi-IN")
            print(response)

            if "jarvis" in response.lower():
                if any(word in response.lower() for word in ["hello", "hi", "how", "what", "why", "when", "where"]):
                    language = "en"
                else:
                    language = "hi"

                response_from_openai = get_response(response, language)
                engine.setProperty('rate', 120)
                engine.setProperty('volume', volume)
                engine.say(response_from_openai)
                engine.runAndWait()
            else:
                print("Didn't recognize 'Jarvis'.")
        except sr.UnknownValueError:
            print("Didn't recognize anything.")
