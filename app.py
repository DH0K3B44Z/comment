from flask import Flask, request, render_template_string
import time
import os

app = Flask(__name__)

# 🔐 Read token
def get_token():
    try:
        with open("token.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "NO_TOKEN_FOUND"

# 💬 Load comment lines
def load_comments():
    try:
        with open("comment.txt", "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return ["No comments found."]

# 🏠 Home form
@app.route('/')
def form():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>🔥 Auto Comment Bot</title>
        <style>
            body { font-family: sans-serif; background-color: #f0f2f5; padding: 30px; }
            .container {
                max-width: 600px; background: white; padding: 20px;
                margin: auto; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }
            input, select, textarea {
                width: 100%; padding: 10px; margin: 10px 0; border-radius: 5px; border: 1px solid #ccc;
            }
            button {
                background-color: #1877f2; color: white; padding: 10px 20px;
                border: none; border-radius: 5px; font-size: 16px; cursor: pointer;
            }
            button:hover { background-color: #145ecb; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>🔥 Facebook Auto Comment Bot</h2>
            <form action="/post" method="post" enctype="multipart/form-data">
                <label>📌 Post ID:</label>
                <input type="text" name="post_id" required>

                <label>😈 Haters Name (Prefix):</label>
                <input type="text" name="hatersname" placeholder="e.g. Hater99">

                <label>🦸 Hero Name (Suffix):</label>
                <input type="text" name="heroname" placeholder="e.g. LegendX">

                <label>⏱️ Delay Between Comments (seconds):</label>
                <input type="number" name="delay" value="5" min="1">

                <label>🔐 Choose Token File:</label>
                <input type="file" name="token_file" accept=".txt">

                <label>💬 Choose Comments File:</label>
                <input type="file" name="comment_file" accept=".txt">

                <button type="submit">🚀 Start Posting</button>
            </form>
        </div>
    </body>
    </html>
    ''')

# 📤 Comment posting simulation
@app.route('/post', methods=['POST'])
def post():
    post_id = request.form['post_id']
    hatersname = request.form['hatersname'].strip()
    heroname = request.form['heroname'].strip()
    delay = int(request.form.get('delay', 5))

    # 📁 Handle uploaded token file
    token_file = request.files.get("token_file")
    if token_file and token_file.filename.endswith(".txt"):
        token_file.save("token.txt")

    # 📁 Handle uploaded comment file
    comment_file = request.files.get("comment_file")
    if comment_file and comment_file.filename.endswith(".txt"):
        comment_file.save("comment.txt")

    token = get_token()
    comments = load_comments()

    log_output = '''
    <html>
    <head>
        <title>🚀 Posting Comments</title>
        <style>
            body { font-family: monospace; background: #111; color: #0f0; padding: 20px; }
            a { color: #0af; }
        </style>
    </head>
    <body>
    <h2>📡 Comment Log</h2>
    <pre>
    '''

    for idx, comment in enumerate(comments, 1):
        final_comment = f"{hatersname} {comment} {heroname}".strip()
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_output += f"[{timestamp}] [{idx}] Post ID: {post_id} | Token: {token[:5]}*** | Comment: {final_comment}\n"
        time.sleep(delay)

    log_output += "</pre><a href='/'>⬅️ Back to Form</a></body></html>"
    return log_output

# 🔃 Auto file creation
if __name__ == '__main__':
    if not os.path.exists("token.txt"):
        with open("token.txt", "w") as f:
            f.write("123456789:FAKE_TOKEN")

    if not os.path.exists("comment.txt"):
        with open("comment.txt", "w") as f:
            f.write("Nice one!\nYou're wrong!\nFake post!\n")

    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
