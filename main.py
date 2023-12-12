import cv2
import os
import face_recognition
import numpy as np
import telebot
from telebot import types
import threading
import queue
from constants import TOKEN, UNKNOWN_FACES_DIR_PATH, DEFAULT_ADMIN
from helpers import clear_directory, unknown_faces_saver, unknown_faces_sender
from markups import stats_menu, confirm_add_student, settings_menu, tolerance_menu

bot = telebot.TeleBot(TOKEN)


# Clear the unknown_faces directory
clear_directory(UNKNOWN_FACES_DIR_PATH)


# Initialize a queue to communicate between threads
student_queue = queue.Queue()
tolerance_queue = queue.Queue()


# Define a function that updates the known face encodings list
def update_known_face_encodings():
    global unknown_face_encodings
    while True:
        try:
            # Get data about the new student from the queue
            student_data = student_queue.get(timeout=1)
            student_name, encoding, index = student_data

            # Save the student in known_face_encodings to be recognized
            known_face_names.append(student_name)
            known_face_encodings.append(encoding)

            # Save the student in added_face_encodings for it not to be lost when faces_to_encodings.py is run
            added_face_names.append(student_name)
            added_face_encodings.append(encoding)

            np.save('db/added_face_encodings.npy', added_face_encodings)
            np.save('db/added_face_names.npy', added_face_names)

            print(f"Added student: {student_name}")

            added_students_indexes.append(index)
        except queue.Empty:
            pass


# Define a function that updates the tolerance parameter
def update_tolerance():
    global tolerance
    while True:
        try:
            tolerance = tolerance_queue.get(timeout=1)  # get new value of the tolerance from the queue
            print(f"Tolerance changed to {tolerance}")
        except queue.Empty:
            pass


# Start a thread to update known face encodings
update_thread = threading.Thread(target=update_known_face_encodings)
update_thread.start()

# Start a thread to update the tolerance parameter
tolerance_thread = threading.Thread(target=update_tolerance)
tolerance_thread.start()


# Define a function that registers a name of the new student
def reg_name(message):
    global student_name
    student_name = message.text

    bot.send_message(admin, f'Name of the newly added student is {student_name}, correct?',
                     reply_markup=confirm_add_student)


# React to the '/start' command
@bot.message_handler(commands=['start'])
def start(message):
    global admin
    admin = message.chat.id

    bot.reply_to(message, f"Hello! I am a bot, which will provide statistics about students' attendance")
    bot.send_message(admin, "Send me '/stats' command to open the statistics menu")

    # face_rec()  # open a webcam


# React to the '/stats' command
@bot.message_handler(commands=['stats'])
def start(message):
    bot.send_message(message.chat.id, "What do you want to know?", reply_markup=stats_menu)


# React to the '/settings' command
@bot.message_handler(commands=['settings'])
def start(message):
    bot.send_message(message.chat.id, "What setting do you want to change?", reply_markup=settings_menu)


# React to text messages
@bot.message_handler(content_types=['text'])
def check(message):
    global add_student
    if add_student:
        # when add_student flag is up, the text of the message is supposed to be the name of the new student
        reg_name(message)
        # so the text of the message is redirected to the reg_name function that registers the new student's name


