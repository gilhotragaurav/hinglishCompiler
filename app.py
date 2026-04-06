from flask import Flask, render_template, request
from compiler import hinglish_to_python
import io
import sys
import traceback
from parser import simple_parser

app = Flask(__name__)   

@app.route("/", methods=["GET"])
def home():
    hinglish_code = request.args.get("code", "")
    return render_template("index.html", hinglish_code=hinglish_code)


@app.route("/result", methods=["POST"])
def result():
    hinglish_code = request.form["code"]
    python_code = hinglish_to_python(hinglish_code)

    output = ""

    parse_errors = simple_parser(hinglish_code)

    if parse_errors:
        output = "❌ Syntax Errors:\n\n" + "\n".join(parse_errors)
        return render_template(
            "result.html",
            python_code=python_code,
            output=output,
            hinglish_code=hinglish_code
        )

    try:
        # INPUT SUPPORT
        user_input = request.form.get("user_input", "")
        input_values = user_input.split(",")

        def mock_input(prompt=""):
            return input_values.pop(0) if input_values else ""

        # CAPTURE OUTPUT
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()

        exec(python_code, {"input": mock_input})

        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

    except Exception as e:
        sys.stdout = old_stdout

        error_type = type(e).__name__
        error_msg = str(e)

        line_no = getattr(e, 'lineno', None)

        if line_no is None:
            tb = traceback.extract_tb(e.__traceback__)
            line_no = tb[-1].lineno if tb else 0
        hinglish_lines = hinglish_code.split("\n")
        if line_no <= len(hinglish_lines):
            hinglish_line = line_no
        else:
            hinglish_line = f"Approx {line_no}"

        #  PRIORITY: REAL ERRORS FIRST
        if error_type in ["IndentationError", "SyntaxError"]:
            output = f"""❌ {error_type}\n
            📍 Line: {line_no}\n
            💡 {error_msg}"""

        else:
            #  CUSTOM SUGGESTIONS
            lines = hinglish_code.split("\n")
            suggestions = []

            for i, line in enumerate(lines, start=1):

                if "likho" in line:
                    suggestions.append(f"Line {i}: 'likho' use kiya hai → 'bolo' use karo")

                if "bolo(" in line:
                    inside = line.split("bolo(")[1].rstrip(")")
                    if '"' not in inside and "'" not in inside:
                        suggestions.append(f"Line {i}: Text ko \" \" me likho")

                if "hai toh" in line:
                    suggestions.append(f"Line {i}: 'hai toh' ki jagah ':' use karo")

            if suggestions:
                output = "❌ Error detected\n\n" + "\n".join(suggestions)
            else:
                output = f"❌ {error_type}\n📍 Line: {line_no}\n💡 {error_msg}"

    return render_template(
        "result.html",
        python_code=python_code,
        output=output,
        hinglish_code=hinglish_code
    )


if __name__ == "__main__":
    app.run(debug=True)