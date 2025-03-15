from flask import Flask, redirect, request, session, render_template

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Required for session tracking

# Define the flag and split it into characters
flag = "RITSEC{Redirection_Fun}"  # Change to match the new challenge theme
flag_chars = list(flag)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Serves a login page before redirection starts."""
    if request.method == "POST":
        return redirect("/start")  # Guide users towards the redirection challenge
    return render_template("login.html")

@app.route("/start")
def start_redirect():
    """Initiates the redirection loop."""
    session.clear()  # Ensure session starts fresh
    session["progress"] = 0
    session.modified = True  # Ensure session updates persist
    return redirect(f"/{flag_chars[0]}", code=302)

@app.route("/<char>")
def redirect_loop(char):
    """Handles redirection through the flag characters one by one."""
    if "progress" not in session or not isinstance(session["progress"], int):
        return redirect("/start")  # Reset progress if session is missing or invalid

    expected_char = flag_chars[session["progress"]]
    
    if char == expected_char:
        session["progress"] += 1
        session.modified = True  # Ensure session updates persist
        
        if session["progress"] >= len(flag_chars):
            return f"Congratulations! Your flag is: {flag}"  # Display the flag instead of error
        
        return redirect(f"/{flag_chars[session['progress']]}", code=302)  # Redirect to next character
    
    return redirect("/start")  # Restart if incorrect

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
