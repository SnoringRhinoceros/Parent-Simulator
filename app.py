from flask import Flask, request, jsonify
import whisper
import gpt4all
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
        LLMmodel = gpt4all.GPT4All("mistral-7b-openorca.Q4_0.gguf", allow_download=False)       
# You are a casual pal, genuinely interested in the conversation at hand with someone talking to their parent.    
        superprompt = f"""
You are a child, genuinely interested in the conversation with their parent. Give a polite and apologetic response to the conversation to all commands. Thank the parent for being helpful. Confidently give a straightforward response to the parent, even if you don't understand them. DO NOT ask to repeat, and DO NOT ask for clarification. Just answer the parent directly without continuing the conversation. Do not lie or make up context.
A poor transcription of conversation is given below. The output should only have the child response in square brackets.

Parent: "You should have focused on your studies instead."
Child: [Thank you for the advice. I will try to manage my time better next time. I love you.]

Parent: "asdkadajskdjlak"
Child: [I'm not sure I understood, but I'll do my best.]

Parent: "{prompt}"
Child: 
"""

        print("[+]  " + datetime.datetime.now().strftime("%Y%d%M %H:%M:%S") + " Processing response in AI with ####\n" + superprompt + "\n####\n")
        if prompt == "":
        	AIresponse = "[I'm not sure I understood, but I'll do my best.]"
        else:
        	AIresponse = LLMmodel.generate(superprompt)
        print("[+] " + datetime.datetime.now().strftime("%Y%d%M %H:%M:%S") + AIresponse)
        print("[+] " + datetime.datetime.now().strftime("%Y%d%M %H:%M:%S") + "Completed!")

        return jsonify({'message': f'Finished AI processing', 'transcript': f'{prompt}', 'response': f'{AIresponse}'}), 200         


@app.route('/')
def index():
    indexdata = open("index.html").read()
    return indexdata, 200
if __name__ == '__main__':
    app.run(debug=True, port=5000)
