""" Development from Nina Nuñez Marco
https://github.com/Nina-99/Algorithm-Huffman"""

from typing import Dict, List


class Node:
    def __init__(self, char: str or None = None, count: int = 0):
        self.char: str or None = char
        self.count: int = count
        self.leaves: List[Node] = []


class Tree:
    def __init__(self, frequency: Dict[str, int] or None = None):
        self.root = None
        if not frequency:
            return

        # NOTE: converts the dictionary to a list ordered by frecuency from lowest to highest
        sorted_list = sorted(frequency.items(), key=lambda x: x[1])

        # NOTE: create one node for each element of the dictionary
        tree_list: List[Node] = []

        for item in sorted_list:
            tree_list.append(Node(item[0], item[1]))

        if len(tree_list) == 1:  # NOTE: if there is only one character
            self.root = tree_list.pop(0)

        while tree_list:  # NOTE: while there are nodes to be added to the tree
            item1 = tree_list.pop(0)
            item2 = tree_list.pop(0)

            combined = Node(count=item1.count + item2.count)
            combined.leaves = [item1, item2]
            if not tree_list:
                self.root = combined
            else:
                tree_list.append(combined)
                tree_list.sort(key=lambda x: x.count)

    def __str__(self) -> str:  # NOTE: return a text representation of a tree
        string = ""
        i = 0
        for item in self.order_bfs():
            num_leaves = len(item.leaves)
            if num_leaves > 0:
                if i == 0:
                    string += (
                        f"\n\tRoot {item.char} ({item.count}) leaves {num_leaves}\n"
                    )
                    i += 1
                elif i == 1:
                    string += f"\n\tLeft_Nodo {item.char} ({item.count}) leaves {num_leaves}\n"
                    i = 2
                else:
                    string += f"\n\tRight_Nodo {item.char} ({item.count}) leaves {num_leaves}\n"
                    i = 1
                j = 0

                for leaf in item.leaves:
                    if j == 0:
                        string += f"left: {leaf.char} ({leaf.count})"
                        j += 1
                    else:
                        string += f"\t\tright: {leaf.char} ({leaf.count})"
        return string

    def order_bfs(self) -> List[Node]:  # NOTE: Generate a list sorted by width
        pending: List[Node] = [self.root]
        nodelist: List[Node] = []
        while pending:
            curr = pending.pop(0)
            nodelist.append(curr)

            for leaf in curr.leaves:
                pending.append(leaf)

        return nodelist

    def _assign_code_char(self, code_dict, node, code):
        if node.char:
            # NOTE: if is one node with each character, change the dictionary with the code so far
            code_dict[node.char] = code

        if len(node.leaves) == 2:
            # NOTE: if is one node of conection, she calls hersel with each one of her sheets
            # NOTE: 0 if is left sheet and 1 if is right sheet
            self._assign_code_char(code_dict, node.leaves[0], code + "0")
            self._assign_code_char(code_dict, node.leaves[1], code + "1")

    def code_to_dict(self) -> Dict[str, str]:
        # NOTE: Convert tree to dictionary of code based on its position

        # NOTE: if there is only one node in the tree represent with a zero
        if not self.root.leaves:
            return {self.root.char: "0"}

        code_dict = {}

        # NOTE: recursively assign codes to each char
        self._assign_code_char(code_dict, self.root, "")

        return code_dict
