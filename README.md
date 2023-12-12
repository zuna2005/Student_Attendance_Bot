# Student Attendance Bot

## Developers
[Bobur Djalalov](https://github.com/bobalive) \
[Nasiba Zulunova](https://github.com/zuna2005)


## Overview

The Student Attendance Bot is a Telegram bot that utilizes face recognition to track and manage student attendance. It is designed to be a user-friendly tool for teachers or administrators to easily keep track of students attending classes.

## Features

- **Face Recognition**: The bot uses the face recognition library to identify and register students based on their facial features.
- **Statistics**: Provides statistics about the number of faces detected and the count of unknown faces.
- **Unknown Faces Management**: Users can view a list of unknown faces, assign names to them, and save the information for future recognition.
- **Dynamic Tolerance Adjustment**: Users can adjust the tolerance level for face recognition to fine-tune the accuracy.
- **Interactive Menu**: Utilizes inline buttons and command triggers to provide a user-friendly interface for interaction.
- **Webcam Integration**: The bot captures frames from the webcam in real-time to recognize faces.

## Getting Started

To use the Student Attendance Bot, follow these steps:

1. **Installation**: First, install [Visual Studio](https://visualstudio.microsoft.com/ru/) in order to run `dlib` library. \
   Then, clone the repository and install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

2. **Configuration**: In the `constants.py` file define:
   - `TOKEN` for your Telegram bot
   - `ABSOLUTE_PATH` to the folder where your project is located
    
3. **Add student photos**: Organize student photos into folders inside the `faces` directory. Each folder should be named after a student, and photos of that student should be placed within the corresponding folder.
4. **Save encodings**: Run the `faces_to_encodings.py` to save the encodings of the students' photos:
    ```bash
    python faces_to_encodings.py
    ```
   
5. **Save encodings**: Execute the main script:
    ```bash
    python main.py
    ```

6. **Interaction**: Use the Telegram commands such as `/start`, `/stats`, and `/settings` to interact with the bot. Follow the prompts to add new students and adjust settings.

## Project Structure

- **main.py**: The main script that initializes and runs the Telegram bot.
- **faces_to_encodings.py**: The script that converts the photos of the students to the encodings and saves them.
- **constants.py**: Configuration constants, including the Telegram bot token and directory paths.
- **helpers.py**: Helper functions for managing unknown faces, updating known face encodings, and handling directories.
- **markups.py**: Configuration for Telegram inline keyboards and button layouts.

## Dependencies

- OpenCV
- face_recognition
- numpy
- telebot

## Contributing

If you find issues or have suggestions for improvements, feel free to create an issue or submit a pull request.


## Acknowledgments

- Special thanks to the developers of the face_recognition library for providing the face recognition capabilities.
- The project structure and threading approach are inspired by the need for real-time processing of webcam frames.

Enjoy tracking student attendance with the Student Attendance Bot!