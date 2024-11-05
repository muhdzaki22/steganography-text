from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Function to convert a string into binary representation
def text_to_binary(text):
    return ''.join(f"{ord(char):08b}" for char in text)

# Function to convert binary data into zero-width characters
def binary_to_zero_width(binary):
    return binary.replace('0', '\u200B').replace('1', '\u200C')

# Function to hide a secret message within the middle of the public text
def encode_message(public_text, private_text):
    binary_message = text_to_binary(private_text)
    encoded_message = binary_to_zero_width(binary_message)
    mid_index = len(public_text) // 2
    return public_text[:mid_index] + '\u200D' + encoded_message + '\u200D' + public_text[mid_index:]

# Function to decode the hidden message from a steganographed text
def decode_message(stego_text):
    parts = stego_text.split('\u200D')
    if len(parts) < 3:
        return "No hidden message found."
    encoded_message = parts[1]
    binary_message = encoded_message.replace('\u200B', '0').replace('\u200C', '1')
    chars = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
    return ''.join([chr(int(char, 2)) for char in chars])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encode', methods=['POST'])
def encode():
    public_text = request.form['public_text']
    private_text = request.form['private_text']
    stego_text = encode_message(public_text, private_text)
    return jsonify({"stego_text": stego_text})

@app.route('/decode', methods=['POST'])
def decode():
    stego_text = request.form['stego_text']
    decoded_message = decode_message(stego_text)
    return jsonify({"decoded_message": decoded_message})

if __name__ == '__main__':
    app.run(debug=True)
