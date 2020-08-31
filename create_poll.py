import random
import string

class Teacher:
    name = ""
    cap = 0

    def __init__(self, name, cap=0):
        self.name = name
        self.cap = cap


class Subject:
    name = ""
    teachers = list()

    def __init__(self, name, teachers):
        self.name = name
        self.teachers = teachers
            # empty object for case when places are over
        self.teachers.append(Teacher("Out of game")) 


class Response:
    owner_id = 0
    name = ""
    prior = list() # permutation from 0 to n-1
    prefer = list() 

    def __init__(self, id, name, n, prior, prefer):
        self.owner_id = id
        self.name = name
        self.prior = [x for x in range(n)]
        self.prefer = [0] * n


def createRandomPass(n):
    letters = string.ascii_letters + string.digits
    res = "".join(random.choice(letters) for i in range(n))
    return res


class Poll:
    owner_id = 0
    voting_pass = ""
    admin_pass = ""

    title = ""
    expected_count_of_students = 0
    open_stats = False  # statistic can watch somebody
    is_close = False    # Poll already finished
    subjects = list()
    responces = list()


    def __init__(self, id, title, subjects, students=0, open_stats=False):
        self.owner_id = id
        self.title = title
        self.expected_count_of_students = students
        self.open_stats = open_stats
        self.is_close = False

        self.voting_pass = createRandomPass(16)
        self.admin_pass = createRandomPass(16)


    def addResponce(r:Response) -> bool:
        responces.append(r)




