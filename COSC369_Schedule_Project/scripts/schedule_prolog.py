"""Convert the two original scheduling inputs to Prolog facts and run sample queries.

Requires SWI-Prolog and PySwip. The C program remains the primary schedule generator.
"""
from pathlib import Path
import argparse
import re

ROOT = Path(__file__).resolve().parents[1]


def atom(value):
    return "'" + value.replace('\\', '\\\\').replace("'", "\\'") + "'"


def records(path, expected):
    with path.open(encoding='utf-8') as handle:
        for number, line in enumerate(handle, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            fields = [field.strip() for field in line.split('|')]
            if len(fields) != expected:
                raise ValueError(f'{path}:{number}: expected {expected} fields, got {len(fields)}')
            yield fields


def generate_facts():
    lines = ["% Generated from the project's two original local input files.",
             "% Quoted atoms preserve names, course codes and clock times."]
    for code, title, lecturer, days, start, end, room in records(ROOT / 'input/courses.txt', 7):
        lines.append(f'course({atom(code)}, {atom(title)}, {atom(lecturer)}, {atom(room)}).')
        for day in days.split(','):
            lines.append(f'class_meeting({atom(code)}, {atom(day.strip())}, {atom(start)}, {atom(end)}).')
    for lecturer, department, office, hours, availability, courses in records(ROOT / 'input/faculty.txt', 6):
        lines.append(f'faculty({atom(lecturer)}, {atom(department)}, {atom(office)}).')
        lines.append(f'required_hours({atom(lecturer)}, {float(hours)}).')
        for code in courses.split(','):
            lines.append(f'teaches({atom(lecturer)}, {atom(code.strip())}).')
        for block in availability.split(';'):
            day, spans = block.split('=', 1)
            for span in spans.split(','):
                start, end = span.strip().split('-', 1)
                lines.append(f'available({atom(lecturer)}, {atom(day.strip())}, {atom(start)}, {atom(end)}).')
    # Office hours are computed by the existing C program, not assumed to equal all availability.
    office_path = ROOT / 'output/office_hours.csv'
    if office_path.exists():
        import csv
        with office_path.open(newline='', encoding='utf-8') as handle:
            for row in csv.DictReader(handle):
                lines.append('office_hours({}, {}, {}, {}, {}).'.format(*[
                    atom(row[k]) for k in ('Faculty', 'Day', 'Start', 'End', 'Related Course')]))
    lines += [
        '', '% Reusable rules for querying the generated facts.',
        'who_teaches(Course, Lecturer) :- teaches(Lecturer, Course).',
        'office_hours_on(Day, Lecturer, Start, End) :- office_hours(Lecturer, Day, Start, End, _).',
        'classes_on(Day, Course, Start, End) :- class_meeting(Course, Day, Start, End).',
    ]
    target = ROOT / 'prolog/schedule_facts.pl'
    target.parent.mkdir(exist_ok=True)
    target.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return target


def query_facts(path):
    try:
        from pyswip import Prolog
    except ImportError as exc:
        raise SystemExit('PySwip is missing. Install SWI-Prolog, then run: python3 -m pip install pyswip') from exc
    prolog = Prolog()
    prolog.consult(str(path))
    examples = [
        ('Who teaches COSC 369?', "who_teaches('COSC 369', Lecturer)"),
        ('Office hours on Wednesday', "office_hours_on('Wednesday', Lecturer, Start, End)"),
        ('Classes on Tuesday', "classes_on('Tuesday', Course, Start, End)"),
    ]
    for title, query in examples:
        print('\n' + title)
        matches = list(prolog.query(query))
        if not matches:
            print('  No matching facts')
        for match in matches:
            print(' ', ', '.join(f'{key}={value}' for key, value in match.items()))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--generate-only', action='store_true', help='Generate Prolog facts without running queries')
    args = parser.parse_args()
    facts = generate_facts()
    print(f'Generated {facts.relative_to(ROOT)}')
    if not args.generate_only:
        query_facts(facts)


if __name__ == '__main__':
    main()
