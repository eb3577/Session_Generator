#Input CSV MUST include headers.
#Output CSV MUST NOT include headers, Panopto bulk scheduler will not accept CSV with headers.


import csv
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import filedialog


# Function to select today's file
def input_file():
    global input_filename
    global input_fp
    input_fp = filedialog.askopenfilename(title="Select input CSV")
    input_name = input_fp.split("/")
    input_filename = input_name[-1]
    input_lbl.config(text=f"Input file: {input_filename}")
#Specify path and filename for output CSV
def output_file():
    global output_filename
    global output_fp
    output_fp = filedialog.asksaveasfilename(defaultextension="csv")
    output_name = output_fp.split("/")
    output_filename = output_name[-1]
    output_lbl.config(text=f"Output file: {output_filename}")
    output_result_label.config(text=f"CSV file '{output_fp}' has been generated. Use this file for the Panopto Bulk Scheduler")
# Specify path for skipped rows CSV
def skipped_rows_file():
    global skip_filename
    global skip_fp
    skip_fp = filedialog.asksaveasfilename(defaultextension="txt")
    skip_name = skip_fp.split("/")
    skip_filename = skip_name[-1]
    skip_lbl.config(text=f"Skipped rows file: {skip_filename}")
    skip_result_label.config(text=f"Text file '{skip_fp}' has been generated.")




def convert_to_12_hour_time(input_time, add_minutes=0):
   
    hours, minutes = divmod(input_time, 100)


    # Validate time
    if hours < 0 or hours > 23 or minutes < 0 or minutes > 59:
        return "Invalid input"


    # for handling cases where minutes go below zero or exceed 59
    minutes += add_minutes
    while minutes < 0:
        hours -= 1
        minutes += 60
    while minutes > 59:
        hours += 1
        minutes -= 60


    # for hours to be in the range of 1 to 12 for 12-hour format
    hours = hours % 12
    if hours == 0:
        hours = 12


    # AM or PM
    meridian = "PM" if input_time >= 1200 else "AM"


    # Formatting
    return "{:02d}:{:02d} {}".format(hours, minutes, meridian)


def generate_sessions(course):
    sessions = []
    days_map = {'M': 'Monday', 'T': 'Tuesday', 'W': 'Wednesday', 'R': 'Thursday', 'F': 'Friday', 'S': 'Saturday', 'U': 'Sunday'}


    try:
        start_date = datetime.strptime(course['Class_Begin_Date'], '%Y-%m-%d %H:%M:%S')
        end_date = datetime.strptime(course['Class_End_Date'], '%Y-%m-%d %H:%M:%S')


        start_time = datetime.strptime(convert_to_12_hour_time(int(course['Class_Begin_Time']), add_minutes=-1), '%I:%M %p')
        end_time = datetime.strptime(convert_to_12_hour_time(int(course['Class_End_Time']), add_minutes=10), '%I:%M %p')


        days_of_week = course['Class_Days_Code'].upper()


        current_date = start_date
        while current_date <= end_date:
            for day_code in days_of_week:
                day = days_map.get(day_code)
                if day and current_date.strftime('%A') == day:
                    room_code = course['Class_Room_Code']
                    building_code = course['Class_Building_Code']


                                       
                    if building_code == 'CSC' and room_code == '451':
                        room_building_combination = f"451 CSC"
                    elif building_code == 'MUD' and room_code == '833':
                        room_building_combination = f"833 MUDD Maevex"
                    elif building_code == 'SCH' and room_code == '501':
                        room_building_combination = f"501 SCH (0013)"
                    elif building_code == 'SCH' and room_code == '614':
                        room_building_combination = f"614 SCH"
                    elif building_code == 'SCEP' and room_code == '412':
                        room_building_combination = f"Davis Auditorium (PC 003)"
                    elif building_code == 'MUD' and room_code == '1024':
                        room_building_combination = f"1024 MUDD Seneca"
                    elif building_code == 'SCEP' and room_code == '750':
                        room_building_combination = f"750 CEPSR"
                    elif building_code == 'MUD' and room_code == '303':
                        room_building_combination = f"303 MUDD Seneca"
                    elif building_code == 'MUD' and room_code == '524':
                        room_building_combination = f"524 MUDD Seneca"
                    elif building_code == 'NWC' and room_code == '501':
                        room_building_combination = f"501 NWC Seneca"
                    elif building_code == 'MUD' and room_code == '627':
                        room_building_combination = f"627 MUDD Seneca"
                    elif building_code == 'MUD' and room_code == '1127':
                        room_building_combination = f"1127 MUDD Seneca NEW"
                    elif building_code == 'HAM' and room_code == '702':
                        room_building_combination = f"702 HAM"
                    elif building_code == 'MUD' and room_code == '545':
                        room_building_combination = f"545 MUDD Seneca"
                    elif building_code == 'HAV' and room_code == '209':
                        room_building_combination = f"209 HAV Maevex"
                    elif building_code == 'PUP' and room_code == '428':
                        room_building_combination = f"428 PUP Maevex"
                    elif building_code == 'IAB' and room_code == '417':
                        room_building_combination = f"417 IAB Maevex"
                    elif building_code == 'PUP' and room_code == '301':
                        room_building_combination = f"301 PUP Maevex"
                    elif building_code == 'MUD' and room_code == '633':
                        room_building_combination = f"633 MUDD Maevex"
                    else:
                        room_building_combination = f"No existing recorder"


                    if room_building_combination == "No existing recorder":
                        return None


                    session_start = datetime.combine(current_date, start_time.time())
                    session_end = datetime.combine(current_date, end_time.time())


                    session_data = {
                        'Title': course['Course_Identifier'],
                        'Recorder Name': room_building_combination,
                        'Date': session_start.strftime('%m/%d/%Y'),
                        'StartTime': session_start.strftime('%I:%M %p'),
                        'EndTime': session_end.strftime('%I:%M %p'),
                        'Presenter Description': '',
                        'Folder Id or Name': course['Folder'],
                        'isWebcast': course['Webcast'],
                    }
                    sessions.append(session_data)


            current_date += timedelta(days=1)


    except ValueError as e:
        print(f"Skipping row due to error: {e}. Row data: {course}")
        return None
    except Exception as e:
        print(f"Skipping row due to unexpected error: {e}. Row data: {course}")
        return None


    return sessions


