import json
import sys
from Nicole.task_schema import NicoleTask


def load_task(file_path):
    try:
        with open(file_path, 'r') as f:
            task = json.load(f)
            return task
    except Exception as e:
        print(f"Error loading task: {e}")
        sys.exit(1)


def validate_task(task):
    try:
        NicoleTask.validate(task)
        print("Task validation passed.")
    except Exception as e:
        print(f"Validation error: {e}")
        sys.exit(1)


def print_plan(task):
    print("Generated plan:")
    # Assuming task plan is done here
    # This is a placeholder for whatever task planning logic is required


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python runner.py <path_to_task_json>")
        sys.exit(1)

    task_file = sys.argv[1]
    task = load_task(task_file)
    validate_task(task)
    print_plan(task)