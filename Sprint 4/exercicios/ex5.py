with open("Sprint 4/exercicios/estudantes.csv", "r") as file:
    
    students = []

    for line in file.readlines():
        line = line.split(',')
        name = line[0]
        notes = [*map(lambda x: int(x.strip()), line[1:])]
        top_notes = sorted(notes, reverse=True)[:3]
        students.append(f"Nome: {name} Notas: {top_notes} Média: {round(sum(top_notes) / len(top_notes), 2):.2f}")


    for i in sorted(students):
        print(i)