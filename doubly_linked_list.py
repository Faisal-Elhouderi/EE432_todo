class Node:
    def __init__(self, task):
        self.task = task
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, task_node):
        if not self.head:
            self.head = task_node
            self.tail = task_node
        else:
            task_node.prev = self.tail
            self.tail.next = task_node
            self.tail = task_node

    def delete(self, node):
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next
        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev

    def to_list(self):
        tasks = []
        current = self.head
        while current:
            tasks.append(current.task)
            current = current.next
        return tasks
