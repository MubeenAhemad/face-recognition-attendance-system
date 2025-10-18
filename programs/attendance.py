import os
import cv2
import pandas as pd
from datetime import datetime
import time
from face_recognition_utils import load_student_data, recognize_faces
from utils import get_lectures_between_times

# Path to the output directory
output_dir = 'D:/FaceRecognitionAttendance/output'
attendance_file = os.path.join(output_dir, 'attendance.xlsx')

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Load student images and encodings
student_folder = os.path.abspath('D:/FaceRecognitionAttendance/students')
student_names, student_encodings = load_student_data(student_folder)

entry_times = {}  # Dictionary to store entry times of students
exit_times = {}   # Dictionary to store exit times to avoid duplicates
cooldown_period = 10  # 10 seconds cooldown between re-detection to avoid duplicates
entry_mode = True  # Ensure the system starts in entry mode

# Video capture from the camera
video_capture = cv2.VideoCapture(0)

def mark_attendance_for_lectures(name, entry_time, exit_time, attendance_file):
    """Marks attendance for all lectures between entry and exit time."""
    now = datetime.now()
    current_date = now.strftime('%Y-%m-%d')
    current_day = now.strftime('%A')
    
    # Get all lectures between entry and exit times
    lectures = get_lectures_between_times(entry_time, exit_time)
    
    for lecture_id, lecture_name in lectures:
        status = 'Present'  # Mark all lectures between entry and exit as present
        
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

        attendance_df = pd.DataFrame(attendance_data)
        
        if not os.path.exists(attendance_file):
            with pd.ExcelWriter(attendance_file, mode='w', engine='openpyxl') as writer:
                attendance_df.to_excel(writer, index=False, sheet_name='Attendance')
        else:
            with pd.ExcelWriter(attendance_file, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
                start_row = writer.sheets['Attendance'].max_row
                attendance_df.to_excel(writer, index=False, sheet_name='Attendance', header=False, startrow=start_row)
        
        print(f"Attendance marked for {name} for Lecture: {lecture_name}")

# Explicitly print that the system starts in Entry Mode by default
print("System started in Entry Mode by default. Press 'x' to switch to Exit Mode, or 'q' to quit.")

while True:
    ret, frame = video_capture.read()
    if not ret:
        print("Failed to capture image from the camera.")
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    recognized_faces = recognize_faces(rgb_frame, student_encodings, student_names)
    current_timestamp = time.time()

    for name in recognized_faces:
        now = datetime.now()
        current_time = now.strftime('%I:%M %p')

        if name != "Unknown":  # Only handle recognized student faces
           if entry_mode:
             if name not in entry_times or (current_timestamp - entry_times[name]['timestamp'] > cooldown_period):
                entry_times[name] = {'timestamp': current_timestamp, 'entry_time': current_time}
                print(f"{name} entered at {current_time}")
             else:
                print(f"{name} has already entered at {entry_times[name]['entry_time']}, skipping duplicate entry.")
           else:
            if name in entry_times:
                if name not in exit_times or (current_timestamp - exit_times[name] > cooldown_period):
                    exit_times[name] = current_timestamp
                    entry_time = entry_times.pop(name)['entry_time']

                    # Mark attendance for all lectures between entry and exit
                    mark_attendance_for_lectures(name, entry_time, current_time, attendance_file)
                    print(f"{name} exited at {current_time}, entry time was {entry_time}.")
                else:
                    print(f"{name} already exited recently, skipping duplicate exit.")
            else:
                print(f"{name} has not entered yet, cannot exit.")
        else:
         print("Unknown face detected, skipping...")

    cv2.imshow('Video', frame)

    # Capture key press
    key = cv2.waitKey(1) & 0xFF
    if key != 255:  # Check if any key is pressed
        print(f"Key pressed: {chr(key)}")  # Print the key pressed for debugging

    if key == ord('e'):  # Switch to Entry mode
        entry_mode = True
        print("Switched to Entry Mode")
    elif key == ord('x'):  # Switch to Exit mode
        entry_mode = False
        print("Switched to Exit Mode")
    elif key == ord('q'):  # Quit the program
        print("Quitting the program...")
        break

# Release resources
video_capture.release()
cv2.destroyAllWindows()
