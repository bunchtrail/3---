import argparse
import subprocess

def main():
    parser = argparse.ArgumentParser(description="Основная программа для запуска задач проекта.")
    parser.add_argument('task', choices=['task1', 'task2', 'task3'], help="Задача для запуска: task1, task2, task3")
    args = parser.parse_args()

    if args.task == 'task1':
        subprocess.run(["python", "src/task1/1task.py"])
    elif args.task == 'task2':
        subprocess.run(["python", "src/task2/2task.py"])
    elif args.task == 'task3':
        subprocess.run(["python", "src/task3/3task.py"])
    else:
        print("Неизвестная задача. Выберите task1, task2 или task3.")

if __name__ == "__main__":
    main()
