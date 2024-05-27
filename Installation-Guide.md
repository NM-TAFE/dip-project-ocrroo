# Project Installation Guide

This guide provides detailed steps and installing the project on your local machine.

## 1. Clone Project Repository

Clone the main repository to your local machine.If you intend to contribute to the development, clone from your fork of the repository.

```bash

git clone  https://github.com/NM-TAFE/dip-programming-prj-advanced-gui-awesome.git

```

## 2. Navigate to Project Directory 

Change into the project directory.

```bash

cd project-advanced-ui-developmennt-team-mental-capacity/

```

## 3. Install Dependencies

Install the project dependencies using the following command.

```bash

pip install -r requirements.txt

```

## 4. Navigate to App Directory

Change into app directory.

```bash
cd app/

```

## 5. (Optional) Configure Application

Copy the `config.example.ini` file and add your relevant configuration variables.Unlike previous versions of OcrRoo, you no longer need to manually create the `config.ini` file;it will generate itself if not present when the server runs.

Using `copy`:

```bash
copy config.example.ini config.ini

```

Or using `cp`:

```bash
cp config.example.ini config.ini

```

## 6. Run the Application

To run the application with silenced debug/logging output, execute the following command. Debug and logging outputs will be saved to an `app.log` file

```bash
python app.py

```

To run the application with debug/logging output in the console, use the following command.This is recommended for development as it automatically reloads the app when changes are detected.

```bash
flask run --debug

```

## Configuration Variables

To use the project, add the following configuration variables to your `config.ini` file:

- `openai_api_key`: API key for OpenAI
- `tesseract_executable`: Path to Tesseract OCR executable
- `ide_executable`: Path to preferred IDE executable

In the current version of the project, this manual configuration is necessary.However, future builds will allow you to perform this configuration from the user interface (UI). 
