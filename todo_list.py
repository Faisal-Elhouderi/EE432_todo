from doubly_linked_list import DoublyLinkedList, Node
from hash_table import HashTable
from priority_bst import PriorityBST
from task import PRIORITY_VALUES, Task


class ToDoList:
    def __init__(self):
        self.tasks_list = DoublyLinkedList()
        self.hash_table = HashTable()
        self.priority_bst = PriorityBST()

    def add_task(self, description, priority_str, status=False):
        if self.hash_table.get(description):
            return False
        try:
            priority = PRIORITY_VALUES[priority_str]
        except KeyError:
            return False
        new_task = Task(description, priority_str, status)
        new_node = Node(new_task)
        self.tasks_list.append(new_node)
        self.hash_table.add(description, new_node)
        self.priority_bst.insert(new_task)
        return True

    def delete_task(self, description):
        node_to_delete = self.hash_table.get(description)
        if not node_to_delete:
            return False
        self.tasks_list.delete(node_to_delete)
        self.hash_table.delete(description)
        self.priority_bst.remove_task(node_to_delete.task)
        return True

    def search_task(self, description):
        node = self.hash_table.get(description)
        return node.task if node else None

    def display_tasks(self, sort_by='insertion'):
        if sort_by == 'insertion':
            return self.tasks_list.to_list()
        elif sort_by == 'priority':
            return self.priority_bst.traverse_in_order()
        return []

    def display_filtered(self, status=None):
        tasks = self.tasks_list.to_list()
        if status is not None:
            return [task for task in tasks if task.status == status]
        return tasks
