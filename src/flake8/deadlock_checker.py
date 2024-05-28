import ast
import os


class DeadlockChecker:
    def __init__(self, tree, filename):
        self.tree = tree
        self.filename = filename
        self.lock_graph = {}
        self.event_graph = {}
        self.join_graph = {}
        self.threads = self.identify_threads()
        self.build_graphs()

    def run(self):
        deadlocks = self.detect_deadlock(self.lock_graph)
        deadlocks.extend(self.detect_deadlock(self.event_graph))
        deadlocks.extend(self.detect_deadlock(self.join_graph))
        for deadlock in deadlocks:
            yield (deadlock[1], deadlock[2], "DLC001 potential deadlock detected", type(self))

    def identify_threads(self):
        threads = {}
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr in {'Thread',
                                                                                                          'Process'}:
                for kw in node.keywords:
                    if kw.arg == 'target' and isinstance(kw.value, ast.Name):
                        thread_func = kw.value.id
                        threads[thread_func] = []
        return threads

    def build_graphs(self):
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef) or isinstance(node, ast.ClassDef):
                for func_node in ast.walk(node):
                    if isinstance(func_node, ast.FunctionDef):
                        func_name = func_node.name
                        current_locks = []
                        current_events = []
                        for n in ast.walk(func_node):
                            if isinstance(n, ast.With):
                                for item in n.items:
                                    lock_name = self.get_lock_name(item.context_expr)
                                    if lock_name:
                                        if lock_name in [l[0] for l in current_locks]:
                                            self.add_to_graph(self.lock_graph, (lock_name, n.lineno, n.col_offset),
                                                              (lock_name, n.lineno, n.col_offset))
                                        else:
                                            current_locks.append((lock_name, n.lineno, n.col_offset))
                                            self.add_to_graph(self.lock_graph, current_locks[-1], current_locks[-1])
                            if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute):
                                lock_name = self.get_lock_name(n.func.value)
                                process_name = self.get_process_name(n.func.value)
                                if n.func.attr in {'acquire', 'wait'}:
                                    if lock_name:
                                        current_locks.append((lock_name, n.lineno, n.col_offset))
                                        if len(current_locks) > 1:
                                            self.add_to_graph(self.lock_graph, current_locks[-2], current_locks[-1])
                                elif n.func.attr in {'release', 'set'}:
                                    if lock_name in [l[0] for l in current_locks]:
                                        current_locks = [l for l in current_locks if l[0] != lock_name]
                                elif n.func.attr == 'wait':
                                    event_name = self.get_event_name(n.func.value)
                                    if event_name:
                                        current_events.append((event_name, n.lineno, n.col_offset))
                                        if len(current_events) > 1:
                                            self.add_to_graph(self.event_graph, current_events[-2], current_events[-1])
                                elif n.func.attr == 'set':
                                    event_name = self.get_event_name(n.func.value)
                                    if event_name in [l[0] for l in current_events]:
                                        current_events = [l for l in current_events if l[0] != event_name]
                                elif n.func.attr == 'join':
                                    if process_name:
                                        current_joins.append((process_name, n.lineno, n.col_offset))
                                        if len(current_joins) > 1:
                                            self.add_to_graph(self.join_graph, current_joins[-2], current_joins[-1])
                                        if len(current_joins) > 1 and current_joins[-1][0] == current_joins[-2][0]:
                                            self.add_to_graph(self.join_graph, current_joins[-1], current_joins[-2])

    def get_lock_name(self, node):
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
            return f"{node.value.id}.{node.attr}"
        return None

    def get_event_name(self, node):
        if isinstance(node, ast.Name):
            return node.id
        return None

    def get_process_name(self, node):
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
            return f"{node.value.id}.{node.attr}"
        return None

    def add_to_graph(self, graph, node1, node2):
        if node1[0] not in graph:
            graph[node1[0]] = set()
        graph[node1[0]].add(node2)

    def detect_deadlock(self, graph):
        visited = set()
        rec_stack = set()
        deadlocks = []

        def visit(node, parent=None):
            if node in rec_stack:
                deadlocks.append(parent)
                return True
            if node in visited:
                return False
            visited.add(node)
            rec_stack.add(node)
            for neighbour in graph.get(node, []):
                if visit(neighbour[0], neighbour):
                    return True
            rec_stack.remove(node)
            return False

        for node in graph:
            if visit(node):
                return deadlocks
        return []


def check_file(filename):
    with open(filename, 'r') as file:
        tree = ast.parse(file.read(), filename=filename)

    checker = DeadlockChecker(tree, filename)
    for error in checker.run():
        print(f"{filename}:{error[0]}:{error[1]}: {error[2]}")


def check_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                check_file(filepath)
