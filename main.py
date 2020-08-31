import poll
#import nltk
#nltk.download('punkt')

# sentence = "А папа у Васи, силён-силёніч в мат'ематике"
# tokens = nltk.word_tokenize(sentence)
# print(tokens)

# edit_distance
# exit()

f = open("create_command_example.txt", "r")
res = ""
for s in f.readlines():
    res += s

p = poll.Poll(0, "", [])
p.importFromJson(res)
#print(p.showClass())
print(p.getResult())

req = """браганець, мулян, 
павчук; OchenSilnoAru
 веклич
тімчишин килишенко лолАру"""

print(p.parseResponse(req))