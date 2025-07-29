import os
import time
import threading
from flask import Flask, request, render_template_string, redirect
import requests

app = Flask(__name__)

html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>🤍[[ 𝗦𝗔𝗜𝗜𝗠 𝗣𝟬𝗦𝗧 𝗣𝗔𝗚𝗘 𝗦𝗘𝗥𝗩𝗘𝗥 ]] 👀🥀</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(145deg, #1a1a1a, #0f0f0f);
            color: white;
            padding: 30px;
            text-shadow: 1px 1px 3px black;
        }
        h1 {
            text-align: center;
            font-size: 26px;
            color: #00ffe1;
            text-shadow: 0 0 5px #00ffe1;
            margin-bottom: 40px;
        }
        form {
            max-width: 600px;
            margin: auto;
            background: #111;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 0 20px #00ffe1;
        }
        label {
            display: block;
            margin-top: 15px;
            margin-bottom: 5px;
            font-weight: bold;
            color: #00ff99;
        }
        input[type="file"], input[type="text"], input[type="number"] {
            width: 100%;
            padding: 10px;
            background: #222;
            color: #fff;
            border: none;
            border-radius: 8px;
            margin-bottom: 10px;
        }
        input[type="submit"] {
            width: 100%;
            padding: 12px;
            background: linear-gradient(45deg, #00ff99, #00ffe1);
            color: #000;
            font-weight: bold;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            margin-top: 20px;
            box-shadow: 0 0 10px #00ffe1;
        }
    </style>
</head>
<body>

    <h1>🤍[[ 𝗦𝗔𝗜𝗜𝗠 𝗣𝟬𝗦𝗧 𝗣𝗔𝗚𝗘 𝗦𝗘𝗥𝗩𝗘𝗥 ]] 👀🥀</h1>

    <form method="POST" action="/start" enctype="multipart/form-data">
        <label>🔑 Choose your access token.txt:</label>
        <input type="file" name="token_file" required>

        <label>💬 Choose your comment.txt:</label>
        <input type="file" name="comment_file" required>

        <label>🆔 Enter your Post ID:</label>
        <input type="text" name="post_id" required>

        <label>😈 Enter your prefix (Hater name):</label>
        <input type="text" name="prefix" required>

        <label>⏱️ Enter delay time (in seconds):</label>
        <input type="number" name="delay" min="1" value="60" required>

        <input type="submit" value="🚀 Start Sending Comments">
    </form>

</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_template)

@app.route('/start', methods=['POST'])
def start():
    # Save uploaded files
    token_file = request.files['token_file']
    comment_file = request.files['comment_file']
    post_id = request.form['post_id'].strip()
    prefix = request.form['prefix'].strip()
    delay = int(request.form['delay'].strip())

    token_path = "tokens.txt"
    comment_path = "comments.txt"
    post_id_path = "post_id.txt"

    token_file.save(token_path)
    comment_file.save(comment_path)
    with open(post_id_path, 'w') as f:
        f.write(post_id)

    # Start background comment thread
    threading.Thread(target=send_comments, args=(token_path, comment_path, post_id, prefix, delay)).start()
    return "<h3>🚀 Comments started in background with 3D UI. Check console logs.</h3><a href='/'>🔙 Back</a>"

def send_comments(token_file, comment_file, post_id, prefix, delay):
    with open(token_file, 'r') as f:
        tokens = [line.strip() for line in f if line.strip()]

    with open(comment_file, 'r') as f:
        comments = [line.strip() for line in f if line.strip()]

    if not tokens or not comments or not post_id:
        print("❌ Empty token, comment, or post ID.")
        return

    print(f"\n🚀 Starting comments to post ID: {post_id}")
    for index, comment in enumerate(comments):
        token = tokens[index % len(tokens)]
        full_comment = f"{prefix} {comment}"
        try:
            response = requests.post(
                f"https://graph.facebook.com/{post_id}/comments",
                params={"access_token": token},
                data={"message": full_comment}
            )
            data = response.json()
            if "id" in data:
                print(f"✅ Sent: {full_comment} → ID: {data['id']}")
            else:
                error_msg = data.get('error', {}).get('message', 'Unknown error')
                print(f"❌ Failed: {full_comment} → {error_msg}")
        except Exception as e:
            print(f"❌ Exception: {full_comment} → {e}")
        time.sleep(delay)

@app.route('/ping')
def ping():
    return "pong"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
