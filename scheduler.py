import json

classes = dict()
month = 'June'

#day:level min, level max, min age, max age, start time hour, start time minute,
# end time hour, end time minute, duration, class size, current enrollment, available
classes = {'Mo' : [[1, 1, 0, 6, 17, 0, 17, 30, 30, 4, 0, True, month, 5],
                       [1, 1, 0, 6, 17, 30, 18, 0, 30, 4, 0, True, month, 5],
                       [2, 4, 4, 6, 18, 0, 19, 0, 60, 6, 0, True, month, 5],
                       [5, 7, 7, 12, 18, 0, 19, 0, 60, 8, 0, True, month, 5],
                       [8, 10, 16, 100, 19, 0, 20, 0, 60, 8, 0, True, month, 5],
                       [11, 20, 7, 15, 19, 0, 20, 0, 60, 6, 0, True, month, 5]
                       ],
           'Tu' : [[1, 1, 0, 6, 17, 0, 17, 30, 30, 4, 0, True, month, 6],
                       [1, 1, 0, 6, 17, 30, 18, 0, 30, 4, 0, True, month, 6],
                       [2, 4, 4, 6, 18, 0, 19, 0, 60, 6, 0, True, month, 6],
                       [5, 7, 7, 12, 18, 0, 19, 0, 60, 8, 0, True, month, 6],
                       [8, 10, 16, 100, 19, 0, 20, 0, 60, 8, 0, True, month, 6],
                       [11, 20, 7, 15, 19, 0, 20, 0, 60, 6, 0, True, month, 6]
                       ],
           'We' : [[1, 1, 0, 6, 17, 0, 1730, 30, 4, 0, True, month, 7],
                       [1, 1, 0, 6, 17, 30, 18, 0, 30, 4, 0, True, month, 7],
                       [2, 4, 4, 6, 18, 0, 19, 0, 60, 6, 0, True, month, 7],
                       [5, 7, 7, 12, 18, 0, 19, 0, 60, 8, 0, True, month, 7],
                       [8, 10, 16, 100, 19, 0, 20, 0, 60, 8, 0, True, month, 7],
                       [11, 20, 7, 15, 19, 0, 20, 0, 60, 6, 0, True, month, 7]
                       ],
           'Th' : [[1, 1, 0, 6, 17, 0, 17, 30, 30, 4, 0, True, month, 8],
                       [1, 1, 0, 6, 17, 30, 18, 0, 30, 4, 0, True, month, 8],
                       [2, 4, 4, 6, 18, 0, 19, 0, 60, 6, 0, True, month, 8],
                       [5, 7, 7, 12, 18, 0, 19, 0, 60, 8, 0, True, month, 8],
                       [8, 10, 16, 100, 19, 0, 20, 0, 60, 8, 0, True, month, 8],
                       [11, 20, 7, 15, 19, 0, 20, 0, 60, 6, 0, True, month, 8]
                       ],
           'Fr' : [[1, 1, 4, 6, 15, 0, 15, 30, 30, 4, 0, True, month, 9],
                       [1, 1, 4, 6, 15, 30, 16, 0, 30, 4, 0, True, month, 9],
                       [2, 7, 7, 12, 15,00, 15, 45, 45, 6, 0, True, month, 9],
                       [2, 7, 7, 12, 15, 45, 16, 30, 45, 6, 0, True, month, 9],
                       [3, 7, 7, 10, 16, 0, 17, 0, 60, 6, 0, True, month, 9],
                       [8, 12, 11, 15, 16, 0, 17, 0, 60, 8, 0, True, month, 9],
                       [5, 10, 11, 15, 17, 0, 18, 0, 60, 8, 0, True, month, 9],
                       [11, 15, 16, 100, 17, 0, 18, 0, 60, 8, 0, True, month, 9]
                       ],
           'Sa' : [[10, 20, 16, 100, 9, 0, 10, 0, 60, 8, 0, True, month, 10],
                         [0, 2, 0, 5, 9, 0, 9, 30, 30, 4, 0, True, month, 10],
                         [10, 20, 10, 15, 10, 0, 11, 0, 60, 4, 0, True, month, 10],
                         [5, 10, 7, 9, 1000, 10, 45, 45, 6, 0, True, month, 10],
                         [10, 100, 16, 100, 11, 0, 12, 0, 60, 8, 0, True, month, 10],
                         [10, 100, 16, 100, 11, 0, 12, 0, 60, 8, 0, True, month, 10]
                         ],
           'Su' : [[10, 100, 16, 100, 9, 0, 10, 0, 60, 8, 0, True, month, 11],
                       [10, 100, 16, 100, 9, 0, 10, 0, 60, 8, 0, True, month, 11],
                       [0, 2, 0, 2, 9, 0, 9, 0, 30, 4, 0, True, month, 11],
                       [0, 5, 0, 5, 9, 30, 10, 15, 45, 4, 0, True, month, 11],
                       [10, 100, 16, 100, 10, 0, 11, 0, 60, 8, 0, True, month, 11],
                       [5, 15, 10, 15, 10, 0, 11, 0, 60, 8, 0, True, month, 11],
                       [5, 10, 7, 9, 10, 15, 11, 0, 45, 6, 0, True, month, 11],
                       [0, 2, 0, 5, 11, 00, 11, 30, 30, 4, 0, True, month, 11],
                       [10, 100, 16, 100, 11, 0, 12, 0, 60, 8, 0, True, month, 11],
                       [0, 5, 0, 5, 12, 0, 12, 30, 30, 6, 0, True, month, 11],
                       [10, 100, 16, 100, 12, 0, 13, 0, 60, 8, 0, True, month, 11],
                       [6, 10, 10, 15, 12, 30, 13, 0, 30, 6, 0, True, month, 11]
                       ]}

def get_students():

    with open('students.json') as student_file:
        students = json.load(student_file)

    return students

def do_the_schedule(students):

    schedule = {}
    schedule['sessions'] = []

    for s in students['student_list']['student']:
    #iterate through student list
        sessionFound = False

        for day, times in classes.items():
        #iterate through each day
            for session in times:

                if (session[9]) and not (sessionFound):
                #check if available

                    if (int(session[0]) <= int(s['level']) <= int(session[1])) and \
                            (int(session[2]) <= int(s['age']) <= int(session[3])):

                        session_info = {}

                        session_info = {'firstName': s['firstName'],
                                        'lastName': s['lastName'],
                                        'month': session[10],
                                        'date': session[13],
                                        'dayOFTheWeek': day,
                                        'level': s['level'],
                                        'startTimeHour': session[4],
                                        'startTimeMinutes': session[5],
                                        'endTimeHour': session[6],
                                        'endTimeMinutes': session[7]
                                        }

                        schedule['sessions'].append(session_info)
                        sessionFound = True

    with open('result.json', 'w') as fp:
        json.dump(schedule, fp, ensure_ascii=True)

    return schedule


def display_schedule(students):
    schedule = do_the_schedule(get_students())


