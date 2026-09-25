import sys
import shutil


def main():
    while True:
        sys.stdout.write("$ ")
        command = input()

        if command == "exit":
            break

        elif command.startswith("echo "):
            print(command[5:])

        elif command.startswith("type "):
            target = command[5:]

            if target in ["type", "echo", "exit"]:
                print(f"{target} is a shell builtin")
            elif path := shutil.which(target):
                print(f"{target} is {path}")
            else:
                print(f"{target}: not found")

        else:
            print(f"{command}: command not found")


if __name__ == "__main__":
    main()