Face Recognition Based Attendance System 

Overview:
The Face Recognition Based Attendance System is an automated solution designed to streamline attendance tracking in educational institutions using real-time face recognition technology.

Features:
Real-time face detection and recognition
Automatic entry and exit time recording
Multi-lecture attendance marking
Excel report generation
Dual mode operation (entry/exit)

Installation:
Prerequisites
Python 3.9
Anaconda Navigator
Camera device

Step-by-Step Installation:
Create Conda Environment

bash
conda create -n FaceRecogAttendance python=3.9
conda activate FaceRecogAttendance
Install Dependencies

bash
conda install numpy pandas opencv
pip install face_recognition openpyxl
Clone Repository

bash
git clone https://github.com/MubeenAhemad/face-recognition-attendance-system.git
cd face-recognition-attendance-system
Project Structure
text
face-recognition-attendance-system/
├── students/                 # Student images
│   ├── Disha.jpg
│   └── Roy.jpg
├── output/                  # Attendance reports
├── programs/               # Source code
│   ├── attendance.py
│   ├── face_recognition_utils.py
│   ├── main.py
│   └── utils.py
├── timetable.json          # Lecture schedule
└── requirements.txt        # Dependencies

Usage
1. Setup Student Images,Output directories and Timetable
Store student images in students/ folder
Use filenames as student names: john.jpg

2. Configure Timetable
Edit timetable.json:

json
{
  "lectures": [
    {
      "name": "Mathematics",
      "start_time": "09:00",
      "end_time": "10:00",
      "days": ["Monday", "Wednesday", "Friday"]
    }
  ]
}
3. Run the System
bash
cd programs
python main.py
4. Controls
Press e for Entry Mode

Press x for Exit Mode

Press q to Quit

Output
The system generates Excel files with:
Date and day
Lecture details
Student names
Entry and exit times
Attendance status

Sample Output
Date	       Day	     Lecture	     Student Name	  Entry Time	 Exit Time	  Status
2024-01-15	Monday	  Mathematics	   John Doe	       08:45	     10:15	    Present

Requirements:
OpenCV
Face Recognition
Pandas
NumPy
Openpyxl


Contact-
Developer: Mubeen Ahemad Attar
Email: amubeen310@gmail.com
Project Link: https://github.com/MubeenAhemad/face-recognition-attendance-system