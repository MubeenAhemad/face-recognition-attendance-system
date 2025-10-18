import os
import face_recognition
import numpy as np  # Import numpy here
import pandas as pd
from datetime import datetime

def load_student_data(student_folder):
    student_names = []
    student_encodings = []
    for filename in os.listdir(student_folder):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            img_path = os.path.join(student_folder, filename)
            student_image = face_recognition.load_image_file(img_path)
            student_encoding = face_recognition.face_encodings(student_image)
            if student_encoding:  # Ensure there is at least one encoding
                student_names.append(os.path.splitext(filename)[0])
                student_encodings.append(student_encoding[0])  # Append the first encoding
    return student_names, student_encodings

def recognize_faces(rgb_frame, student_encodings, student_names):
    # Find all face locations and encodings in the current frame
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    recognized_names = []

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(student_encodings, face_encoding)
        name = "Unknown"  # Default if no match is found

        if True in matches:
            first_match_index = matches.index(True)
            name = student_names[first_match_index]

        recognized_names.append(name)

    return recognized_names  # Return only recognized name

# Path to the output directory
output_dir = 'D:/FaceRecognitionAttendance/output'
# Path to the Excel file where attendance is stored
attendance_file = os.path.join(output_dir, 'attendance.xlsx')

def mark_attendance(name, lecture_id, lecture_name, entry_time, exit_time):
    # Get current date and day
    now = datetime.now()
    current_date = now.strftime('%Y-%m-%d')
    current_day = now.strftime('%A')

    # Attendance status logic (you can customize this part)
    if entry_time and exit_time:
        status = 'Present'
    else:
        status = 'Absent'

    # Create a dictionary with the attendance details
    attendance_data = {
        'Date': [current_date],
        'Day': [current_day],
        'Student Name': [name],
        'Lecture Number': [lecture_id],
        'Lecture Name': [lecture_name],
        'Entry Time': [entry_time],
        'Exit Time': [exit_time],
        'Attendance Status': [status]
    }

    # Convert the dictionary to a DataFrame
    attendance_df = pd.DataFrame(attendance_data)

    # Check if the Excel file exists
    if not os.path.exists(attendance_file):
        # If the file doesn't exist, create it and write the header
        with pd.ExcelWriter(attendance_file, mode='w', engine='openpyxl') as writer:
            attendance_df.to_excel(writer, index=False, sheet_name='Attendance')
    else:
        # If the file exists, append the new data without overwriting
        with pd.ExcelWriter(attendance_file, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
            start_row = writer.sheets['Attendance'].max_row
            attendance_df.to_excel(writer, index=False, sheet_name='Attendance', header=False, startrow=start_row)

    print(f"Attendance marked for {name} for Lecture: {lecture_name}")