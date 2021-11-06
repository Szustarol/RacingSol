### Rozwiązania zadań rekrutacyjnych AGH Racing

# Zadanie 1
W zasadzie niewiele do komentowania - dość trywialna implementacja maszyny stanów.
Użyta biblioteka curses żeby "wyłapać" wciśnięcie klawisza, to trochę naiwne podejście,
ale dla takiego zastosowania wystarczy.
Uruchamiamy skrypt *lights.py*.

# Zadanie 2
Zaimplementowana metoda Newtona z autorskim wyborem punktu początkowego, wystarczy uruchomić
skrypt *sqrt.py*, poczekać chwilę aż policzą się wykresy, w efekcie ukażą się wyniki obliczeń.

# Zadanie 3
Game of Life zaimplementowane z biblioteką PyGame do wizualizacji, uruchamiamy skrypt 
*gameOfLife.py*, ustawienia poczatkowe można podać jako plik .json, np.
*gameOfLife.py glider.json*, załączam również trzy przykładowe ustawienia w formacie .json.
Jeśli skyrpt będzie uruchomiony bez pliku, to wygeneruje losowe ustawienie.
Aby wyjść wciskamy ESC.
Za logikę odpowiada klasa GameState, za konfigurację i wczytywanie JSON - GameConfig, 
wyświetlanie View, a całą resztą zajmuje się *gameOfLife.py*.