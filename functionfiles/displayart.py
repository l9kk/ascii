def display_art(file_path, input_string):
    try:
        with open(file_path, 'r') as file:
            ascii_map = map_file(file_path)

        if not ascii_map:
            print("Error: Character map is empty, please provide a valid char map")
            return "", None

        result = []
        count = 0
        input_string = input_string.replace("\\n", "\n")
        words = input_string.split("\n")

        if not is_printable(input_string):
            return "", None

        for word in words:
            if word == "":
                count += 1
                if count < len(words):
                    result.append("\n")
            else:
                for i in range(8):
                    line = ""
                    for char in word:
                        if char in ascii_map:
                            line += ascii_map[char][i]
                        else:
                            raise ValueError(f"Error: character '{char}' not found in map")
                    result.append(line + "\n")
        return "".join(result), None

    except Exception as e:
        return "", f"Error: {str(e)}"


def map_file(file_path):
    # Assuming a function that loads the map from a file
    # Replace with actual logic to parse the file into a dictionary of ASCII art
    ascii_map = {}
    return ascii_map

def is_printable(text):
    # Implement a check for whether the string is printable
    return True
