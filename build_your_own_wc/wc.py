import sys

def count_bytes(file_content):
    return len(file_content.encode('utf-8'))

def count_words(file_content):
    return len(file_content.split())

def count_chars(file_content):
    return len(file_content)

def count_lines(file_content):
    return file_content.count("\n")

def read_file_or_stdin(filename=None):
    if filename:
        with open(filename,"r",encoding="utf-8") as file:
            return file.read()
    else:
        return sys.stdin.read()

def ccwc(args):
    if len(args) < 2:
        print("Usage: wc [options] [file]")
        print("Options:")
        print("  -c    Count bytes")
        print("  -l    Count lines")
        print("  -w    Count words")
        print("  -m    Count characters")
        sys.exit(1)

    options = {"-c": count_bytes, "-l": count_lines, "-w": count_words, "-m": count_chars}
    option_flags = [arg for arg in args[1:] if arg.startswith("-")]
    filenames = [arg for arg in args[1:] if not arg.startswith("-")]
    if not filenames:
        filenames = [None]
    results = []
    for filename in filenames:
        file_content = read_file_or_stdin(filename)
        output = []
        if not option_flags:
            option_flags = ["-l", "-w", "-c"]
        for flag in option_flags:
            if flag in options:
                count = options[flag](file_content)
                output.append(f"{count}")
            else:
                print(f"Invalid option: {flag}")
                sys.exit(1)
        results.append(f"{'   '.join(output)} {filename or '(stdin)'}")

    return "\n".join(results)



if __name__ == "__main__":
    output = ccwc(sys.argv)
    print(output)