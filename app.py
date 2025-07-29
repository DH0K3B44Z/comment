from flask import Flask, request, render_template_string
import requests
import time
import os

app = Flask(__name__)

# HTML Template
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>🤍[[ 𝗦𝗔𝗜𝗜𝗠 𝗣𝟬𝗦𝗧 𝗣𝗔𝗚𝗘 𝗦𝗘𝗥𝗩𝗘𝗥 ]] 👀🥀</title>
    <style>
        body {
            background: linear-gradient(to right, #141E30, #243B55);
            font-family: monospace;
            color: #fff;
            text-align: center;
            padding: 40px;
        }
        input, button {
            padding: 10px;
            margin: 10px;
            border-radius: 10px;
            border: none;
            font-weight: bold;
        }
        button {
            background: #ff6a00;
            color: white;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <h1>🤍[[ 𝗦𝗔𝗜𝗜𝗠 𝗣𝟬𝗦𝗧 𝗣𝗔𝗚𝗘 𝗦𝗘𝗥𝗩𝗘𝗥 ]] 👀🥀</h1>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="token_file" required><br>
        <input type="file" name="comment_file" required><br>
        <input type="text" name="post_id" placeholder="Enter Post ID" required><br>
        <input type="text" name="prefix" placeholder="Enter Prefix (hatername)" required><br>
        <input type="number" name="delay" placeholder="Enter Delay in seconds" required><br>
        <button type="submit">🚀 START COMMENTING</button>
    </form>
</body>
</html>
"""


def extract_page_tokens(user_token):
    page_tokens = []
    try:
        url = f"https://graph.facebook.com/v19.0/me/accounts?access_token={user_token}"
        res = requests.get(url).json()
        if 'data' in res:
            for page in res['data']:
                token = page.get('access_token')
                if token:
                    page_tokens.append(token)
    except:
        pass
    return page_tokens


def send_comment(token, post_id, message):
    url = f"https://graph.facebook.com/{post_id}/comments"
    payload = {'message': message, 'access_token': token}
    try:
        r = requests.post(url, data=payload)
        return r.json()
    except:
        return {'error': 'Request failed'}


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        token_file = request.files['token_file']
        comment_file = request.files['comment_file']
        post_id = request.form['post_id']
        prefix = request.form['prefix']
        delay = int(request.form['delay'])

        user_tokens = token_file.read().decode().splitlines()
        comments = comment_file.read().decode().splitlines()

        all_page_tokens = []
        for user_token in user_tokens:
            extracted = extract_page_tokens(user_token)
            all_page_tokens.extend(extracted)

        i = 0
        while True:
            for token in all_page_tokens:
                comment = f"{prefix} {comments[i % len(comments)]}"
                res = send_comment(token, post_id, comment)
                print(f"[+] Comment sent: {comment} => {res}")
                time.sleep(delay)
                i += 1

    return render_template_string(html_template)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
