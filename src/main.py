import subprocess

def run_task(task_number):
    if task_number == 1:
        subprocess.run(["python", "src/task1/1task.py"])
    elif task_number == 2:
        subprocess.run(["python", "src/task2/2task.py"])
    elif task_number == 3:
        subprocess.run(["python", "src/task3/3task.py"])
    elif task_number == 4:
        subprocess.run(["python", "src/task4/task4.py"])
    else:
        print(f"Задача {task_number} не найдена.")

def main():
    while True:
        print("\nВыберите задачу для запуска:")
        print("1. Задача 1 - построение цепи Маркова")
        print("2. Задача 2 - анализ цепи Маркова")
        print("3. Задача 3 - генетический алгоритм")
        print("4. Задача 4 - задача коммивояжера")
        print("0. Выход")
        
        try:
            task_number = int(input("Введите номер задачи: "))
            if task_number == 0:
                print("Выход из программы.")
                break
            run_task(task_number)
        except ValueError:
            print("Некорректный ввод. Пожалуйста, введите номер задачи.")

if __name__ == "__main__":
    main()