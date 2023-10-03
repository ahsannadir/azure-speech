#Importing Libraries
from dotenv import load_dotenv
import os
from playsound import playsound

# Import namespaces
import azure.cognitiveservices.speech as speech_sdk

# Loading Key & Region
load_dotenv()
cog_key = os.getenv('COG_SERVICE_KEY')
cog_region = os.getenv('COG_SERVICE_REGION')

# Configure speech servie
speech_config = speech_sdk.SpeechConfig(cog_key, cog_region)
print('Ready to use speech service in:', speech_config.region)

# Main Function
def main():
    try:
        command = TranscribeCommand()
        print(f"Your Name is: {SayMyName(command)}")
        TranslateSpeech()

    except Exception as ex:
        print(ex)

# Function to extract extract text from the audio file 
def TranscribeCommand():
    command = ''

    # Configure speech recognition
    current_dir = os.getcwd()
    audioFile = 'D:\\Azure102\\AI-102-AIEngineer\\07-speech\\Python\\speaking-clock\\ahsan_intro.wav'
    #playsound(audioFile)
    audio_config = speech_sdk.AudioConfig(filename=audioFile)
    speech_recognizer = speech_sdk.SpeechRecognizer(speech_config, audio_config)

    # Process speech input
    speech = speech_recognizer.recognize_once_async().get()
    if speech.reason == speech_sdk.ResultReason.RecognizedSpeech:
        command = speech.text
        print(command)
    else:
        print(speech.reason)
        if speech.reason == speech_sdk.ResultReason.Canceled:
            cancellation = speech.cancellation_details
            print(cancellation.reason)
            print(cancellation.error_details)

    return command

# Function to Call name from the Extracted Audio
def SayMyName(sentence):
    words = sentence.split()
    for i in range(1, len(words)):
        if words[i][0].isupper():
            return words[i]
        

# Function to translate the text into Urdu & save it
def TranslateSpeech():
    global translation_config

    translation_config = speech_sdk.translation.SpeechTranslationConfig(cog_key, cog_region)
    translation_config.speech_recognition_language = 'en-US'
    translation_config.add_target_language('ur')
    print('Ready to translate from',translation_config.speech_recognition_language)

    translation = ''
    targetLanguage = 'ur'

    audioFile = 'D:\\Azure102\\AI-102-AIEngineer\\07-speech\\Python\\speaking-clock\\ahsan.wav'

    audio_config = speech_sdk.AudioConfig(filename=audioFile)
    translator = speech_sdk.translation.TranslationRecognizer(translation_config, audio_config = audio_config)
    print("Getting speech from file...")
    result = translator.recognize_once_async().get()
    print('Translating "{}"'.format(result.text))
    translation = result.translations[targetLanguage]
    print(translation)

    voices = {
        "ur": "ur-PK-UzmaNeural"
    }

    speech_config.speech_synthesis_voice_name = voices.get(targetLanguage)
    speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config)
    speak = speech_synthesizer.speak_text_async(translation).get()
    if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
        print(speak.reason)

    with open('ahsan_intro_translated.wav', 'wb') as audio_file:
        audio_file.write(speak.audio_data)

if __name__ == "__main__":
    main()