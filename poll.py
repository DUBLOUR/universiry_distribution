import random
import string
import json
import nltk

class Student:
    id = 0
    name = ""
    prior = 0

    _MAX_PRIOR = 1000000

    def __init__(self, id, name, prior=_MAX_PRIOR):
        self.id = id
        self.name = name
        self.prior = _MAX_PRIOR

    def __lt__(a, b):
        if a.prior != b.prior:
            return a.prior < b.prior
        return a.name < b.name


class Teacher:
    name = ""
    cap = 0
    _tmp_cap = 0
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
            print("WARNING!\tdelStudent", self.name, self.students, id, name)


class Subject:
    name = ""
    teachers = list()

    def __init__(self, name, teachers):
        self.name = name
        self.teachers = teachers
            # empty object for case when places are over
        # self.teachers.append(Teacher("Out of game")) 


    def formLists(self, max_students=0):
        cnt_required = 0
        sum_cap = 0
        has_auto = 0

        for t in self.teachers:
            cnt_required += len(t.students)
            if t.cap != 0:
                sum_cap += t.cap
            else:
                has_auto += 1

        max_tmp_cap = cnt_required
        if max_students and has_auto:
            max_tmp_cap = (max_students - sum_cap + has_auto - 1) // has_auto

        for i in range(len(self.teachers)):
            if self.teachers[i].cap:
                self.teachers[i]._tmp_cap = self.teachers[i].cap
            else:
                self.teachers[i]._tmp_cap = max_tmp_cap

        other = []

        results = dict()
        for t in self.teachers:
            if not len(t.students):
                results[t.name] = []
                continue
            lst = sorted(t.students)

            if len(lst) < t._tmp_cap:
                results[t.name] = lst
                continue

            tmp0, tmp1 = [], []
            p = lst[t._tmp_cap].prior

            for x in lst:
                if x.prior < p:
                    tmp0.append(x)
                elif x.prior == p:
                    tmp1.append(x)
                else:
                    other.append(x)

            tmp1 = random.shuffle(tmp1)
            cnt = t._tmp_cap - len(tmp0)
            tmp0 += tmp0[:cnt]
            other += tmp0[cnt:]
            results[t.name] = tmp0

        if len(other):
            other = random.shuffle(other)
            for t in self.teachers:
                while other and len(results[t.name]) < t._tmp_cap:
                    results[t.name].append(other.pop())

        if len(other):
            results["Out of game"] = other
        return results


def parseResponse(raw, poll):
    n = len(poll.subjects)

    def getTeachers(subs):
        res = list()
        for i in range(len(subs)):
            for j in range(len(subs[i].teachers)):
                name = subs[i].teachers[j].name
                name = name.lower()
                res.append( (name,i,j) )
        return res

    def getSurnames(raw_sentence):
        tokens = nltk.word_tokenize(raw_sentence)
        res = []
        for t in tokens:
            if len(t) > 1:
                res.append(t.lower())
        return res

    def f(surname):
        sim, id = 1000, -1
        for x in range(len(teachers)):
            now_sim = nltk.edit_distance(surname, teachers[x][0])
            # print("\t", now_sim, surname, teachers[x][0])
            if now_sim < sim:
                sim = now_sim
                id = x
        # print()
        return sim, id

    
    teachers = getTeachers(poll.subjects)
    surnames = getSurnames(raw)
    # print(teachers)
    # print(surnames)

    if len(surnames) < n:
        return False, "Too few words"

    res = []
    for s in surnames:
        similarity, id = f(s)
        res.append((similarity, id))
    allow_rate = sorted(res)[n-1][0]

    prior, prefer = [], []
    cnt = 0
    for sim, id in res:
        if sim <= allow_rate and cnt < n:
            prior.append(teachers[id][1])
            prefer.append(teachers[id][2])
            cnt += 1

    # check = []
    # for i in range(n):
    #     check.append(poll.subjects[prior[i]].teachers[prefer[i]].name)

    return prior, prefer



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
    folder_pass = ""
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
        self.genPass()
        

    def genPass(self):
        self.folder_pass = createRandomPass(8)
        self.voting_pass = createRandomPass(16)
        self.admin_pass = createRandomPass(16)


    def importFromJson(self, config_string) -> bool:
        data = json.loads(config_string)
        
        if "title" not in data:
            return False

        if "subjects" not in data:
            return False

        title = str(data["title"])
        
        students = None
        if "students" in data:
            students = int(data["students"])

        open_stats = None
        if "open_results" in data:
            open_stats = bool(data["open_results"])

        subjects_raw = list(data["subjects"])
        if len(subjects_raw) < 1:
            return False

        subjects = []
        for x in subjects_raw:
            if ("name" not in x) or ("teachers" not in x):
                return False
            name = str(x["name"])
            t = list(x["teachers"])
            teachers_list = []

            if len(t) < 1:
                return False

            for now_t in t:
                if "name" not in now_t:
                    return False
                t_name = str(now_t["name"])
                t_cap = 0
                if "cap" in now_t:
                    try:
                        t_cap = int(now_t["cap"])
                    except:
                        pass

                # print("\t", t_name, t_cap)
                teachers_list.append(Teacher(t_name, t_cap))

            s = Subject(name, teachers_list)
            subjects.append(s)

        self.title = title
        self.expected_count_of_students = students
        self.open_stats = open_stats
        self.subjects = subjects
        self.is_close = False
        

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
            if r.prefer[i] >= len(self.subjects.teachers): 
                return False

        return True


    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)


    def showClass(self):
        res = dict()
        
        res["title"] = self.title
        res["students"] = self.expected_count_of_students
        res["open_stats"] = self.open_stats

        subs = list()
        for s in self.subjects:
            now_s = dict()
            now_s["name"] = s.name

            teachers = list()
            for t in s.teachers:
                name = t.name
                cap = "auto"
                if t.cap:
                    cap = str(t.cap)
                teachers.append({"name":name, "cap":cap})
            now_s["teachers"] = teachers
            subs.append(now_s)
        res["subjects"] = subs

        return json.dumps(res, indent="  ", ensure_ascii=False)


    def getResult(self):
        n = self.expected_count_of_students

        res = dict()
        for s in self.subjects:
            res[s.name] = s.formLists(n)

        return json.dumps(res, indent="  ", ensure_ascii=False)


    def checkResponse(self, prior, prefer):
        check = []
        n = len(prior)
        for i in range(n):
            check.append(self.subjects[prior[i]].teachers[prefer[i]].name)
        return check


    def parseResponse(self, sentence):
        prior, prefer = parseResponse(sentence, self)
        if prior == False:
            return prefer
        
        return self.checkResponse(prior, prefer)
        

# class EmployeeEncoder(json.JSONEncoder):
#         def default(self, o):
#             return o.__dict__


# print(EmployeeEncoder().encode(Poll))
# # employeeJSONData = json.dumps(employee, indent=4, cls=EmployeeEncoder)
# # print(employeeJSONData)

# # Let's load it using the load method to check if we can decode it or not.
# print("Decode JSON formatted Data")
# employeeJSON = json.loads(employeeJSONData)
# print(employeeJSON)


