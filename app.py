from flask import Flask, redirect, request, make_response

app = Flask(__name__)

# Define the flag and split it into characters
flag = "WHH{Ke3P-mov1ng}"  # Your challenge flag
flag_chars = list(flag)

@app.route("/")
def start_redirect():
    """Initiates the redirection loop using cookies."""
    resp = make_response(redirect(f"/{flag_chars[0]}", code=302))
    resp.set_cookie("progress", "0")  # Start from the first character
    return resp

@app.route("/<char>")
def redirect_loop(char):
    """Handles redirection through the flag characters using cookies."""
    progress = request.cookies.get("progress", "0")  # Retrieve progress from cookies

    try:
        progress = int(progress)
    except ValueError:
        return redirect("/")  # Reset if cookie is corrupted

    if progress >= len(flag_chars):
        return "The page isn’t redirecting properly", 400  # Simulate infinite loop detection

    expected_char = flag_chars[progress]

    if char == expected_char:
        progress += 1  # Move to the next character
        resp = make_response(
            redirect(f"/{flag_chars[progress]}", code=302) if progress < len(flag_chars) else "Done"
        )
        resp.set_cookie("progress", str(progress))  # Store updated progress in the cookie
        return resp

    return redirect("/")  # Restart if incorrect

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
