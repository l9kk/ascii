import os
import sys

def main():
    if len(sys.argv) == 1:
        print("")
        return

    arg_str = sys.argv[1]
    style_banner = ""
    output_file = ""
    align = ""
    third_banner = False
    width = 0

    if len(arg_str) >= 8:
        if arg_str[:2] == "--":
            if arg_str[:8] == "--align=" or arg_str[:9] == "--output=":
                pass
            else:
                print("Wrong flag. (--output= or --align=)")
                return

        if arg_str[:8] == "--align=":
            width = get_terminal_size()
            align = arg_str[8:].lower()
            if align == "":
                print("Missing align name!")
                return
            elif align not in ["left", "right", "center", "justify"]:
                print("Wrong align! (right, left, center, justify)")
                return

            arg_str = sys.argv[2]
            third_banner = True
            if "--output=" in sys.argv[2]:
                print("Can not use output flag and align flag same time!")
                return

        elif arg_str[:9] == "--output=":
            output_file = arg_str[9:]
            if output_file == "":
                print("Missing output name!")
                return
            if len(sys.argv) < 3:
                print("Missing string!")
                return

            arg_str = sys.argv[2]
            third_banner = True
            if "--align=" in sys.argv[2]:
                print("Can not use output flag and align flag same time!")
                return

    if len(sys.argv) == 2:
        style_banner = "standard"
    elif len(sys.argv) == 3:
        style_banner = "standard" if third_banner else sys.argv[2].lower()
    elif len(sys.argv) == 4:
        style_banner = sys.argv[3].lower()
    else:
        print("Usage: python main.py [options] [string] [font] || Example: python main.py \"test\" standard || Options: --output=, --align=")
        return

    sep_args = arg_str.split("\\n")

    try:
        with open(f"{style_banner}.txt", 'r') as f:
            lines = f.read().split("\n")
    except FileNotFoundError:
        print(f"{style_banner} banner does not exist.")
        return

    if align:
        print_ascii_art_align(sep_args, lines, align, width)
    elif output_file:
        try:
            with open(output_file, 'w') as created_file:
                print_ascii_art_to_file(sep_args, lines, created_file)
        except IOError:
            print("Something went wrong while creating output file.")
    else:
        print_ascii_art(sep_args, lines)

def get_terminal_size():
    try:
        rows, columns = os.popen('stty size', 'r').read().split()
        return int(columns)
    except ValueError:
        return 80

def print_ascii_art_align(sentences, text_file, position, w):
    for word in sentences:
        if not word:
            print()
            continue

        word_count = word.count(' ') + 1
        word_len = sum(len(text_file[(ord(char) - 32) * 9 + 2]) for char in word)

        spaces_for_justify = (w - word_len) // word_count if word_count > 1 else (w - word_len)
        spaces = w // 2 - word_len // 2

        for h in range(1, 9):
            if position == "center":
                print(" " * spaces, end="")
            elif position == "right":
                print(" " * (spaces * 2), end="")

            for char in word:
                for line_index, line in enumerate(text_file):
                    if line_index == (ord(char) - 32) * 9 + h:
                        if position == "justify" and char == ' ':
                            print(line, end="")
                            print(" " * spaces_for_justify, end="")
                        else:
                            print(line, end="")
                        break

            if position == "center" or position == "left":
                print(" " * spaces, end="")
            print()

def print_ascii_art_to_file(sentences, text_file, to_file):
    for word in sentences:
        if not word:
            to_file.write("\n")
            continue

        for h in range(1, 9):
            for char in word:
                for line_index, line in enumerate(text_file):
                    if line_index == (ord(char) - 32) * 9 + h:
                        to_file.write(line)
                        break
            to_file.write("\n")
    to_file.write("\n")

def print_ascii_art(sentences, text_file):
    for word in sentences:
        if not word:
            print()
            continue

        for h in range(1, 9):
            for char in word:
                for line_index, line in enumerate(text_file):
                    if line_index == (ord(char) - 32) * 9 + h:
                        print(line, end="")
                        break
            print()

if __name__ == "__main__":
    main()
