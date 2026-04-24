def build_tree(flow):
    stack = []
    tree = {}

    for x in flow:
        if stack and stack[-1] == x:
            stack.pop()
        else:
            if stack:
                parent = stack[-1]
                tree.setdefault(parent, [])

                if x not in tree[parent]:
                    tree[parent].append(x)

            stack.append(x)

    return tree


def print_tree(root, tree):
    def _print(node, prefix="", is_last=True):
        connector = "└─ " if is_last else "├─ "
        print(prefix + connector + str(node))

        children = tree.get(node, [])
        for i, child in enumerate(children):
            last = i == len(children) - 1
            new_prefix = prefix + ("   " if is_last else "│  ")
            _print(child, new_prefix, last)

    print(root)
    children = tree.get(root, [])
    for i, child in enumerate(children):
        _print(child, "", i == len(children) - 1)
