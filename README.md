# Azure Cognitive Services

Recognizing receipt details using Azure Cognitive Services.

## Development Setup

1. Ubuntu build essentials:
   ```bash
   sudo apt-get update
   sudo apt-get install -y build-essential checkinstall
   sudo apt-get install -y libncursesw5-dev \
   libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev \
   libffi-dev zlib1g-dev wget curl llvm libncurses5-dev git xz-utils \
   tk-dev libffi-dev liblzma-dev python-openssl libreadline-dev libsqlite3-dev \
   unixodbc-dev
   ```

2. Install [pyenv](https://github.com/pyenv/pyenv):
   ```bash
   curl https://pyenv.run | bash
   ```
3. Install and activate the Python version:
   ```bash
   pyenv install
   ```
4. Install [Poetry](https://python-poetry.org/docs/).
   ```bash
   curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
   source $HOME/.poetry/env
   ```
5. Install dependencies
   ```bash
   poetry install
   ```
6. Install the pre-commit Git hooks:
   ```bash
   poetry run pre-commit install
   ```
7. Setup Visual Studio Code:
   ```bash
   poetry env info
   ```
   Copy the full path of the virtualenv created by Poetry.
   Create a file `.vscode/settings.json` with the following contents:
      ```json
      {
        "python.pythonPath": "/path-to-poetry-virtualenv/bin/python"
      }
      ```
## Debugging with Visual Studio Code

To debug with Visual Studio Code, open `launch.json` file by clicking on `Run` -> `Open Configurations`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Recognizer",
            "type": "python",
            "request": "launch",
            "python.pythonPath": "${command:python.interpreterPath}",
            "module": "AzureCognitiveServices.recognizer",
            "console": "integratedTerminal"
        },
        {
            "name": "Python: Pipeline",
            "type": "python",
            "request": "launch",
            "python.pythonPath": "${command:python.interpreterPath}",
            "module": "AzureCognitiveServices.pipeline",
            "args": [
                "--image-folder",
                "data/images/",
            ],
            "console": "integratedTerminal"
        }
    ]
}
```

## Prerequisites

Set the azure variables with your own values before running the code using config/secrets/credentials.yaml:
* endpoint - the endpoint to your Cognitive Services resource.
* key - your Form Recognizer API key

## Run entire pipeline
```bash
poetry run python -m AzureCognitiveServices.pipeline --image-folder data/images
```
