import os 
import random

hasSmiley = {}
phases = ["training", "testing"]
for phase in phases:
    with open(f"./choose34/experimentFiles/{phase}.csv", "w") as f:
        f.write("pair,Left_Stim,Right_Stim,Correct_Response\n")
        for i in range(1, 9):
            imgs = os.listdir(f"./choose34/assets/pairs/pair{i}/{phase}")
            correct = random.randint(0, 1)
            if correct == 0:
                f.write(f"pair{i},{imgs[0]},{imgs[1]},left\n")
                f.write(f"pair{i},{imgs[1]},{imgs[0]},right\n")
                hasSmiley[imgs[0]] = True
            else:
                f.write(f"pair{i},{imgs[0]},{imgs[1]},right\n")
                f.write(f"pair{i},{imgs[1]},{imgs[0]},left\n")
                hasSmiley[imgs[1]] = True