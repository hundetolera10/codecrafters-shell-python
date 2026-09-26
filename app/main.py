import sys
import os
import subprocess


def main():

    # Commands that our shell handles itself
    builtin_commands = ["exit", "echo", "type", "pwd", "cd"]

    # Keep the shell running until the user enters "exit"
    while True:

        # Display the shell prompt
        sys.stdout.write("$ ")

        # Read what the user types
        user_input = input()

        # Split the input into command + arguments
        # Example:
        # "echo hello world"
        # becomes:
        # ["echo", "hello", "world"]
        parts = user_input.split()

        # If the user presses Enter without typing anything,
        # restart the loop and display another prompt
        if not parts:
            continue

        # First item is the command
        command = parts[0]

        # Everything after the command is an argument
        arguments = parts[1:]

        # -------------------------
        # EXIT BUILTIN
        # -------------------------
        if command == "exit":

            # Stop the REPL loop and close the shell
            break

        # -------------------------
        # ECHO BUILTIN
        # -------------------------
        elif command == "echo":

            # Join all arguments together with spaces
            # Example:
            # ["hello", "world"] -> "hello world"
            print(" ".join(arguments))

        # -------------------------
        # PWD BUILTIN
        # -------------------------
        elif command == "pwd":

            # os.getcwd() returns the current working directory
            print(os.getcwd())

        elif command == "cd":
            target_dir= " ".join(arguments)
            try:
                os.chdir(target_dir)
            except FileNotFoundError:
                print(f"cd:{target_dir}: No such file or directory")
            except PermissionError:
                print(f"cd:{target_dir}: Permission denied")
        # -------------------------
        # TYPE BUILTIN
        # -------------------------
        elif command == "type":

            # The command we want information about
            target = " ".join(arguments)

            # First check if the target is one of our builtins
            if target in builtin_commands:
                print(f"{target} is a shell builtin")

            else:
                # Assume we haven't found the executable yet
                executable_path = None

                # Get PATH from the operating system
                path_environment = os.environ.get("PATH", "")

                # Split PATH into separate directories
                # Linux/macOS uses :
                # Windows uses ;
                # os.pathsep automatically chooses the correct one
                path_directories = path_environment.split(os.pathsep)

                # Search each PATH directory
                for directory in path_directories:

                    # Build a possible executable path
                    file_path = os.path.join(directory, target)

                    # Check:
                    # 1. Is it actually a file?
                    # 2. Is it executable?
                    if (
                        os.path.isfile(file_path)
                        and os.access(file_path, os.X_OK)
                    ):
                        executable_path = file_path
                        break

                # If we found it, print the path
                if executable_path is not None:
                    print(f"{target} is {executable_path}")

                # Otherwise the command doesn't exist
                else:
                    print(f"{target}: not found")

        # -------------------------
        # EXTERNAL PROGRAMS
        # -------------------------
        else:

            # Assume the executable doesn't exist yet
            executable_path = None

            # Read PATH
            path_environment = os.environ.get("PATH", "")

            # Split PATH into directories
            path_directories = path_environment.split(os.pathsep)

            # Search PATH for the program
            for directory in path_directories:

                file_path = os.path.join(directory, command)

                # Check if the file exists and is executable
                if (
                    os.path.isfile(file_path)
                    and os.access(file_path, os.X_OK)
                ):
                    executable_path = file_path
                    break

            # If the executable exists, run it
            if executable_path is not None:

                # argv should look like:
                #
                # ["program_name", "arg1", "arg2"]
                #
                # executable= tells Python which actual file to execute
                subprocess.run(
                    [command] + arguments,
                    executable=executable_path,
                )

            # Otherwise print command not found
            else:
                print(f"{command}: command not found")


# Start the shell
if __name__ == "__main__":
    main()