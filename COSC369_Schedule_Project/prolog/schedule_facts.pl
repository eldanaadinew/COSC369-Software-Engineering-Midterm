% Generated from the project's two original local input files.
% Quoted atoms preserve names, course codes and clock times.
course('COSC 631', 'Database Management', 'Dr. Appolo Tankeh', 'CS 313').
class_meeting('COSC 631', 'Wednesday', '17:00', '19:30').
course('COSC 369', 'Software Engineering I', 'Dr. Appolo Tankeh', 'CS 108').
class_meeting('COSC 369', 'Tuesday', '09:30', '10:45').
class_meeting('COSC 369', 'Thursday', '09:30', '10:45').
course('COSC 330', 'Systems Programming I', 'Dr. Appolo Tankeh', 'CS 311').
class_meeting('COSC 330', 'Monday', '09:30', '10:45').
class_meeting('COSC 330', 'Wednesday', '09:30', '10:45').
faculty('Dr. Appolo Tankeh', 'Computer Science', 'CS 108').
required_hours('Dr. Appolo Tankeh', 8.75).
teaches('Dr. Appolo Tankeh', 'COSC 631').
teaches('Dr. Appolo Tankeh', 'COSC 369').
teaches('Dr. Appolo Tankeh', 'COSC 330').
available('Dr. Appolo Tankeh', 'Monday', '10:45', '13:00').
available('Dr. Appolo Tankeh', 'Tuesday', '10:45', '13:00').
available('Dr. Appolo Tankeh', 'Wednesday', '10:45', '13:00').
available('Dr. Appolo Tankeh', 'Wednesday', '15:00', '17:00').
office_hours('Dr. Appolo Tankeh', 'Monday', '10:45', '13:00', 'COSC 330').
office_hours('Dr. Appolo Tankeh', 'Tuesday', '10:45', '13:00', 'COSC 369').
office_hours('Dr. Appolo Tankeh', 'Wednesday', '10:45', '13:00', 'COSC 330').
office_hours('Dr. Appolo Tankeh', 'Wednesday', '15:00', '17:00', 'COSC 631').

% Reusable rules for querying the generated facts.
who_teaches(Course, Lecturer) :- teaches(Lecturer, Course).
office_hours_on(Day, Lecturer, Start, End) :- office_hours(Lecturer, Day, Start, End, _).
classes_on(Day, Course, Start, End) :- class_meeting(Course, Day, Start, End).
