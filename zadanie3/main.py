import heapq
from collections import Counter

''' -------Wstęp teoretyczny dla głupich dziewczynek-------
 znaki:
 -> często występujące znaki dostają krótsze kody binarne
 -> rzadziej występujące znaki dostają dłuższe kody
 -> w wyniku: zakodowany tekst jest krótszy
 
 drzewo binarne:
 -> liście - znaki z tekstu (unikatowe symbole użyte w tekście)
 -> ścieżka od korzenia do liścia - kod binarny dla znaku (0 = lewo, 1 = prawo)
 -> w wyniku: każdy znak ma unikalną ścieżkę, znaki częstsze są bliżej korzenia, znaki rzadsze są głębiej
 
 ścieżka:
 -> mówi jak dojść od korzenia drzewa do konkretnego znaku (liścia):
		-> 0 = przechodzisz w lewo w drzewie
		-> 1 = przechodzisz w prawo w drzewie
 węzły:
 -> każdy znak i jego częstotliwość tworzy osobny węzeł
'''


# klasa reprezentująca węzeł drzewa Huffmana
class Node:
	def __init__(self, x):
		self.data = x	# przechowuje częstotliwość węzła
		self.left = None # odnośnik do lewego dziecka w drzewie
		self.right = None #odnośnik do prawego dziecka w drzewie

	def __lt__(self, other): # przeciążenia "mniejsze niż", żeby heapq wiedział, jak sortować węzły
		return self.data < other.data

# funkcja do przechodzenia drzewa w przód (najpierw korzeń, potem lewo, potem prawo)
# w praktyce: budujemy kod binarny dla każdego znaku
# kode_list - lista, w której zbieramy gotowe kody Huffmana
# current_path - aktualna ścieżka w formie stringa, która pokazuje, jakie kroki (0/1) przeszliśmy od korzenia do aktualnego miejsca
def preOrder(root, code_list, current_path):

	if root is None:
		return

	# jak jesteśmy na liściu, czyli nie ma dzieci, to zapisujemy zakodowaną ścieżkę (curr) -> dodajemy ten kod binarny do listy wynikowej
	if root.left is None and root.right is None:
		code_list.append(current_path)
		return

	# jeśli to nie jest liść, to idziemy dalej
	preOrder(root.left, code_list, current_path + '0')
	preOrder(root.right, code_list, current_path + '1')

# sign_list - lista unikatowych znaków z tekstu
# freq – lista częstotliwości znaków z sign_list
def huffmanCodes(sign_list, freq):

	n = len(sign_list)
	priority_queue = []

	# dodajemy do kolejki węzły z częstotliwościami
	for i in range(n):
		temp = Node(freq[i])
		heapq.heappush(priority_queue, temp)

	# tworzenie drzewa Huffmana
	while len(priority_queue) >= 2:
		# pobranie dwóch węzłów (lewy i prawy) o najmniejszych częstotliwościach
		l = heapq.heappop(priority_queue)
		r = heapq.heappop(priority_queue)
		# tworzenie nowego węzła przez łączenie częstotliwości -> powstaje nowa grupa ze wspólnych rodzicem
		newNode = Node(l.data + r.data)
		newNode.left = l
		newNode.right = r
		# dodanie nowego węzła do kopca
		heapq.heappush(priority_queue, newNode)

# kiedy się skończy while to zostanie tylko jeden węzeł root
	root = heapq.heappop(priority_queue)
	code_list = []
	# przechodzimy przez drzewo
	preOrder(root, code_list, "")
	return code_list

if __name__ == "__main__":
	text = "Kocham różowy :)"
	# zliczanie częstotliwości występowania znaków
	counter = Counter(text)
	# wyciągamy znaki i ich częstotliwości osobno
	sign_list = list(counter.keys())
	freq = list(counter.values())
	print("Znaki:", sign_list)
	print("Częstotliwości:", freq)

	code_list = huffmanCodes(sign_list, freq)
	for code in code_list:
		print(code, end=" ")