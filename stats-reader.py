import json
import os

def wczytaj_statystyki(sciezka_pliku):
    if not os.path.exists(sciezka_pliku):
        print(f"Nie znaleziono pliku: {sciezka_pliku}")
        return

    with open(sciezka_pliku, 'r', encoding='utf-8') as f:
        dane = json.load(f)

    mined = dane.get("stats", {}).get("minecraft:mined", {})

    if not mined:
        print("Brak danych o zniszczonych blokach.")
        return
    
    print("Zniszczone bloki:")
    suma = 0  # zmienna na sumę wszystkich bloków
    
    # Poprawiona pętla po elementach słownika mined
    for blok, ilosc in mined.items():
        suma += ilosc  # sumujemy ilości
        nazwa = blok.replace("minecraft:", "")
        print(f"  - {nazwa}: {ilosc}")

    print(f'Łączna ilość zniszczonych bloków: {suma}')

# Ścieżka do pliku statystyk gracza — zmień na odpowiednią
sciezka = "9dd1ff07-e21d-4634-bf2b-5b4396938078.json"
wczytaj_statystyki(sciezka)
