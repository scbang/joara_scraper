def is_normal_dialog(line):
    return line.startswith('“') \
           or line.startswith('"') \
           or line.startswith('[') \
           or line.startswith('<') \
           or line.startswith("* * *") \
           or line.startswith('-')


def is_dialog(line):
    return is_normal_dialog(line) or is_past_dialog(line)


def is_past_dialog(line):
    return line.startswith('《')


def is_title(line):
    return line.startswith('#')


def reformat_text(input_file_path="./input.txt", output_file_path="./output.txt"):
    input_lines = []
    input_f = open(input_file_path, 'r')
    while True:
        line = input_f.readline()
        if not line:
            break
        input_lines.append(line)
    input_f.close()

    output_lines = []

    prev_text_mode = "separation"
    text_mode = "separation"
    for input_line in input_lines:
        if input_line == "\n":
            text_mode = "separation"
            continue
        input_line = input_line.lstrip()
        if text_mode == "separation":
            if is_title(input_line):
                if prev_text_mode != "separation":
                    output_lines.append("\n")
                output_lines.append(input_line)
                prev_text_mode = text_mode
                text_mode = "title"
            elif input_line.startswith("* * *"):
                output_lines.append("\n")
                output_lines.append("\n")
                output_lines.append("\n")
                output_lines.append(input_line)
                output_lines.append("\n")
                output_lines.append("\n")
                output_lines.append("\n")
                prev_text_mode = "separation"
            elif is_dialog(input_line):
                output_lines.append("\n")
                output_lines.append("\n")
                output_lines.append("\n")
                output_lines.append(input_line)
                prev_text_mode = text_mode
                text_mode = "normal_dialog" if is_normal_dialog(input_line) else "past_dialog"
            else:
                if prev_text_mode in ["normal", "normal_dialog", "past_dialog"]:
                    output_lines.append("\n")
                    output_lines.append("\n")
                    output_lines.append("\n")
                    output_lines.append("*\n")
                    output_lines.append("\n")
                    output_lines.append("\n")
                    output_lines.append("\n")
                output_lines.append(input_line)
                prev_text_mode = text_mode
                text_mode = "normal"
            continue
        elif text_mode == "title":
            if is_dialog(input_line):  # turn into dialog mode
                prev_text_mode = text_mode
                text_mode = "normal_dialog" if is_normal_dialog(input_line) else "past_dialog"
            else:
                prev_text_mode = text_mode
                text_mode = "normal"
        elif text_mode == "normal":
            if is_dialog(input_line):  # turn into dialog mode
                output_lines.append("\n")
                output_lines.append("\n")
                output_lines.append("\n")
                prev_text_mode = text_mode
                text_mode = "normal_dialog" if is_normal_dialog(input_line) else "past_dialog"
            else:  # stay in normal mode
                output_lines.append("\n")
        elif text_mode == "normal_dialog":
            if not is_normal_dialog(input_line):  # turn into normal mode
                output_lines.append("\n")
                output_lines.append("\n")
                output_lines.append("\n")
                prev_text_mode = text_mode
                text_mode = "normal" if not is_past_dialog(input_line) else "past_dialog"
        elif text_mode == "past_dialog":
            if not is_past_dialog(input_line):  # turn into normal mode
                output_lines.append("\n")
                output_lines.append("\n")
                output_lines.append("\n")
                prev_text_mode = text_mode
                text_mode = "normal" if not is_normal_dialog(input_line) else "normal_dialog"
        output_lines.append(input_line)

    output_f = open(output_file_path, 'w+')
    for output_line in output_lines:
        output_f.write(output_line)
    output_f.close()
