import poll

teachers_file = "teachersOM3.json"
students_file = "studentsOM3.txt"
randomSeed = "abHkk1o3Ac-BKVup"

teachersJson = ""
with open(teachers_file, "r") as f:
    for s in f.readlines():
        teachersJson += s

wantedRaw = dict()
with open(students_file, "r") as f:
    for s in f.readlines():
        surname, wantedTeachers = s.split(maxsplit=1)
        wantedRaw[surname] = wantedTeachers



p = poll.Poll(0, "", [], randomSeed)
p.importFromJson(teachersJson)
print(p.showClass())


i = 1
for surname, wantedTeachers in wantedRaw.items():
    r = poll.Response()
    r.name = surname
    r.id = i
    i += 1
    r.prior, r.prefer = poll.parseResponse(wantedTeachers, p)
    print(surname, p.checkResponse(r.prior, r.prefer), p.addResponse(r), sep='\t')
    

print(p.getResult())

