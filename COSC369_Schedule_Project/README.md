# COSC 369 Faculty Schedule Generator

This project reads exactly two local input files and produces class-schedule and office-hours documents. The sample data uses Dr. Appolo Tankeh and reproduces the courses, times, rooms, and office hours shown in the supplied project image. The values are read from the files and are not hard-coded in the program.

## Requirements

- GCC (or another C11 compiler)
- GNU Make
- `ar` (normally installed with GNU Binutils)
- Python 3 with `python-docx` for the optional Word output

On Bowie State's Linux lab computers, GCC, Make, and `ar` should normally already be available. To install the optional Python package on a personal computer, run:

```bash
python3 -m pip install python-docx
```

## Compile and run

From the project directory:

```bash
make
make run
```

The executable accepts exactly two arguments:

```bash
./bin/schedule_generator input/courses.txt input/faculty.txt
```

It writes these files to `output/`:

- `class_schedule.csv`
- `office_hours.csv`
- `schedule.txt`

To also produce the formatted Word document:

```bash
make documents
```

This creates `output/Faculty_Schedule.docx`.

## Make targets

- `make` or `make all`: compile objects, create `lib/libschedule.a`, and link the executable.
- `make run`: build if necessary and run with the two sample input files.
- `make documents`: run the C program and generate the Word document.
- `make clean`: remove generated objects, library, executable, and schedule outputs.
- `make rebuild`: clean and compile again.

## Input formats

Both files use a pipe (`|`) delimiter so commas can safely appear inside day and course lists.

`input/courses.txt`:

```text
course_code|course_title|lecturer|days|start_time|end_time|room
```

Days are full names separated by commas. Times use 24-hour `HH:MM` format.

`input/faculty.txt`:

```text
lecturer|department|office|required_hours|availability|courses_taught
```

Availability uses `Day=HH:MM-HH:MM`; separate days with semicolons and multiple blocks on one day with commas. Lecturer names must match exactly across both files.

## Scheduling rule

For each faculty member, the program examines availability blocks in the order supplied. It rejects blocks that overlap the lecturer's class time, selects enough non-conflicting time to meet the required weekly total, and trims only the final block when needed. Each selected block is labeled with the nearest course taught by that lecturer on that day, or `General` when no same-day course exists. The output always includes the warning that instructors should not be interrupted during class times.

## Project organization

- `src/main.c`: command-line control flow
- `src/input.c`: input parsing and time utilities
- `src/scheduling.c`: validation and office-hour generation
- `src/output.c`: CSV and text output
- `include/scheduler.h`: shared data types and public function declarations
- `lib/libschedule.a`: static library created from the three reusable modules
- `scripts/generate_docx.py`: optional document formatter
- `report/COSC369_Project_Report.pdf`: written report

## Sample-data note

The included input files intentionally retain the sample courses and schedule supplied with the assignment. Keep the field order unchanged when editing the data.

## Midterm extension: Python and Prolog

The original C application, static library, and two local input files remain unchanged. An optional extension in `scripts/schedule_prolog.py` converts **the same two input files** into Prolog facts and also imports the office-hours output computed by the C program. The Prolog knowledge base is generated, not hard-coded.

To generate the knowledge base without installing Prolog:

```bash
make prolog-facts
```

This produces `prolog/schedule_facts.pl` containing `course`, `class_meeting`, `faculty`, `teaches`, `available`, and computed `office_hours` facts. It also defines `who_teaches`, `office_hours_on`, and `classes_on` rules.

To run the sample Prolog queries, first install **SWI-Prolog** and a matching-architecture Python installation, then install PySwip:

```bash
python3 -m pip install pyswip
make prolog-demo
```

Sample questions include: who teaches COSC 369, which office hours are on Wednesday, and which classes meet on Tuesday. Alternatively, open `prolog/schedule_facts.pl` in SWI-Prolog and query `who_teaches('COSC 369', Lecturer).` or `office_hours_on('Wednesday', Lecturer, Start, End).`.

**Important:** The C application is still the source of truth for selected office hours. Prolog's `available` facts describe *possible* office hours; `office_hours` facts reflect the actual selected schedule. The sample queries require SWI-Prolog/PySwip and have not been claimed as executed unless tested in that environment.

## GitHub submission and presentation

Upload the contents of this project folder to a GitHub repository, not just the ZIP archive. Submit the repository URL on Blackboard. For the presentation, demonstrate `make run`, show the generated schedule, explain the static library and Makefile, then demonstrate the Prolog facts and queries (if SWI-Prolog is installed). Explain that the project uses two locally stored input files rather than fetching information from the Internet.
