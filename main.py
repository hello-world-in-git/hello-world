# Code to generate pixel art on your Github contributions mosaic.
#
# To make it work:
# 1. Create a new user on github and create a new project.
# 2. Set the desired art, email, name and remote in this file below
# 3. run `python3 main.py | /bin/bash`
#
# Created by Sándor Polgár on 2024-10-30
# Original: https://github.com/hello-world-in-git/hello-world/
#

from os.path import basename
import datetime


# Set the pixels here (52×7 pixels for 364 days)
TEXT = ".................................................... \
        ...@.@.@@@.@...@...@@@....@...@.@@@.@@@.@...@@..@... \
        ...@.@.@...@...@...@.@....@...@.@.@.@.@.@...@.@.@... \
        ...@@@.@@@.@...@...@.@....@...@.@.@.@@..@...@.@.@... \
        ...@.@.@...@...@...@.@....@.@.@.@.@.@.@.@...@.@..... \
        ...@.@.@@@.@@@.@@@.@@@.....@.@..@@@.@.@.@@@.@@..@... \
        ...................................................."

GIT_COMMIT_EMAIL = "186809185+hello-world-in-git@users.noreply.github.com"
GIT_COMMIT_NAME = "Hello World"
GIT_REMOTE = "git@github.com:hello-world-in-git/hello-world.git"


def main():

    # Create a string with the characters in correct order
    lines = TEXT.split()
    cols = "".join([lines[j][i] for i in range(52) for j in range(7)])

    def get_date(i):
        """Return the timestamp on the ith day of 2024 in the format that git expects it"""
        date = datetime.datetime(2023, 1, 1, 12) + datetime.timedelta(days=i-1)
        # 2023 starts with a Sunday, making it ideal for art
        date_string = date.strftime("%a %b %d %H:%M %Y +0100")
        return date_string

    file_name = "text.txt"  # The single file created in the git repo

    # Create and initialize git repo
    init_command = f"git init && touch {file_name}"
    # set git config options
    config_command = f"git config user.email '{GIT_COMMIT_EMAIL}' && git config user.name '{GIT_COMMIT_NAME}' && git remote add 'origin' {GIT_REMOTE}"
    # Add a last commit on the last day of year, add this python file too
    final_commit_command = f"git add {file_name} {basename(__file__)} && GIT_COMMITTER_DATE='{get_date(365)}' git commit -m 'Final commit' --date='{get_date(365)}'"
    # Push the repo to the remote
    push_command = f"git push --set-upstream origin master"

    # Print the text to a file and create a commit for each green pixel
    # Based on https://stackoverflow.com/a/5017265
    commit_commands = [f"echo -n '{cols[i]}' >> {file_name}" +
                       (f" && git add {file_name} && GIT_COMMITTER_DATE='{get_date(i+1)}' git commit -m 'commit on day {i+1}' --date='{get_date(i+1)}'" if cols[i] == "@" else "") for i in range(364)]

    # Concatenate all command into one
    command = f"{init_command} && {config_command} && {' && '.join(commit_commands)} && {final_commit_command} && {push_command}"

    # Print the command.
    print(command)


if __name__ == "__main__":
    main()
