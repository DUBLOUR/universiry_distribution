import poll

f = open("create_command_example.txt", "r")
res = ""
for s in f.readlines():
    res += s

p = poll.Poll(0, "", [])
p.importFromJson(res)
print(p.showClass())