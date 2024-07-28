# Mekore: Image Downloader

Mekore is a Python script that allows you to download images from a website, with options to block or allow specific filenames. It utilizes concurrency to speed up the downloading process.

## Usage

### Using Python Script

1. **Clone the repository:**

    ```bash
    git clone https://github.com/0Akiro/Mekore.git
    ```

2. **Navigate to the directory:**

    ```bash
    cd mekore
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the script:**

    ```bash
    python mekore.py [URL] [--block_list BLOCK_LIST_FILE] [--allow_list ALLOW_LIST_FILE]
    ```

    Replace `[URL]` with the URL of the website from which you want to download images. Optionally, you can specify the `--block_list` and `--allow_list` arguments to provide files containing lists of blocked and allowed filenames, respectively.

    Example:

    ```bash
    python mekore.py https://example.com --block_list blocked.txt --allow_list allowed.txt
    ```

### Using Pre-Compiled Executable

1. **Download the executable from the [releases](https://github.com/0Akiro/Mkore/releases) page.**

2. **Open Command Prompt (cmd) and navigate to the directory containing the executable.**

3. **Run the executable with the desired arguments:**

    ```bash
    mekore.exe [URL] [--block_list BLOCK_LIST_FILE] [--allow_list ALLOW_LIST_FILE]
    ```

    Replace `[URL]` with the URL of the website from which you want to download images. Optionally, you can specify the `--block_list` and `--allow_list` arguments to provide files containing lists of blocked and allowed filenames, respectively.

    Example:

    ```bash
    mekore.exe https://example.com --block_list blocked.txt --allow_list allowed.txt
    ```

## Arguments

- `url` (positional): URL of the website from which to download images.
- `--block_list BLOCK_LIST_FILE`: File containing a list of blocked filenames.
- `--allow_list ALLOW_LIST_FILE`: File containing a list of allowed filenames.

## Termux

```bash
pkg install git python3 python-pip && git clone https://github.com/0akiro/mekore && cd mekore && pip install -r requirements.txt

