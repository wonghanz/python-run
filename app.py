# This is the server-side script that runs the Python code and returns the results
# It uses Flask as the web framework and CPython as the Python interpreter

from flask import Flask, request, jsonify
import sys
import io
import contextlib

app = Flask(__name__)

@app.route("/run", methods=["POST"])
def run():
    # Get the Python code from the request data
    code = request.get_data().decode("utf-8")

    # Redirect the standard output and error to a string buffer
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        with contextlib.redirect_stderr(buffer):
            try:
                # Execute the Python code in a new namespace
                exec(code, {})
            except Exception as e:
                # Print the exception if any
                print(e, file=sys.stderr)

    # Get the output and error from the buffer
    output = buffer.getvalue()

    # Return the output and error as a JSON response
    return jsonify(output=output)

if __name__ == "__main__":
    app.run(debug=True)
