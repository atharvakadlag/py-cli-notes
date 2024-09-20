# CLI Notes Application

This is a simple command-line interface (CLI) application for managing notes. The application allows you to create, view, and add content to notes stored in your home directory.

## Requirements

- Python 3.12.4
- `click` library
- `inquirer` library

## Setup

1. Clone the repository.
2. Create a virtual environment and activate it:
    ```sh
    python -m venv .direnv/python-3.12
    source .direnv/python-3.12/bin/activate
    ```
3. Install the required dependencies:
    ```sh
    pip install click inquirer
    ```

## Usage

### Commands

- **new**: Create a new note.
    ```sh
    python app.py new
    ```

- **view**: View and edit an existing note.
    ```sh
    python app.py view
    ```

- **add**: Add content to an existing note.
    ```sh
    python app.py add [OPTIONS] [CONTENT]
    ```

### Options for `add` command

- `--file`, `-f`: Specify a file to append to the note.
- `--cmd`, `-c`: Append a command from history to the note.

### Example

To create a new note:
```sh
python app.py new
```

To view and edit an existing note:

```sh
python app.py view
```

To add content to an existing note:

```sh
python app.py add "This is additional content."
```