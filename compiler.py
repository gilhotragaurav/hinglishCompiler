def hinglish_to_python(code):
    mapping = {
        "bolo": "print",
        "agar": "if",
        "warna": "else",
        "jabtak": "while",
        "ke_liye": "for",
        "input_lo": "input"
    }

    # Normalize line breaks (IMPORTANT)
    code = code.replace("\r\n", "\n").replace("\r", "\n")

    lines = code.split("\n")
    python_code = []

    for line in lines:
        new_line = line  # indentation preserve

        for key, value in mapping.items():
            new_line = new_line.replace(key, value)

        python_code.append(new_line)

    return "\n".join(python_code)