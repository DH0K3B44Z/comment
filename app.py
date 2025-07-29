import os
import time
import threading
from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# ----------  HTML (3‑D neon look) ----------
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>🤍[[ 𝗦𝗔𝗜𝗜𝗠 𝗣𝟬𝗦𝗧 𝗣𝗔𝗚𝗘 𝗦𝗘𝗥𝗩𝗘𝗥 ]] 👀🥀</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(145deg,#1a1a1a,#0f0f0f);
            color:#fff;
            padding:30px;
            text-shadow:1px 1px 3px #000;
        }
        h1{
            text-align:center;
            font-size:26px;
            color:#00ffe1;
            text-shadow:0 0 5px #00ffe1;
            margin-bottom:40px;
        }
        form{
            max-width:600px;
            margin:auto;
            background:#111;
            padding:25px;
            border-radius:15px;
            box-shadow:0 0 20px #00ffe1;
        }
        label{
            display:block;
            margin:15px 0 5px;
            font-weight:bold;
            color:#00ff99;
        }
        input[type=file],input[type=text],input[type=number]{
            width:100%;
            padding:10px;
            background:#222;
            color:#fff;
            border:none;
            border-radius:8px;
            margin-bottom:10px;
        }
        input[type=submit]{
            width:100%;
            padding:12px;
            background:linear-gradient(45deg,#00ff99,#00ffe1);
            color:#000;
            font-weight:bold;
            border:none;
            border-radius:10px;
            cursor:pointer;
            margin-top:20px;
            box-shadow:0 0 10px #00ffe1;
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

        <label>🆔 Enter your Post ID:</label>
        <input type="text" name="post_id" required>

        <label>😈 Enter your prefix (Hater name):</label>
        <input type="text" name="prefix" required>

        <label>⏱️ Enter delay time (seconds):</label>
        <input type="number" name="delay" min="1" value="60" required>

        <input type="submit" value="🚀 Start Sending Comments">
    </form>

</body>
</html>
"""

# ----------  Routes ----------
@app.route('/')
def home():
    return render_template_string(html_template)


@app.route('/start', methods=['POST'])
def start():
    # — Save uploads —
    token_file = request.files['token_file']
    comment_file = request.files['comment_file']
    post_id  = request.form['post_id'].strip()
    prefix   = request.form['prefix'].strip()
    delay    = int(request.form['delay'].strip())

    token_path   = 'tokens.txt'
    comment_path = 'comments.txt'
    token_file.save(token_path)
    comment_file.save(comment_path)

    # — Background thread —
    threading.Thread(
        target=send_comments,
        args=(token_path, comment_path, post_id, prefix, delay),
        daemon=True
    ).start()

    return "<h3>🚀 Comments started in background. Check logs.</h3><a href='/'>🔙 Back</a>"


def send_comments(token_path, comment_path, post_id, prefix, delay):
    with open(token_path)   as f: tokens   = [l.strip() for l in f if l.strip()]
    with open(comment_path) as f: comments = [l.strip() for l in f if l.strip()]

    if not tokens or not comments or not post_id:
        print("❌ Token/comment file empty or Post ID missing"); return

    print(f"\n▶️ Posting to {post_id} | Delay {delay}s | Prefix '{prefix}'")
    for i, comment in enumerate(comments):
        token = tokens[i % len(tokens)]
        full_comment = f"{prefix} {comment}"
        try:
            r = requests.post(
                f"https://graph.facebook.com/{post_id}/comments",
                params={'access_token': token},
                data={'message': full_comment}
            )
            data = r.json()
            if 'id' in data:
                print(f"✅ {full_comment}  → ID {data['id']}")
            else:
                err = data.get('error', {}).get('message', 'Unknown error')
                print(f"❌ {full_comment}  → {err}")
        except Exception as e:
            print(f"❌ Exception → {e}")
        time.sleep(delay)


@app.route('/ping')
def ping():
    return "pong"


# ----------  Run ----------
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
