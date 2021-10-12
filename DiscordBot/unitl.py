
####FUUUUUUUUUUUUUUCK ALL OF THIS IS POINTLESS

print("open Worked")

# ord() to go from char to int
# chr to go from int to char

start = 97
end = 122

lines = []
with open("serviceInfo.txt") as f:
    for line in f:
        for i in range(0,7):
            #print("i is: " + line[i].lower())
            if ord(line[i].lower()) >= start and ord(line[i].lower()) <= end:
                lines.append(line)
                break
                

print(len(lines))

with open("smallerServiceFile.txt","w") as f:
    for i in lines:
        f.write(i)



