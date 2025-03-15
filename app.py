from flask import Flask, redirect, request, session

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Required for session tracking

# Define the flag and split it into characters
flag = "WHH{Ke3P-mov1ng}"  # Change to match the new challenge theme
flag_chars = list(flag)

@app.route("/")
def start_redirect():
    """Initiates the redirection loop."""
    session["progress"] = 0
    return redirect(f"/{flag_chars[0]}", code=302)

@app.route("/<char>")
def redirect_loop(char):
    """Handles redirection through the flag characters one by one."""
    if "progress" not in session:
        return redirect("/")  # Reset progress if accessed incorrectly

    expected_char = flag_chars[session["progress"]]
    
    if char == expected_char:
        session["progress"] += 1
        
        if session["progress"] >= len(flag_chars):
            return "The page isn’t redirecting properly", 400  # Simulating infinite redirection issue
        
        return redirect(f"/{flag_chars[session['progress']]}", code=302)  # Redirect to next character
    
    return redirect("/")  # Restart if incorrect

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
