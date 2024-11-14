import os
import sys

ANSI_COLORS = {
    "black": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "reset": "\033[0m",
}


def main():
    if len(sys.argv) == 1:
        print("")
        return

    args = sys.argv[1:]
    style_banner = ""
    output_file = ""
    align = ""
    color = ""
    letters_to_color = ""
    width = 0

    index = 0
    while index < len(args):
        arg = args[index]
        if arg.startswith("--"):
            if arg.startswith("--align="):
                align = arg[len("--align=") :].lower()
                if align == "":
                    print("Missing align name!")
                    return
                elif align not in ["left", "right", "center", "justify"]:
                    print("Wrong align! (right, left, center, justify)")
                    return
                index += 1
            elif arg.startswith("--output="):
                output_file = arg[len("--output=") :]
                if output_file == "":
                    print("Missing output name!")
                    return
                index += 1
            elif arg.startswith("--color="):
                color = arg[len("--color=") :].lower()
                if color == "":
                    print("Missing color name!")
                    return
                if color not in ANSI_COLORS:
                    print(
                        f"Invalid color '{color}'. Available colors: {', '.join(ANSI_COLORS.keys())}"
                    )
                    return
                index += 1

                if index + 1 < len(args) and not args[index].startswith("--"):
                    letters_to_color = args[index]
                    index += 1

            else:
                print(
                    'Usage: python main.py [options] [string] [font] || Example: python main.py "test" standard || Options: --output=, --align=, --color='
                )
                return
        else:
            break

    remaining_args = args[index:]
    if not remaining_args:
        print("Missing string!")
        return
    arg_str = remaining_args[0]
    if len(remaining_args) >= 2:
        style_banner = remaining_args[1].lower()
    else:
        style_banner = "standard"

    sep_args = arg_str.split("\\n")

    try:
        with open(f"{style_banner}.txt", "r") as f:
            lines = f.read().split("\n")
    except FileNotFoundError:
        print(f"{style_banner} banner does not exist.")
        return

    if align:
        width = get_terminal_size()
        if output_file:
            try:
                with open(output_file, "w", encoding="utf-8") as created_file:
                    print_ascii_art_align(
                        sep_args,
                        lines,
                        align,
                        width,
                        created_file,
                        color,
                        letters_to_color,
                    )
            except IOError:
                print("Something went wrong while creating output file.")
        else:
            print_ascii_art_align(
                sep_args, lines, align, width, None, color, letters_to_color
            )
    else:
        if output_file:
            try:
                with open(output_file, "w", encoding="utf-8") as created_file:
                    print_ascii_art_to_file(
                        sep_args, lines, created_file, color, letters_to_color
                    )
            except IOError:
                print("Something went wrong while creating output file.")
        else:
            print_ascii_art(sep_args, lines, color, letters_to_color)


def get_terminal_size():
    try:
        rows, columns = os.popen("stty size", "r").read().split()
        return int(columns)
    except ValueError:
        return 80


def print_ascii_art_align(
    sentences, text_file, position, w, output_file, color, letters_to_color
):
    for word in sentences:
        if not word:
            if output_file:
                output_file.write("\n")
            else:
                print()
            continue

        word_count = word.count(" ") + 1
        word_len = sum(len(text_file[(ord(char) - 32) * 9 + 2]) for char in word)

        spaces_for_justify = (
            (w - word_len) // word_count if word_count > 1 else (w - word_len)
        )
        spaces = w // 2 - word_len // 2

        for h in range(1, 9):
            line_output = ""
            if position == "center":
                line_output += " " * spaces
            elif position == "right":
                line_output += " " * (spaces * 2)

            for char in word:
                if char == " ":
                    line_output += " " * 8
                else:
                    line_index = (ord(char) - 32) * 9 + h
                    if 0 <= line_index < len(text_file):
                        line = text_file[line_index]
                        if color and (not letters_to_color or char in letters_to_color):
                            line = (
                                    ANSI_COLORS[color]
                                    + line
                                    + ANSI_COLORS["reset"]
                            )
                        line_output += line
            if position == "center" or position == "left":
                line_output += " " * spaces

            if output_file:
                output_file.write(line_output + "\n")
            else:
                print(line_output)


def print_ascii_art_to_file(sentences, text_file, to_file, color, letters_to_color):
    for word in sentences:
        if not word:
            to_file.write("\n")
            continue

        for h in range(1, 9):
            line_output = ""
            for char in word:
                if char == " ":
                    line_output += " " * 8
                else:
                    line_index = (ord(char) - 32) * 9 + h
                    if 0 <= line_index < len(text_file):
                        line = text_file[line_index]
                        if color and (not letters_to_color or char in letters_to_color):
                            line = (
                                    ANSI_COLORS[color]
                                    + line
                                    + ANSI_COLORS["reset"]
                            )
                        line_output += line
            to_file.write(line_output + "\n")
    to_file.write("\n")


def print_ascii_art(sentences, text_file, color, letters_to_color):
    for word in sentences:
        if not word:
            print()
            continue

        for h in range(1, 9):
            line_output = ""
            for char in word:
                if char == " ":
                    line_output += " " * 8
                else:
                    line_index = (ord(char) - 32) * 9 + h
                    if 0 <= line_index < len(text_file):
                        line = text_file[line_index]
                        if color and (not letters_to_color or char in letters_to_color):
                            line = (
                                    ANSI_COLORS[color]
                                    + line
                                    + ANSI_COLORS["reset"]
                            )
                        line_output += line
            print(line_output)


if __name__ == "__main__":
    main()
