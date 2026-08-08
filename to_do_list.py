import json

def incarca_lista():
    try:
        with open("task.json","r") as f:
            return json.load(f)
     
    except FileNotFoundError:
        return []    
    except json.decoder.JSONDecodeError:
        return []

def salveaza_lista(taskuri):
    with open("task.json", "w") as f:
        json.dump(taskuri, f, indent=4)
    
def afiseaza_taskuri(taskuri):
    if not taskuri:
        print("\n Nu ai niciun task salvat.")
        return
    print("\n --LISTA DE TASKURI--")
    index=1
    for task in taskuri:
        status="[X]" if task['completat'] else "[ ]"
        print(f"{index}.{status} [{task['prioritate']}] {task['titlu']} ")
        index+=1
        

def adauga_task(taskuri):
    titlu=input("Introdu un task nou: ")
    if titlu:
        print("\nAlege o prioritate:1. Scazuta,2. Medie,3. Ridicata")
        prio=input("Optiune: ").strip()
        prioritati={'1':'Scazuta','2':'Medie','3':'Ridicata'}
        prioritate=prioritati.get(prio)
        task = {'titlu': titlu, 'completat': False,'prioritate':prioritate}
        
        taskuri.append(task)
        salveaza_lista(taskuri)
        print("Task adaugat cu succes!")
    else:
        print("Titlul nu poate fi gol!")

def marcheaza_finalizat(taskuri):
    if not taskuri:
        print("\nNu ai niciun task de sters!")
        return
    afiseaza_taskuri(taskuri)
    
    try:
        nr=int(input("\nIntrodu numarul taskului de finalizat : " ))
        if 1<=nr<=len(taskuri):
            taskuri[nr-1]['completat']=True
            salveaza_lista(taskuri)
            print("Task marcat ca si finalizat!")
        else:
            print("introdu un numar care sa exista in lista de taskuri")
    except ValueError:
        print("introdu un numar valid!")

def sterge_task(taskuri):
    if not taskuri:
        print("\nNu ai niciun task de sters!")
        return
    afiseaza_taskuri(taskuri)
    try:
        nr=int(input("\nIntrodu numarul taskului de sters : " ))
        if 1<=nr<=len(taskuri):
            taskuri.pop(nr-1)
            salveaza_lista(taskuri)
            print("Task-ul a fost sters cu succes!")
        else:
            print("introdu un numar care sa exista in lista de taskuri")
    except ValueError:
            print("introdu un numar valid!")




def main():
    taskuri=incarca_lista()

    while True:
        print("\n----To-Do List----")
        print("Avem urmatoarele optiuni!")
        print("1. Vezi task-urile")
        print("2. Adauga task")
        print("3. Marcheaza task ca si finalizat")
        print("4. Sterge task")
        print("5. Iesire")
        
        opt=input("Alege o optiune (1-5): ").strip()
        
        if opt=='1':
            afiseaza_taskuri(taskuri)
        elif opt=='2':
            adauga_task(taskuri)
        elif opt=='3':
            marcheaza_finalizat(taskuri)
        elif opt=='4':
            sterge_task(taskuri)
        elif opt=='5':
            print("La revedere !")
            break
        else:
            print("Optiune invalida! Incearca din nou.")
        

if __name__=='__main__':
    main()