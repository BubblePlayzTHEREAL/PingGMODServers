from flask import Flask, request, send_file, jsonify
from PIL import Image, ImageDraw, ImageFont
import a2s
import os

app = Flask(__name__)

def create_image_with_names(player_names, output_filename):
    width, height = 400, 200
    image = Image.new("RGB", (width, height), "white")

    draw = ImageDraw.Draw(image)

    font_path = "font.otf"
    font_size = 20
    font = ImageFont.truetype(font_path, font_size)

    text_color = (0, 0, 0)
    y_position = 1

    for player_name in player_names:
        draw.text((5, y_position), player_name, font=font, fill=text_color)
        y_position += font_size + 5

    image.save(output_filename)
    return image

def get_player_names(ip, port):
    print("Getting player names")
    # Convert IP address to a tuple of strings
    address = (ip, int(port))  # Convert port to an integer

    players = a2s.players(address, timeout=3, encoding="utf-8")
    player_names = [player.name for player in players]
    print("Gotted em")
    return player_names

@app.route('/', methods=['GET'])
def generate_image():
    os.system("cls")
    ip = request.args.get('ip')
    port = request.args.get('port')

    if not ip or not port:
        return jsonify({"error": "Missing 'ip' or 'port' in the URL parameters."}), 400

    print(ip)
    print(port)
    player_names = get_player_names(ip, port)

    if player_names:
        output_filename = "img.png"
        image = create_image_with_names(player_names, output_filename)
        print("Sent Image back!")
        return send_file(output_filename, mimetype='image/png'), 200
    else:
        print("Failed")
        return jsonify({"error": "Failed to fetch player names."}), 500

if __name__ == '__main__':
    app.run(debug=True)
