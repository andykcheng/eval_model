import requests
import json
import time

# Define the API URL
url = "http://192.168.4.27:11434/api/chat"

def runRequest(model, instruction, message, marker):
    time_start = time.time()
    # Define the payload
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": instruction},
            {"role": "user", "content": message}
        ],
        "temperature": 0.01,
        "format": "json",
        "stream": False
    }

    # Make the POST request
    response = requests.post(url, json=payload)
    time_end = time.time()
    # Check the response
    if response.status_code == 200:
        result = response.json()
        answer = result["message"]["content"]
        # make the model name 12 characters long by padding with spaces
        model = model.ljust(20)
        time_taken = time_end - time_start
        print("Model:", model, "Answer:", answer, " (" + str(time_taken) + "s)")
        
        
        # write to an output with filename output<dd_MM_yyyy_hh_mm_ss> file for further analysis with the following format:
        """ 
        Time: <now>
        Model: <model_name>
        Instruction: <instruction>
        Question: <question>
        Answer: <answer>
        
        ================================================
        """
        with open("output" + marker + ".txt", "a") as f:
            f.write("Time: " + time.strftime("%d_%m_%Y_%H_%M_%S") + "\n")
            f.write("Model: " + model + "\n")
            f.write("Instruction: " + instruction + "\n")
            f.write("Question: " + message + "\n")
            f.write("Answer: " + answer + "\n")
            f.write("Time taken: " + str(time_taken) + "s\n")
            f.write("================================\n")
        
        # print("Response:", result["message"]["content"])
    else:
        print("Error:", response.status_code, response.text)
models = [
        # "llama3.2:1b", 
        # "llama3.2:latest", 
        # "llama3.1", #8b
        # "qwen:0.5b", 
        # "qwen:4b",
        # "qwen2.5:3b",
        # "qwen2.5:7b", # 7b
        # "qwen2.5:32b",
        "qwen2.5-coder:3b",
        "qwen2.5-coder:7b"
        ]
light_instruction = """# Instruction
     Your name is Chatty. You are a chatbot that would change user request into function calls.  Only use the functions available to you. If function is not available, please raise error by returning ```[{"error":"Function not available"}]```.
     IMPORTANT: Please only output the JSON, and do not print any other information. Only apply the necesasry functions, nothing else. 
     
     # Available functions
     turn_light_on_off(lightID: int, onOff: bool) - Turn the light on or off.
     change_light_brightness(lightID: int, brightness: int) - Change the brightness of the light.
     change_light_color(lightID: int, color: str) - Change the color of the light. Available colors are red, green, blue, yellow, cyan, magenta, white.
     flash_light(lightID: int, frequency: float) - Flash the light with a frequency in Hz.
     # Return format
     If function is available:
     [{"result": "success", "function_name": "turn_light_on_off", "lightID": 1, "onOff": true}]
     
     If function is not available:
     [{"error": "Function not available"}]
     """
instruction_questions = [
    # {"instruction": "You are a friendly assistant called Chatty. You only answer in a few words.", "question": "What is your name?"},
    # {"instruction": light_instruction, "question": "Turn light 1 on."},

    # {"instruction": light_instruction, "question": "Change light 1 brightness to 50%"},
    {"instruction": light_instruction, "question": "將燈一光度轉成 50%"},
    # {"instruction": light_instruction, "question": "Change light 1 to red"},
    # {"instruction": light_instruction, "question": "將燈一轉成紅色"},
    # {"instruction": light_instruction, "question": "將一號燈轉成綠色"},
    # {"instruction": light_instruction, "question": "Cook me an egg."},
    # {"instruction": light_instruction, "question": "Turn on washing machine."},
    {"instruction": light_instruction, "question": "light one flash in 2Hz"},
    {"instruction": light_instruction, "question": "light one flash in 2kHz"},
    {"instruction": light_instruction, "question": "light one flash in 5.4kHz"},
    
    
    
    
    
    
]
test_marker = time.strftime("%d_%m_%Y_%H_%M_%S") + "_est_small_models"
for instruction_question in instruction_questions:    
    # print("Instruction:", instruction_question["instruction"])
    print("\n\n\nQuestion:", instruction_question["question"])
    for model in models:
        runRequest(model, instruction_question["instruction"], instruction_question["question"], test_marker)
