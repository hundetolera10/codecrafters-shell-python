import sys
import os
import subprocess


BUILTIN_COMMANDS = ["type", "echo", "exit"]
PATH_DIRECTORIES = os.environ.get("PATH", "").split(os.pathsep)


def is_executable(file_path):
    return os.access(file_path, os.X_OK)


def is_file(file_path):
    return os.path.isfile(file_path)


def get_file_path(command):
    for directory in PATH_DIRECTORIES:
        file_path = os.path.join(directory, command)

        if is_file(file_path) and is_executable(file_path):
            return file_path

    return None


def print_command_type(command):
    if command in BUILTIN_COMMANDS:
        print(f"{command} is a shell builtin")
    else:
        file_path = get_file_path(command)

        if file_path is not None:
            print(f"{command} is {file_path}")
        else:
            print(f"{command}: not found")


def main():
    while True:
        sys.stdout.write("$ ")

        user_input = input()
        parts = user_input.split()

        if not parts:
            continue

        command = parts[0]
        arguments = parts[1:]

        if command == "exit":
            break

        elif command == "echo":
            print(" ".join(arguments))

        elif command == "type":
            print_command_type(" ".join(arguments))

        else:
            file_path = get_file_path(command)

            if file_path is not None:
                arguments.insert(0, command)
                subprocess.run(arguments, executable=file_path)

            else:
                print(f"{command}: command not found")


if __name__ == "__main__":
    main()