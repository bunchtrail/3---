import argparse
import subprocess
import os

def main():
    parser = argparse.ArgumentParser(description="Основная программа для запуска задач проекта.")
    parser.add_argument('task', choices=['1', '2', '3'], help="Задача для запуска: 1, 2, 3", nargs='?')
    args = parser.parse_args()

    task_scripts = {
        '1': 'task1/markov_chain_analysis.py',
        '2': 'task2/transition_analysis.py',
        '3': 'task3/genetic_algorithm.py'
    }

    if not args.task:
        print("Выберите задачу для запуска:")
        for key, script in task_scripts.items():
            print(f"{key}: {script}")
        selected_task = input("Введите номер задачи (1, 2 или 3): ").strip()
    else:
        selected_task = args.task

    if selected_task in task_scripts:
        script_path = os.path.join(os.path.dirname(__file__), task_scripts[selected_task])
        subprocess.run(["python", script_path])
    else:
        print("Пожалуйста, введите номер задачи для запуска: 1, 2 или 3.")

if __name__ == "__main__":
    main()
