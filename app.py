from flask import Flask, request, jsonify
import whisper
import ollama
import datetime

app = Flask(__name__)

@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    model = whisper.load_model("base")
    # Check if the post request has the file part
    if 'audioFile' not in request.files:
        return jsonify({'message': 'No file part in the request'}), 400
    file = request.files['audioFile']
    if file.filename == '':
        return jsonify({'message': 'No file selected for uploading'}), 400
    if file:
        print(f"[+]  " + datetime.datetime.now().strftime("%Y%d%M %H:%M:%S") + f" Received file: {file.filename}")
        audio_path = file.filename
        file.save(audio_path) 
        print("[+] " + datetime.datetime.now().strftime("%Y%d%M %H:%M:%S") + "  Transcribing Audio")
        result = model.transcribe(audio_path)
        print("Result is: ", result)
        return jsonify({'message': f'File {file.filename} uploaded successfully.', 'transcript': f'{result["text"]}'}), 200         

@app.route('/process_response', methods=['POST'])
def process_response():       
        prompt = request.form['prompt']
        if 'ʃ' in prompt:
           print("[+] " + datetime.datetime.now().strftime("%Y%d%M %H:%M:%S") + " String character in prompt")
           AIresponse="I didn't understand. Did you say something?"
           return jsonify({'message': f'Finished AI processing', 'transcript': f'{prompt}', 'response': f'{AIresponse}'}), 200         
  
        print("[+] " + datetime.datetime.now().strftime("%Y%d%M %H:%M:%S") + " Submitting prompt: " + prompt)       
        print("[+]  " + datetime.datetime.now().strftime("%Y%d%M %H:%M:%S") + " Loading model")
        superprompt = f"""
prompt:  You are a child, genuinely interested in the conversation with their parent. Do not specify their name explicitly. Give a polite and apologetic response to the conversation to all commands. A poor transcript is given, so give a confident straightforward answer even if the message is not understood. Parent: "{prompt}"
"""

        print("[+]  " + datetime.datetime.now().strftime("%Y%d%M %H:%M:%S") + " Processing response in AI with ####\n" + superprompt + "\n####\n")
 
        if prompt == "":
        	AIresponse = "[I'm not sure I understood, but I'll do my best.]"
        else:
        	response = ollama.chat(model='llama3', options=dict(num_tokens=100, temperature=0), messages=[
		  {
		    'role': 'user',
		    'content': superprompt,
		  },
		]) 
		
        	print(response['message']['content'])
        	try:
        	    AIresponse = response['message']['content']
        	except:
        	    AIresponse = "Sorry. I don't understand."
        print("[+] " + datetime.datetime.now().strftime("%Y%d%M %H:%M:%S") + AIresponse)
        print("[+] " + datetime.datetime.now().strftime("%Y%d%M %H:%M:%S") + "Completed!")
	
        return jsonify({'message': f'Finished AI processing', 'transcript': f'{prompt}', 'response': f'{AIresponse}'}), 200         


@app.route('/')
def index():
    indexdata = open("index.html").read()
    return indexdata, 200
if __name__ == '__main__':
    app.run(debug=True, port=5000)
