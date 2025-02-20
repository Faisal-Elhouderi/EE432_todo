# task.py
PRIORITY_VALUES = {'High': 3, 'Medium': 2, 'Low': 1}

class Task:
    def __init__(self, description, priority_str, status=False):
        self.description = description
        self.priority_str = priority_str
        self.priority = PRIORITY_VALUES[priority_str]
        self.status = status

    def __repr__(self):
        return f"Task(description={self.description}, priority={self.priority_str}, status={self.status})"