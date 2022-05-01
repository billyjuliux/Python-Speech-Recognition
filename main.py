from neuralintents import GenericAssistant
from regex import P
import speech_recognition
import pyttsx3 as tts
import sys

recognizer = speech_recognition.Recognizer()

speaker = tts.init()
# Set the speaker talk rate
speaker.setProperty('rate', 150)

# Set the todo list
todo_list = ['Go Shopping', 'Clean Room']

def add_todo():
  global recognizer

  # Prompt the user for the todo
  speaker.say("What to do do you want to add?")
  speaker.runAndWait()

  done = False
  while not done:
    try:
      with speech_recognition.Microphone() as mic:
        # Recognize what user is saying
        recognizer.adjust_for_ambient_noise(mic, duration=0.5)
        audio = recognizer.listen(mic)
        todo_item = recognizer.recognize_google(audio).lower()

        todo_list.append(todo_item)
        done = True

        # Tell the user the process is done
        speaker.say(f"I added {todo_item} to the to do list!")
        speaker.runAndWait()
    
    except speech_recognition.UnknownValueError:
      recognizer = speech_recognition.Recognizer()
      speaker.say("I did not understand you, please try again!")
      speaker.runAndWait()

def show_todos():
  global recognizer

  if (todo_list == []):
    # If there is none
    speaker.say("Your to do list is empty")
  else :
    # Say every todo item
    speaker.say("The items on your to do list are the following")
    for item in todo_list:
      speaker.say(item)
    
  speaker.runAndWait()

def reset_todos():
  global recognizer
  global todo_list

  # Delete all todo
  todo_list = []

  speaker.say("I have deleted all your to do list.")
  speaker.runAndWait()

def greeting():
  # Response the greeting
  speaker.say("Hello, what can I do for you?")
  speaker.runAndWait()

def exit():
  speaker.say("Goodbye. See you next time!")
  speaker.runAndWait()
  sys.exit(0)

mappings = {
  "greeting": greeting,
  "add_todo": add_todo,
  "show_todos": show_todos,
  "reset_todos": reset_todos,
  "exit": exit
}

# Setup the assistant
assistant = GenericAssistant('intents.json', intent_methods=mappings)
assistant.train_model()

# Stream for user input
while True:
  try :
    with speech_recognition.Microphone() as mic :
      # Recognize what user is saying
      recognizer.adjust_for_ambient_noise(mic, duration=0.5)
      audio = recognizer.listen(mic)
      message = recognizer.recognize_google(audio).lower()
    
    # Request for response to the assistant
    assistant.request(message)

  except speech_recognition.UnknownValueError:
      recognizer = speech_recognition.Recognizer()
      speaker.say("I did not understand you, please try again!")
      speaker.runAndWait()