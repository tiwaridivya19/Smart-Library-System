
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        current = self.root

        for character in word.lower():
            if character not in current.children:
                current.children[character] = TrieNode()

            current = current.children[character]

        current.is_end = True

    def search(self, word):
        current = self.root

        for character in word.lower():
            if character not in current.children:
                return False

            current = current.children[character]

        return current.is_end

    def starts_with(self, prefix):
        current = self.root

        for character in prefix.lower():
            if character not in current.children:
                return False

            current = current.children[character]

        return True

    def autocomplete(self, prefix):
        current = self.root

        for character in prefix.lower():
            if character not in current.children:
                return []

            current = current.children[character]

        results = []

        def collect(node, word):
            if node.is_end:
                results.append(word)

            for character in sorted(node.children):
                collect(
                    node.children[character],
                    word + character
                )

        collect(current, prefix.lower())
        return results
