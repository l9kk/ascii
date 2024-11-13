import os
import sys

def main():
    if len(sys.argv) == 1:
        print("Missing input string!")
        return

    arg_str = sys.argv[1]
    style_banner = ""
    align = ""
    third_banner = False
    width = 0

    if len(arg_str) >= 8 and arg_str.startswith("--"):
        if arg_str.startswith("--align="):
            width = get_terminal_size()
            align = arg_str[8:].lower()
            if align == "":
                print("Missing alignment option!")
                return
            elif align not in ["left", "right", "center", "justify"]:
                print("Invalid alignment option! Choose from right, left, center, or justify.")
                return
            arg_str = sys.argv[2]
            third_banner = True
        else:
            print("Invalid flag. Only --align= is supported.")
            return

    if len(sys.argv) == 2:
        style_banner = "standard"
    elif len(sys.argv) == 3:
        style_banner = "standard" if third_banner else sys.argv[2].lower()
    elif len(sys.argv) == 4:
        style_banner = sys.argv[3].lower()
    else:
        print("Usage: python main.py [options] [string] [font]")
        print("Example: python main.py \"test\" standard")
        print("Options: --align=")
        return

    sep_args = arg_str.split("\\n")

    try:
        with open(f"{style_banner}.txt", 'r') as f:
            lines = f.read().split("\n")
    except FileNotFoundError:
        print(f"Font '{style_banner}' does not exist.")
        return

    with open('result.txt', 'w') as output_file:
        if align:
            print_ascii_art_align(sep_args, lines, align, width, output_file)
        else:
            print_ascii_art(sep_args, lines, output_file)

def get_terminal_size():
    try:
        rows, columns = os.popen('stty size', 'r').read().split()
        return int(columns)
    except ValueError:
        return 80

def print_ascii_art_align(sentences, text_file, position, w, output_file):
    for word in sentences:
        if not word:
            output_file.write("\n")
            continue

        word_count = word.count(' ') + 1
        word_len = sum(len(text_file[(ord(char) - 32) * 9 + 2]) for char in word)

        spaces_for_justify = (w - word_len) // word_count if word_count > 1 else (w - word_len)
        spaces = w // 2 - word_len // 2

        for h in range(1, 9):
            if position == "center":
                output_file.write(" " * spaces)
            elif position == "right":
                output_file.write(" " * (spaces * 2))

            for char in word:
                line_index = (ord(char) - 32) * 9 + h
                if 0 <= line_index < len(text_file):
                    line = text_file[line_index]
                    if position == "justify" and char == ' ':
                        output_file.write(line + " " * spaces_for_justify)
                    else:
                        output_file.write(line)
            output_file.write("\n")

def print_ascii_art(sentences, text_file, output_file):
    for word in sentences:
        if not word:
            output_file.write("\n")
            continue

        for h in range(1, 9):
            for char in word:
                line_index = (ord(char) - 32) * 9 + h
                if 0 <= line_index < len(text_file):
                    output_file.write(text_file[line_index])
            output_file.write("\n")

if __name__ == "__main__":
    main()
