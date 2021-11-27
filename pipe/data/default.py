def default_pipe(data, config):
    subjects = config.get("subjects")
    mutated_data = []
    for row in data:
        # Nest the subjects defined in config into a single dict
        # and add it to mutated_row with the key "Subjects".
        row_subjects = {k: int(v) for k, v in row.items() if k in subjects and bool(v)}
        mutated_row = {k: v for k, v in row.items() if k not in subjects}
        mutated_row["Subjects"] = row_subjects
        mutated_data.append(mutated_row)

    return mutated_data


def marks_validator_pipe(data, config):
    """
    Pipe to validate the marks' entries for every student.
    Checks happening here:
    1. If marks for a particular subject exceed the maximum possible marks
    """
    subjects = config.get("subjects")
    for row in data:
        if "Subjects" in row:
            for k, v in row["Subjects"].items():
                if v > subjects[k]:
                    print(
                        f"VALIDATION ERROR: '{k}' subject of {row.get('Name')} has more marks than the max possible marks."
                    )
                    exit(1)
    return data


def percentage_and_total_marks_pipe(data, config):
    """
    Pipe to calculate maximum marks possible, total marks and percentage obtained by the student.

    1. Total marks obtained are available in the 'TotalMarksObtained' key.
    2. Maximum marks possible for the student are available in the 'MaxMarks' key.
    3. Percentage obtained is available in the 'Percentage' key.
    """
    mutated_data = []
    subjects = config.get("subjects")
    for row in data:
        max_marks = 0
        marks_obtained = 0
        student_subjects: dict = row.get("Subjects")
        for [subject, marks] in student_subjects.items():
            marks_obtained += marks
            max_marks += subjects[
                subject
            ]  # .get is not required since the subject should exist in the dictionary.
        percentage = round(100 * marks_obtained / max_marks, 2)
        mutated_row = dict(row)
        mutated_row["TotalMarksObtained"] = marks_obtained
        mutated_row["MaxMarks"] = max_marks
        mutated_row["Percentage"] = percentage
        mutated_data.append(mutated_row)
    return mutated_data
