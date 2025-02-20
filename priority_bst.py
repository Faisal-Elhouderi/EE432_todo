from doubly_linked_list import DoublyLinkedList, Node


class BSTNode:
    def __init__(self, priority):
        self.priority = priority
        self.tasks = DoublyLinkedList()
        self.left = None
        self.right = None

class PriorityBST:
    def __init__(self):
        self.root = None

    def insert(self, task):
        self.root = self._insert(self.root, task.priority, task)

    def _insert(self, node, priority, task):
        if not node:
            new_node = BSTNode(priority)
            new_node.tasks.append(Node(task))
            return new_node
        if priority > node.priority:
            node.left = self._insert(node.left, priority, task)
        elif priority < node.priority:
            node.right = self._insert(node.right, priority, task)
        else:
            node.tasks.append(Node(task))
        return node

    def remove_task(self, task):
        priority = task.priority
        node = self._find_node(priority)
        if node:
            current = node.tasks.head
            prev = None
            while current:
                if current.task == task:
                    if prev:
                        prev.next = current.next
                        if current.next:
                            current.next.prev = prev
                        else:
                            node.tasks.tail = prev
                    else:
                        node.tasks.head = current.next
                        if node.tasks.head:
                            node.tasks.head.prev = None
                        else:
                            node.tasks.tail = None
                    if not node.tasks.head:
                        self._delete_bst_node(priority)
                    return True
                prev = current
                current = current.next
        return False

    def _find_node(self, priority):
        current = self.root
        while current:
            if priority == current.priority:
                return current
            elif priority > current.priority:
                current = current.left
            else:
                current = current.right
        return None

    def _delete_bst_node(self, priority):
        self.root = self._delete_node(self.root, priority)

    def _delete_node(self, node, priority):
        if not node:
            return node
        if priority > node.priority:
            node.left = self._delete_node(node.left, priority)
        elif priority < node.priority:
            node.right = self._delete_node(node.right, priority)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            temp = self._min_value_node(node.right)
            node.priority = temp.priority
            node.tasks = temp.tasks
            node.right = self._delete_node(node.right, temp.priority)
        return node

    def _min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def traverse_in_order(self):
        tasks = []
        self._in_order(self.root, tasks)
        return tasks

    def _in_order(self, node, tasks):
        if node:
            self._in_order(node.left, tasks)
            current = node.tasks.head
            while current:
                tasks.append(current.task)
                current = current.next
            self._in_order(node.right, tasks)
