from flask import Flask, redirect, request, session, render_template, make_response

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Required for session tracking

# Define the flag and split it into characters
flag = "WHH{Ke3P-mov1ng}"
flag_chars = list(flag)

@app.route("/", methods=["GET", "POST"])
def login():
    """Serves a login page before redirection starts."""
    if request.method == "POST":
        session.clear()  # Reset any existing session
        session["progress"] = 0
        session.modified = True  # Ensure session updates persist
        return redirect(f"/{flag_chars[0]}", code=302)  # Start the redirection challenge
    return render_template("login.html")

@app.route("/<char>")
def redirect_loop(char):
    """Handles redirection through the flag characters one by one."""
    if "progress" not in session or not isinstance(session["progress"], int):
        return redirect("/")  # Restart if session is missing or invalid

    expected_char = flag_chars[session["progress"]]
    
    if char == expected_char:
        session["progress"] += 1
        session.modified = True  # Ensure session updates persist

        if session["progress"] >= len(flag_chars):
            response = make_response("Done")
            response.headers["X-Flag"] = flag  # Flag is now visible in the Network tab headers
            return response

        return redirect(f"/{flag_chars[session['progress']]}", code=302)  # Redirect to next character
    
    return redirect("/")  # Restart if incorrect

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
