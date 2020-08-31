import random
import string

class Student:
    id = 0
    name = ""
    prior = 0

    _MAX_PRIOR = 1000000

    def __init__(self, id, name, prior=_MAX_PRIOR):
        self.id = id
        self.name = name
        self.prior = _MAX_PRIOR


class Teacher:
    name = ""
    cap = 0
    students = list()

    def __init__(self, name, cap=0):
        self.name = name
        self.cap = cap
        self.students = list()


    def addStudent(self, id, name, prior=None):
        if prior == None:
            s = Student(id, name)
        else:
            s = Student(id, name, prior)
        self.students.append(s)


    def delStudent(self, id, name, prior=None):
        if prior == None:
            s = Student(id, name)
        else:
            s = Student(id, name, prior)
        
        try:
            id = self.students.remove(s)
        except:
            print("MEM!\tdelStudent", self.name, self.students, id, name)



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
    cnt_responces = 0
    #responces = list()


    def __init__(self, id, title, subjects, students=0, open_stats=False):
        self.owner_id = id
        self.title = title
        self.expected_count_of_students = students
        self.open_stats = open_stats
        self.is_close = False
        self.cnt_responces = 0

        self.voting_pass = createRandomPass(16)
        self.admin_pass = createRandomPass(16)


    def importFromJson(self, json):
        pass


    def addResponce(self, r:Response) -> bool:
        if not self.validate_response(r):
            return False

        t = self.subjects.teachers
        for i in range(len(r)):
            t[ prefer[i] ].addStudent(r.owner_id, r.name, prior[i])
            # for j in range(len(t)):
            #     if j == prefer[i]:
            #         t[j].addStudent(r.owner_id, r.name, prior[i])
            #     else:
            #         t[j].addStudent(r.owner_id, r.name)

        #responces.append(r)
        self.cnt_responces += 1
        return True


    def delResponce(self, r:Response):
        t = self.subjects.teachers
        for i in range(len(r)):
            t[ prefer[i] ].delStudent(r.owner_id, r.name, prior[i])
        
        self.cnt_responces -= 1


    def validate_response(self, r:Response) -> bool:
        n = len(r)
        if n != len(self.subjects): 
            return False

        used = [False]*n
        for i in r.prior:
            has_prior[i] = True
        if False in used:
            return False

        for i in range(n):
            if r.prefer[i] >= len(self.subjects.teachers)-1: 
                # "-1" because we has 1 faik teacher
                return False

        return True


    def getResults(self):
        pass





