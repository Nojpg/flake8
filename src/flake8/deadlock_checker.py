import ast


class DeadlockChecker:
    def __init__(self, tree, filename):
        self.tree = tree
        self.filename = filename
        self.lock_graph = {}
        self.threads = self.identify_threads()
        self.build_lock_graph()

    def run(self):
        if self.detect_deadlock():
            yield (0, 0, "DLC001 potential deadlock detected", type(self))

    def identify_threads(self):
        threads = {}
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Call) and isinstance(node.func,
                                                         ast.Attribute) and node.func.attr == 'Thread':
                for kw in node.keywords:
                    if kw.arg == 'target':
                        thread_func = kw.value.id
                        threads[thread_func] = []
        return threads

    def build_lock_graph(self):
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                func_name = node.name
                if func_name in self.threads:
                    current_locks = []
                    for n in ast.walk(node):
                        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute):
                            lock_name = self.get_lock_name(n.func.value)
                            if n.func.attr == 'acquire':
                                current_locks.append(lock_name)
                                if len(current_locks) > 1:
                                    self.add_to_graph(current_locks[-2], current_locks[-1])
                            elif n.func.attr == 'release' and lock_name in current_locks:
                                current_locks.remove(lock_name)

    def get_lock_name(self, node):
        if isinstance(node, ast.Name):
            return node.id
        return None

    def add_to_graph(self, lock1, lock2):
        if lock1 not in self.lock_graph:
            self.lock_graph[lock1] = set()
        self.lock_graph[lock1].add(lock2)

    def detect_deadlock(self):
        visited = set()
        rec_stack = set()

        def visit(lock):
            if lock in rec_stack:
                return True
            if lock in visited:
                return False
            visited.add(lock)
            rec_stack.add(lock)
            for neighbour in self.lock_graph.get(lock, []):
                if visit(neighbour):
                    return True
            rec_stack.remove(lock)
            return False

        for lock in self.lock_graph:
            if visit(lock):
                return True
        return False


def check_file(filename):
    with open(filename, 'r') as file:
        tree = ast.parse(file.read(), filename=filename)
    checker = DeadlockChecker(tree, filename)
    for error in checker.run():
        print(f"{filename}:{error[0]}:{error[1]}: {error[2]}")


check_file(r'C:\Users\killa\PycharmProjects\flake8\deadlock-test-suite\testcases\CWE833_Deadlock\dl_on_event.py')
