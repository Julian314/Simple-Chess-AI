import csv
import numpy as np
model1 = []
model2 = []
model3 = []

with open('evaluations.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if abs(float(row["Stockfish"])) < 150:
            model1.append(abs(float(row["Stockfish"]) - float(row["ShessGPT_1"])))
            model2.append(abs(float(row["Stockfish"]) - float(row["ShessGPT_2"])))
            model3.append(abs(float(row["Stockfish"]) - float(row["ShessGPT_3"])))

print(f'model1: {sum(model1)/len(model1)}, model2: {sum(model2)/len(model2)}, model3: {sum(model3)/len(model3)}')
print(np.median(model1),np.median(model2),np.median(model3))
print(f'model1: {max(model1)} model2: {max(model2)}, model3: {max(model3)}')