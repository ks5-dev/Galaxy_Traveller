import os
def write_score(score) :
    with open("score.txt", "a") as file:
        file.write(" "+str(score))
        file.close()

def receive_score():
    out = []
    with open("score.txt", "r") as file:
    
        line = file.readline()  # scores are one line
        scores = [int(s) for s in line.split(" ")]  # read scores as integers
        file.close()
    out.append(str(max(scores)))
    out.append(str(scores[-1]))
    return out