def generate_files():
    fields = ['Course_Identifier', 'Class_Room_Code', 'Class_Building_Code', 'Class_Begin_Date', 'Class_End_Date',
            'Class_Begin_Time', 'Class_End_Time', 'Folder', 'Webcast', 'Class_Days_Code', 'Presenter Description']


    courses = []
    skipped_rows = []


    with open(input_fp, 'r') as csvfile:
        csv_reader = csv.DictReader(csvfile, fieldnames=fields)
        next(csv_reader)
        courses = [row for row in csv_reader]


        with open(skip_fp, 'w') as skipped_file:
            skipped_file.write("Skipped rows (Course names, Folder, Reason, Room Code, and Building Code):\n")
           
            for course in courses:
                sessions = generate_sessions(course)
               
                all_sessions = []
                if sessions:
                    all_sessions.extend(sessions)
                else:
                    skipped_file.write(f"Course Identifier: {course['Course_Identifier']}, Folder: {course['Folder']}, Reason: No existing recorder, Room Code: {course['Class_Room_Code']}, Building Code: {course['Class_Building_Code']}\n")




    for course in courses:
        sessions = generate_sessions(course)
        if sessions:
            all_sessions.extend(sessions)
        else:
            skipped_rows.append({
                'Course_Identifier': course['Course_Identifier'],
                'Folder': course['Folder'],
                'Reason': "No existing recorder",
                'Room_Code': course['Class_Room_Code'],
                'Building_Code': course['Class_Building_Code']
            })




    # Output CSV
    output_fields = ['Title', 'Recorder Name', 'Date', 'StartTime', 'EndTime', 'Presenter Description', 'Folder Id or Name', 'isWebcast']


    with open(output_fp, 'w', newline='') as csvfile:
        csv_writer = csv.DictWriter(csvfile, fieldnames=output_fields)
        #csv_writer.writeheader()


        for session in all_sessions:
            day_of_week = datetime.strptime(session['Date'], '%m/%d/%Y').strftime('%A')
            session['Title'] = f"{session['Title']} on {session['Date']} ({day_of_week})"


            csv_writer.writerow(session)


    print(f"CSV file '{output_fp}' has been generated.")






    with open(skip_fp, 'w') as skipped_file:
        skipped_file.write("Skipped rows (Course names, Folder, Reason, Room Code, and Building Code):\n")


        for skipped_course in skipped_rows:
            skipped_file.write(f"Course Identifier: {skipped_course['Course_Identifier']}, Folder: {skipped_course['Folder']}, Reason: {skipped_course['Reason']}, Room Code: {skipped_course['Room_Code']}, Building Code: {skipped_course['Building_Code']}\n")


    print(f"Skipped rows have been logged to '{skip_fp}'.")


window = tk.Tk()
window.title("Session Generator")


#Input CSV
input_btn = tk.Button(window, text="Select input CSV with headers", command=input_file)
input_btn.grid(row=0, column=0, padx=10, pady=10)
input_lbl = tk.Label(window, text="Input file: None")
input_lbl.grid(row=0, column=1, padx=10, pady=10)


#Ouput CSV
output_btn = tk.Button(window, text="Select output CSV destination", command=output_file)
output_btn.grid(row=1, column=0, padx=10, pady=10)
output_lbl = tk.Label(window, text="Output file: None")
output_lbl.grid(row=1, column=1, padx=10, pady=10)


#Skipped rows CSV
skip_btn = tk.Button(window, text="Select skipped rows destination", command=skipped_rows_file)
skip_btn.grid(row=2, column=0, padx=10, pady=10)
skip_lbl = tk.Label(window, text="Skipped rows file: None")
skip_lbl.grid(row=2, column=1, padx=10, pady=10)


# Run comparison button
compare_btn = tk.Button(window, text="Generate", command=generate_files)
compare_btn.grid(row=3, column=1, columnspan=2, pady=10)


# Result label
output_result_label = tk.Label(window, text="Results will be displayed here")
output_result_label.grid(row=4, column=0, columnspan=2, pady=10)


# Result label
skip_result_label = tk.Label(window, text="Results will be displayed here")
skip_result_label.grid(row=5, column=0, columnspan=2, pady=10)


#run main event loop

window.mainloop()
