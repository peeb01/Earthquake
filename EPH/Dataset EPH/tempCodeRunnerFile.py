column = ['SUN', 'MERCURY', 'VENUS', 'MOON', 'MARS', 'SATURN', 'JUPITER', 'URANUS', 'NEPTUNE']
pos = ['x',' y', 'z']
col = [f'{column[i]}_{pos[j]}' for i in range(len(column)) for j in range(len(pos))]
print(col)
print(len(col)/3)
