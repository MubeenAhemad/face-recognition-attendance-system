import json
from datetime import datetime

# Load timetable from a JSON file
def load_timetable(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data['lectures']  # Assuming the JSON contains a dictionary where keys are days

# Path to JSON timetable file
timetable_file_path = 'D:/FaceRecognitionAttendance/timetable.json'  # Adjust path as necessary
timetable = load_timetable(timetable_file_path)

def get_lecture_details(current_time):
    """
    Get the current lecture details based on the current time and day of the week.
    """
    current_day = current_time.strftime('%A')
    formatted_time = current_time.strftime('%I:%M %p')

    if current_day in timetable:
        lectures_today = timetable[current_day]
        for lecture in lectures_today:
            lecture_id = lecture['lecture_id']
            lecture_name = lecture['lecture_name']
            start_time = lecture['start_time']
            end_time = lecture['end_time']

            if start_time <= formatted_time <= end_time:
                return lecture_id, lecture_name  # Return the current lecture ID and name

    return None, None

def get_lectures_between_times(entry_time, exit_time):
    """
    Returns all lectures that fall between the entry and exit times.
    This function checks the timetable and finds all the lectures that a student is
    considered 'present' for based on their entry and exit times.
    """
    lectures_in_range = []

    # Convert entry_time and exit_time into datetime objects for comparison
    entry_time_obj = datetime.strptime(entry_time, '%I:%M %p')
    exit_time_obj = datetime.strptime(exit_time, '%I:%M %p')

    current_day = datetime.now().strftime('%A')

    if current_day in timetable:
        lectures_today = timetable[current_day]

        for lecture in lectures_today:
            lecture_start_time = datetime.strptime(lecture['start_time'], '%I:%M %p')
            lecture_end_time = datetime.strptime(lecture['end_time'], '%I:%M %p')

            # Check if the lecture falls between the student's entry and exit time
            if lecture_start_time >= entry_time_obj and lecture_end_time <= exit_time_obj:
                lectures_in_range.append((lecture['lecture_id'], lecture['lecture_name']))

    return lectures_in_range

# Example usage:
if __name__ == "__main__":
    # Test get_lecture_details
    current_time = datetime.now()
    lecture_id, lecture_name = get_lecture_details(current_time)
    
    if lecture_id and lecture_name:
        print(f"Current Lecture: {lecture_name} (ID: {lecture_id})")
    else:
        print("No lecture is active at this time.")
    
    # Test get_lectures_between_times
    entry_time = '09:00 AM'  # Example entry time
    exit_time = '12:00 PM'  # Example exit time
    
    # Fetch all lectures that fall between entry and exit times
    lectures = get_lectures_between_times(entry_time, exit_time)
    
    if lectures:
        print(f"Lectures between {entry_time} and {exit_time}:")
        for lecture_id, lecture_name in lectures:
            print(f"Lecture ID: {lecture_id}, Lecture Name: {lecture_name}")
    else:
        print(f"No lectures found between {entry_time} and {exit_time}.")
