from flask import Flask, request, jsonify, Markup
from flask_cors import CORS
import subprocess

import helper

app = Flask(__name__)
CORS(app)

@app.route("/run-script", methods=["POST"])
def run_script():
    input_data = request.json["input"]

    print("POST received")
    
    # Execute your Python script here
    # Example command: python my_script.py <input_data>
    data = input_data.split(', ')
    try:
        command = ["python", "populate_dataset.py", "--role", data[0], "--country", data[1], "--sex", data[2]]
        result = subprocess.run(command, capture_output=True, text=True)
        print(result.stdout)
        
        output_text = Markup(helper.proc_text(result.stdout))
        output_image = "example.png" 
    except:
        output_text = "wrong format!"
        output_image = "" 
    # output_text = Markup(helper.give_text())
    # print(output_text)
    # output_text = result.stdout.strip()
    # output_text = """/// NAME\n Sigrun Jonsdottir \n
    #                 /// CODENAME\n Frostbite \n
    #                 /// ROLE\n Sentinel \n
    #                 /// APPEARANCE\n Sigrun is a tall woman with pale skin and icy blue eyes. She has long, white hair that is usually kept in a braid. She wears a white and blue jumpsuit with a hood and a white and blue mask. She also wears a pair of white and blue gloves and boots. \n
    #                 /// BIOGRAPHY\n Sigrun is a native of Iceland, and has always been drawn to the cold and icy environment of her homeland. She was born with the ability to manipulate ice and snow, and has used this power to protect her people from harm. After hearing about the VALORANT Protocol, she decided to join them in order to use her powers to protect the world from the threats posed by Omega Earth. \n
    #                 /// PERSONALITY\n Sigrun is a stoic and determined individual, and is always focused on her mission. She is loyal to her team and will do whatever it takes to protect them. She is also a bit of a loner, preferring to work alone and not get too close to her teammates.\n
    #                 /// ABILITIES:\n
    #                     C - Ice Wall: Sigrun can create a wall of ice that blocks enemy movement and projectiles.\n
    #                     Q - Ice Shards: Sigrun can fire a barrage of ice shards that slow and damage enemies.\n
    #                     E - Ice Trap: Sigrun can place a trap on the ground that freezes enemies in place.\n
    #                     X - Blizzard: Sigrun can create a blizzard that slows and damages enemies in an area.\n
    #                 /// RELATIONSHIPS\n
    #                 Sigrun has a close bond with Brimstone, who she sees as a mentor and guardian figure. She also has a friendly rivalry with Killjoy and Raze, which eventually develops into a romantic relationship."""
    # output_image = "example.png"  # Replace with the path to the output image

    return jsonify({
        "outputText": output_text,
        "outputImage": output_image
    })

if __name__ == "__main__":
    app.run()