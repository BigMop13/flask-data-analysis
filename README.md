# Analiza Danych Służby Zdrowia

## Opis Projektu
Ten projekt to aplikacja webowa napisana w Pythonie z wykorzystaniem frameworka Flask, która umożliwia analizę i wizualizację danych dotyczących służby zdrowia w Polsce. Aplikacja prezentuje interaktywne wykresy i statystyki dotyczące:

- Liczby lekarzy i pielęgniarek w Polsce w latach 2017-2023
- Wskaźników zdrowotnych w różnych województwach
- Rozkładu liczby lekarzy według województw

## Funkcjonalności
- Interaktywne wykresy stworzone przy użyciu biblioteki Plotly
- Analiza trendów w służbie zdrowia na przestrzeni lat
- Porównanie danych między województwami
- System uwierzytelniania użytkowników
- Responsywny interfejs użytkownika

## Wymagania
- Python 3.11
- Docker i Docker Compose
- PostgreSQL 15

## Instalacja i Uruchomienie

### 1. Sklonuj repozytorium
```bash
git clone <url-repozytorium>
cd flask-data-analysis
```

### 2. Uruchom aplikację za pomocą Dockera
```bash
docker compose up --build
```

Aplikacja będzie dostępna pod adresem: http://localhost:5001

### 3. Rejestracja i Logowanie
- Zarejestruj nowe konto używając formularza rejestracji
- Zaloguj się używając utworzonego konta
- Po zalogowaniu będziesz miał dostęp do wszystkich wykresów i analiz

## Struktura Projektu
```
flask-data-analysis/
├── app.py              # Główny plik aplikacji
├── auth.py             # Obsługa uwierzytelniania
├── models.py           # Modele bazy danych
├── data_loader.py      # Ładowanie i przetwarzanie danych
├── analysis_utils.py   # Funkcje analityczne
├── templates/          # Szablony HTML
├── static/            # Pliki statyczne (CSS, JS)
├── requirements.txt    # Zależności Pythona
└── docker-compose.yml  # Konfiguracja Dockera
```

## Technologie
- **Backend**: Flask, SQLAlchemy, PostgreSQL
- **Frontend**: HTML, CSS, Bootstrap
- **Wizualizacja**: Plotly
- **Analiza Danych**: Pandas
- **Konteneryzacja**: Docker

## Autor
Jakub Kućmin
Kamil Kurek

## Licencja
Ten projekt jest udostępniany na licencji MIT. 
