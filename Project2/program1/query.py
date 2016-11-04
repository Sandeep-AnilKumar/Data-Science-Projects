import sys

def q1(cleaned_file):
    courses = []
    for line in cleaned_file:
        course_list = (line.split("-", 1)[1]).split('|')
        for course in course_list:
            courses.append(course.lower().strip())
    courses = list(set(courses))
    print("The distinct number of courses in the dataset are: - ", len(courses))
    return

def q2(cleaned_file):
    print("\nThe courses taught by Professor Mitchell Theys are:")
    for line in cleaned_file:
        name_courses = line.split('-', 1)
        if name_courses[0].strip() == "Theys":
            courses = name_courses[1].split('|')
            courses = [c.strip() for c in courses]
            print(", ".join(courses))
            break
    return

def q3(cleaned_file):
    name_to_course = {}
    threshold = -1
    for line in cleaned_file:
        if not line.strip():
            continue
        courses = line.split('-', 1)[1].split('|')
        if len(courses) >= 5:
            name = line.split('-', 1)[0].strip()
            name_to_course.setdefault(name, [])
            courses = [c.strip() for c in courses]
            name_to_course[name].append(courses)

    for prof1, course1 in name_to_course.items():
        for prof2, course2 in name_to_course.items():
            if prof2 != prof1:
                set1 = set(course1[0])
                set2 = set(course2[0])
                intersection = len(set.intersection(set1, set2))
                union = len(set1 or set2)
                temp = intersection / union
                if temp > threshold:
                    threshold = temp
                    prof_1 = prof1
                    prof_2 = prof2
    print ("\nTwo professors who have the most aligned teaching interests based on course titles are:")
    print(prof_1, "and", prof_2)
    return

in_file = open("cleaned.txt", 'r').read().splitlines()
q1(in_file)
q2(in_file)
q3(in_file)
