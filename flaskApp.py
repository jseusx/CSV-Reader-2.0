from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        serial_number = request.form.get("serial_number")
        # Add logic to process serial number
        return f"Serial Number Submitted: {serial_number}"
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)