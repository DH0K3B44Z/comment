from flask import Flask, request, render_template_string
import requests
import threading
import time
import os
import random

app = Flask(__name__)
running = False

html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>🤍[[ 𝗦𝗔𝗜𝗜𝗠 𝗣𝟬𝗦𝗧 𝗣𝗔𝗚𝗘 𝗦𝗘𝗥𝗩𝗘𝗥 ]] 👀🥀</title>
    <style>
        body {
            font-family: monospace;
            background: linear-gradient(135deg, #010101, #1a1a1a);
            color: #00ffee;
            padding: 30px;
        }
        h2 {
            font-size: 28px;
            color: #ffffff;
            text-shadow: 0 0 10px #0ff;
        }
        input, textarea {
            width: 100%;
            padding: 8px;
            margin: 8px 0;
            background: #0e0e0e;
            color: #0ff;
            border: 1px solid #0ff;
            border-radius: 5px;
        }
        input[type="submit"] {
            background: #0ff;
            color: #000;
            font-weight: bold;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <h2>🤍[[ 𝗦𝗔𝗜𝗜𝗠 𝗣𝟬𝗦𝗧 𝗣𝗔𝗚𝗘 𝗦𝗘𝗥𝗩𝗘𝗥 ]] 👀🥀</h2>
    <form action="/" method="post" enctype="multipart/form-data">
        <label>Choose access_token.txt:</label>
        <input type="file" name="token_file" required><br>
        <label>Choose comment.txt:</label>
        <input type="file" name="comment_file" required><br>
        <label>Enter Post ID:</label>
        <input type="text" name="post_id" required><br>
        <label>Enter prefix (hatername):</label>
        <input type="text" name="prefix"><br>
        <label>Enter time delay (in seconds):</label>
        <input type="number" name="delay" required><br>
        <input type="submit" value="Start Commenting">
    </form>
</body>
</html>
"""

def post_comment(token, post_id, message):
    url = f"https://graph.facebook.com/{post_id}/comments"
    payload = {
        "message": message,
        "access_token": token
    }
    try:
        r = requests.post(url, data=payload)
        if r.status_code == 200:
            print(f"\033[92m[✅ Sent] → {message}\033[0m")
        else:
            print(f"\033[91m[❌ Failed] → {message}\033[0m")
    except Exception as e:
        print(f"\033[91m[⚠ Error] {str(e)}\033[0m")

def start_commenting(tokens, comments, post_id, prefix, delay):
    global running
    running = True
    while running:
        for token in tokens:
            comment = random.choice(comments)
            final_comment = f"{prefix} {comment}" if prefix else comment
            post_comment(token.strip(), post_id, final_comment)
            time.sleep(delay)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        token_file = request.files["token_file"]
        comment_file = request.files["comment_file"]
        post_id = request.form["post_id"]
        prefix = request.form["prefix"]
        delay = int(request.form["delay"])

        tokens = token_file.read().decode("utf-8").strip().splitlines()
        comments = comment_file.read().decode("utf-8").strip().splitlines()

        t = threading.Thread(target=start_commenting, args=(tokens, comments, post_id, prefix, delay))
        t.daemon = True
        t.start()

        return "<h2 style='color:lime;'>✅ Commenting Started... Check logs for updates!</h2>"

    return render_template_string(html_template)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
