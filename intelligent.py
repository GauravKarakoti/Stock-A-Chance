from brain6 import ReplyBrain
from Listen import MicExecution

def MainExecution():

    from Speak2 import Speak
    Speak("Initiating Stock-a-chance!")
    Speak("Everything operational sir!")

    while True:
        Data = MicExecution()
        if "terminate" in Data:
            Speak("Terminating!! Have a great day!")
            break
        Data = str(Data).replace(".","")
        Reply = ReplyBrain(Data)
        Speak(Reply)
           
MainExecution()