# React to clicking the inline buttons
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    global add_student, unknown_face_num, tolerance, name

    # stats_menu buttons
    if call.data == 'number_students':
        bot.send_message(admin, f'{num_faces} faces detected')
    elif call.data == 'number_unknowns':
        bot.send_message(admin, f'{len(unknown_face_encodings)} unknown faces are registered')
    elif call.data == 'unknown_faces':
        bot.send_message(admin, "Here is the photos of unknown faces detected:")
        for k in range(len(unknown_face_encodings)):
            if k not in added_students_indexes:
                markup_inline_name_to_unknown = types.InlineKeyboardMarkup(row_width=1)
                item_add_student = types.InlineKeyboardButton(text='Add a student', callback_data=f'add_student-{k}')
                markup_inline_name_to_unknown.add(item_add_student)

                with open(f'unknown_faces/unknown_face_{k}.jpg', 'rb') as photo:
                    bot.send_photo(admin, photo, reply_markup=markup_inline_name_to_unknown)

    # name_to_unknown button
    elif call.data.startswith("add_student-"):
        unknown_face_num = int(call.data.split('-')[1])
        bot.send_message(admin, "Enter a name of the student")
        add_student = True

    # confirm_add_student buttons
    elif call.data == "yes":
        bot.send_message(admin, 'The student is added')
        add_student = False

        print(student_name)
        student_face_encoding = unknown_face_encodings[unknown_face_num]

        # put the face encoding and name of the student to the queue to then add it to the know face encodings
        student_queue.put((student_name, student_face_encoding, unknown_face_num))

    elif call.data == "no":
        bot.send_message(admin, "Enter a name of the student")

    # settings_menu buttons
    elif call.data == "change_tolerance":
        bot.send_message(admin, f"Choose the tolerance (current is {tolerance})", reply_markup=tolerance_menu)

    # tolerance menu buttons
    elif call.data.startswith("0."):
        tolerance_queue.put(float(call.data))
        bot.send_message(admin, f"Tolerance updated to {call.data}")


add_student = False
num_faces = 0
student_name = ''
name = ''
admin = DEFAULT_ADMIN
unknown_face_num = -1
tolerance = 0.5
added_students_indexes = []
unknown_face_encodings = []

# Load known face encodings and names
if os.path.exists('db/added_face_encodings.npy'):
    known_face_encodings = np.load('db/known_face_encodings.npy').tolist() + np.load('db/added_face_encodings.npy').tolist()
    known_face_names = np.load('db/known_face_names.npy').tolist() + np.load('db/added_face_names.npy').tolist()

    # Newly added students are saved in a seperate numpy file so that when faces_to_encodings.py is run they are not lost
    added_face_encodings = np.load('db/added_face_encodings.npy').tolist()
    added_face_names = np.load('db/added_face_names.npy').tolist()
else:
    known_face_encodings = np.load('db/known_face_encodings.npy').tolist()
    known_face_names = np.load('db/known_face_names.npy').tolist()

    added_face_encodings = []
    added_face_names = []


# Create a directory to save the unknown face images
os.makedirs('unknown_faces', exist_ok=True)


# Define a function that opens the webcam and gets data from it
def face_rec():
    global num_faces, admin

    video_capture = cv2.VideoCapture(0)  # open the webcam

    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        # Find face locations in the frame
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        # Count the number of faces in the frame
        num_faces = len(face_locations)

        i = 0
        for face_encoding in face_encodings:

            # Compare the face with known faces
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=tolerance)

            # Compare the face with already registered unknown faces
            unknown_face_matches = face_recognition.compare_faces(unknown_face_encodings, face_encoding, tolerance=0.5)

            # Set default value of the name to "Unknown"
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                # Get the name of the known face
                name = known_face_names[first_match_index]

            # Get the corners of the rectangle of the face location
            top, right, bottom, left = face_locations[i]
# lets run the app for 1 month (i can change)
            # after 1 month i stop this and i have new database
            if (name == "Unknown") and not (True in unknown_face_matches):
                # Get the rectangle f
                face_image = frame[top:bottom, left:right]

                # Count the number of the registered unknown faces
                unknown_face_counter = len(unknown_face_encodings)

                unknown_faces_saver(face_image, unknown_face_counter)
                unknown_faces_sender(unknown_face_counter, bot, admin)

                unknown_face_encodings.append(face_encoding)

            # Draw a rectangle and label on the frame
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

            i += 1

        # Display the frame
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close the OpenCV window
    video_capture.release()
    cv2.destroyAllWindows()


face_recognition_thread = threading.Thread(target=face_rec)
face_recognition_thread.start()

bot.polling(non_stop=True)