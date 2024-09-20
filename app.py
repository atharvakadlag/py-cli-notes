#!/Users/atharva/.pyenv/shims/python
import click
import os
import sys
import inquirer

LAST_NOTE_FILE = os.path.expanduser("~/notes/.last_note")
HISTFILE = "/Users/atharva/.zsh_history"


# ## UTILS ###
def tail(file_path, lines=10):
    """Read the last `lines` lines from a file."""
    with open(file_path, "rb") as f:
        f.seek(0, os.SEEK_END)
        buffer = bytearray()
        pointer_location = f.tell()
        while pointer_location >= 0 and lines > 0:
            f.seek(pointer_location)
            pointer_location -= 1
            new_byte = f.read(1)
            if new_byte == b"\n":
                lines -= 1
            buffer.extend(new_byte)
        return buffer[::-1].decode("utf-8")


# ## APP CODE ###


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        view_last_note()


@cli.command()
def new():
    # Get the home directory
    home_dir = os.path.expanduser("~")
    notes_dir = os.path.join(home_dir, "notes")

    # Ensure the notes directory exists
    if not os.path.exists(notes_dir):
        os.makedirs(notes_dir)

    # Get the note name
    note_name = click.prompt("Enter the note name")

    # Get the note content
    click.echo("Enter your note (end with Ctrl+D):")
    note_content = sys.stdin.read()

    # Save the note
    note_path = os.path.join(notes_dir, note_name + ".txt")
    with open(note_path, "w") as note_file:
        note_file.write(note_content)

    # Save the last edited note
    with open(LAST_NOTE_FILE, "w", encoding="utf-8") as last_note_file:
        last_note_file.write(note_name + ".txt")

    click.echo(f"Note saved as {note_path}")


@cli.command()
def view():
    try:
        # Get the home directory
        home_dir = os.path.expanduser("~")
        notes_dir = os.path.join(home_dir, "notes")

        # Ensure the notes directory exists
        if not os.path.exists(notes_dir):
            click.echo("No notes directory found.")
            return

        # List all notes
        notes = [f for f in os.listdir(notes_dir) if os.path.isfile(os.path.join(notes_dir, f)) and f.endswith(".txt")]
        if not notes:
            click.echo("No notes found.")
            return

        # Use inquirer to select a note
        questions = [
            inquirer.List(
                "note",
                message="Select a note to view",
                choices=notes,
            ),
        ]
        answers = inquirer.prompt(questions)
        selected_note = answers["note"]

        note_filename = os.path.join(notes_dir, selected_note)
        click.edit(filename=note_filename)
        with open(LAST_NOTE_FILE, "w") as last_note_file:
            click.echo(f"Last note edited: {selected_note}")
            last_note_file.write(selected_note)
    except KeyboardInterrupt:
        click.echo("\nNote view aborted.")
    except TypeError as e:
        click.echo(f"\nNo note selected. {e}")


def view_last_note():
    try:
        # Check if the last note file exists
        if not os.path.exists(LAST_NOTE_FILE):
            click.echo("No last edited note found.")
            return

        # Read the last edited note
        with open(LAST_NOTE_FILE, "r") as last_note_file:
            last_note = last_note_file.read().strip()

        # Get the home directory
        home_dir = os.path.expanduser("~")
        notes_dir = os.path.join(home_dir, "notes")
        note_path = os.path.join(notes_dir, last_note)

        # Ensure the note exists
        if not os.path.exists(note_path):
            click.echo("Last edited note not found.")
            return

        # Display the last edited note
        with open(note_path, "r") as note_file:
            note_content = note_file.read()

        click.echo(f"\nContent of {last_note}:\n")
        click.echo(note_content)
    except KeyboardInterrupt:
        click.echo("\nNote view aborted.")


@cli.command()
@click.argument("content", required=False)
@click.option("--file", "-f", "file", help="File to append to the note")
@click.option("--cmd", "-c", "command", is_flag=True, help="Append a command from history to the note")
def add(content, file, command):
    try:
        # Check if the last note file exists
        if not os.path.exists(LAST_NOTE_FILE):
            click.echo("No last edited note found.")
            return

        # Check if the last note file exists
        if file:
            if os.path.exists(file):
                # Read the last edited note
                click.echo(f"Reading content from file: {file}")
                with open(file, "r") as content_file:
                    content = content_file.read().strip()
                    content = "---\nfile: " + file + "\n" + content + "\n---\n"
            else:
                click.echo(f"File not found: {file}")
                return

        if command:
            # run the command history to get the last 10 lines of the command history
            history_content = tail(HISTFILE, 10)
            history_lines = history_content.strip("\n").split("\n")
            history_lines = [(";").join(i.split(";")[1:]) for i in history_lines]

            print(history_lines)
            # present the lines in inquirer multi select
            questions = [
                inquirer.Checkbox(
                    "lines",
                    message="Select lines to append",
                    choices=[(line, i) for i, line in enumerate(history_lines)],
                ),
            ]
            answers = inquirer.prompt(questions)
            selected_lines = [history_lines[i] for i in answers["lines"]]
            content = "\n".join(selected_lines)

        # Read the last edited note
        with open(LAST_NOTE_FILE, "r") as last_note_file:
            last_note = last_note_file.read().strip()

        # Get the home directory
        home_dir = os.path.expanduser("~")
        notes_dir = os.path.join(home_dir, "notes")
        note_path = os.path.join(notes_dir, last_note)

        # Ensure the note exists
        if not os.path.exists(note_path):
            click.echo("Last edited note not found.")
            return

        if content:
            with open(note_path, "a") as note_file:
                note_file.write("\n" + content)
            click.echo(f"Appended to note: {note_path}")
        else:
            # click.echo("Enter your note (end with Ctrl+D):")
            # new_content = sys.stdin.read()
            questions = [
                inquirer.Editor(
                    "content",
                    message="Enter your note content",
                ),
            ]
            answers = inquirer.prompt(questions)
            new_content = answers["content"]
            new_content = "\n" + new_content
            with open(note_path, "a") as note_file:
                note_file.write(new_content)

        click.echo(f"Note updated: {note_path}")
    except KeyboardInterrupt:
        click.echo("\nNote update aborted.")


if __name__ == "__main__":
    cli()
