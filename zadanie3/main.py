import heapq

# milo ze link do youtuba w tresci zadania nie dziala ale chociaz dali link do implementacji xD

# Class to represent huffman tree
class Node:
	def __init__(self, x):
		self.data = x
		self.left = None
		self.right = None

	def __lt__(self, other):
		return self.data < other.data

# Function to traverse tree in preorder
# manner and push the huffman representation
# of each character.
def preOrder(root, ans, curr):
	if root is None:
		return

	# Leaf node represents a character.
	if root.left is None and root.right is None:
		ans.append(curr)
		return

	preOrder(root.left, ans, curr + '0')
	preOrder(root.right, ans, curr + '1')

def huffmanCodes(s, freq):
	# Code here
	n = len(s)

	# Min heap for node class.
	pq = []
	for i in range(n):
		tmp = Node(freq[i])
		heapq.heappush(pq, tmp)

	# Construct huffman tree.
	while len(pq) >= 2:
		# Left node
		l = heapq.heappop(pq)

		# Right node
		r = heapq.heappop(pq)

		newNode = Node(l.data + r.data)
		newNode.left = l
		newNode.right = r

		heapq.heappush(pq, newNode)

	root = heapq.heappop(pq)
	ans = []
	preOrder(root, ans, "")
	return ans

if __name__ == "__main__":
	s = "abcdef"
	freq = [5, 9, 12, 13, 16, 45]
	ans = huffmanCodes(s, freq)
	for code in ans:
		print(code, end=" ")