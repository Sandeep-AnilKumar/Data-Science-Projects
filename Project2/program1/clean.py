import sys
import re
import string

# dictionary to store clean data.
cleaned_data = {}
# list of professors
professors = []
# list of courses
courses = []


def createdict(profname, course_list):
    new_course_list = []
    is_course_match = False
    profname = profname.title()
    prof_courses = course_list.split('|')
    prof_courses = [course.strip() for course in prof_courses]
    if profname not in cleaned_data:
        cleaned_data.setdefault(profname, [])

    for c in prof_courses:
        # replace & with and
        if '&' in c:
            c = c.replace('&', 'and ')
        # replace intro. or intro with introduction
        matcher = re.match("intro\.?", c)
        if matcher:
            c = re.sub("intro\.?", "introduction ", c)
        # replace or make all roman numerals capitals.
        matcher = re.match(r"\bi+\b", c.lower())
        if matcher:
            c = c.lower()
            c = re.sub(r"\bi\b", "I", c)
            c = re.sub(r"\bii\b", "II", c)
            c = re.sub(r"\biii\b", "III", c)

        # remove all punctuation marks.
        punctuation_regex = re.compile('[%s]' % re.escape(string.punctuation))
        c = punctuation_regex.sub('', c)

        c_split = c.split()
        c_word_array = []
        # make only non roman numeral words as "title", roman numerals as "uppercase".
        for c_split_constituent in c_split:
            matcher = re.match(r"\bi+\b", c_split_constituent.lower())
            if matcher:
                c_split_constituent = c_split_constituent.upper()
            else:
                c_split_constituent = c_split_constituent.title()
            c_word_array.append(c_split_constituent)

        c = (" ".join(c_word for c_word in c_word_array))

        if not courses:
            courses.append(c)
        is_course_match = False
        if c in courses:
            is_course_match = True
        else:
            # calculate courses similarity using edit distance using DP.
            for c2 in courses:
                c_length = len(c)
                c2_length = len(c2)
                table = [[0 for x in range(c2_length + 1)] for x in range(c_length + 1)]
                for i in range(c_length + 1):
                    table[i][0] = i
                for j in range(c2_length + 1):
                    table[0][j] = j
                for i in range(1, c_length + 1):
                    for j in range(1, c2_length + 1):
                        if c[i - 1] == c2[j - 1]:
                            table[i][j] = table[i - 1][j - 1]
                        else:
                            table[i][j] = 1 + min(table[i][j - 1], table[i - 1][j], table[i - 1][j - 1])
                distance = table[i][j]
                if distance <= 2:
                    is_course_match = True
                    c = c2
                    break
        if not is_course_match:
            courses.append(c)
        new_course_list.append(c)
    cleaned_data[profname] = cleaned_data[profname] + new_course_list
    return

# output file where the cleaned data is stored.
out = open("cleaned.txt", "w")

# input file to read the data.
inFile = sys.argv[1]
file_buffer = open(inFile, "r").read().splitlines()

for line in file_buffer:
    if not line.strip():
        continue
    # separate the prof names and course lists.
    separator = line.split('-', 1)
    # if the professor name has comma, since we only need last name, we take only that.
    prof = separator[0].strip()
    if ',' in prof:
        prof = (prof.split(',')[0]).strip()
        # if professor name has a space in the last name, take only the last part from it.
        if ' ' in prof:
            prof = (prof.split()[-1]).strip()
        # if professor name has a '.' in the last name, take only the last part form it.
        elif '.' in prof:
            prof = (prof.split('.')[-1]).strip()
    # if professor name is in firstName.lastName format, take only lastName.
    elif '.' in prof:
        prof = ((prof.split('.')[-1]).split()[-1]).strip()
    # if professor name is in firstName lastName format, take only lastName.
    elif ' ' in prof:
        prof = (prof.split()[-1]).strip()
    else:
        prof = prof.strip()
    # create a dictionary of professor to their courses.
    createdict(prof, separator[1].strip())

for key, value in cleaned_data.items():
    professors.append(key)
    # sort the courses list
    value = list(set(value))
    value.sort()
    cleaned_data[key] = value

professors.sort()
for name in professors:
    out.write(name + " - " + ("|".join(cleaned_data[name]))+"\n")

