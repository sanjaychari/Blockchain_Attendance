def find_records(form, blockchain):
    for block in blockchain:
        print(block.data)
        condition = (block.data[0] == form.get("name") and
                    block.data[1] == form.get("date") and
                    block.data[2] == form.get("course") and
                    block.data[3] == form.get("year") and
                    len(block.data[4]) == int(form.get("number")))
        if condition:
            return block.data[4]
    return -1

def find_student_records_dates(form, blockchain):
    li = []
    for block in blockchain:
        print(block.data)
        condition = (block.data[1] == form.get("date"))
        if condition:
            li.append([block.data[2],block.data[4][int(form.get("number"))-1]])
    if(len(li) > 0):
        return li
    else:
        return -1
 
def find_student_records_courses(form, blockchain):
    li = []
    for block in blockchain:
        print(block.data)
        condition = (block.data[2] == form.get("course"))
        if condition:
            li.append([block.data[1],block.data[4][int(form.get("number"))-1]])
    if(len(li) > 0):
        return li
    else:
        return -1

def find_student_records_comp(form, blockchain):
    li = []
    dic = {}
    for block in blockchain:
        print(block.data)
        if(block.data[2] not in dic):
            if(isinstance(block.data[4],list)):
                if(not(block.data[4][int(form.get("number"))-1] == "A")):
                    dic[block.data[2]] = [1,1]
                else:
                    dic[block.data[2]] = [0,1]
        else:
            if(isinstance(block.data[4],list)):
                if(not(block.data[4][int(form.get("number"))-1] == "A")):
                    dic[block.data[2]][0] += 1
                    dic[block.data[2]][1] += 1
                else:
                    dic[block.data[2]][1] += 1
    for key in dic:
        li.append([key,str(dic[key][0])+"/"+str(dic[key][1]),float(dic[key][0])/float(dic[key][1])*100])
    if(len(li) > 0):
        return li
    else:
        return -1