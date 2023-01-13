# **PerformanceApp** - Aplikacja wspomagająca progres w wysiłku fizycznego


    Aplikacja z interfejsem służy do pomiaru i nadzorowania aktualnego statusu zdrowotnego użytkownika. Do klasyfikacji nowych użytkowników użyty został model uczenia maszynowego, którego algorytm został przyuczony na ogólnodostępnym zbiorze 10 tysięcy badanych osób o różnej płci i wieku.
    Głównym założeniem aplikacji było wsparcie progresu użytkowników w wysiłku fizycznym poprzez możliwość porównania swoich osiągnięć z innymi.
    
    Autorzy: Paweł Kawecki i Marcel Gęsicki

## **Licencja**
<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Licencja Creative Commons" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br />Ten utwór jest dostępny na <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">licencji Creative Commons Uznanie autorstwa-Użycie niekomercyjne-Na tych samych warunkach 4.0 Międzynarodowe</a>.

# **Diagram architektury procesu**

![app diagram](https://github.com/pkaweck/Flask_app/blob/master/images/App_Diagram.png?raw=true "Diagram technologiczny aplikacji")

    1. Użytkonik wchodzi w interakcję z interfejsem
    2. Wyniki wysyłane są do aplikacje w Azure App Services, gdzie wykonywana jest predykcja
    3a. Wyniki predykcji inicjują pobranie danych z bazy w celu stworzenia wizualizacji
    3b. Użytkownik zostaje przekierowany na stronę dashboardu
    4. Dane wprowadzone przez użytkownika zostają spakowane do JSONa wysłane poprzez HTTP request POST do pipeline'u Azure Logic Apps
    5. Dane zostają rozpakowane z obiektu JSON i wprowadzone do odpowiedniej tabeli w bazie danych
    6. Zależnie od potrzeby manualnie jest wykonywane przyuczenie modelu machine learningowego na nowych danych


# **Specyfikacja wymagań**


1.  Formularz [Priorytet 1 - Frontend] - służący do interakcji z użytkownikiem wchodzącym na stronę. Formularz wypełniany jest danymi użytkownika odnoszących się do osiągnięć fizycznych. 
2.  Model uczenia maszynowego [Priorytet 1 - Backend] - służy predykcji przypisania wyników użytkownika do danej klasy fizycznej.
3.  Baza danych [Priorytet 1 - Backend] - Azure SQL DB do przechowywania wyników wprowadzonych przez użytkowników.
4.  Dashboard [Priorytet 1 - Frontend] - wizualne przedstawienie danych użytkownika w porównaniu do pozostałej puli wyników.
5.  Modyfikacje dashboardu [Priorytet 3 - Frontend] - możliwość wyboru przedstawionych w dashboardzie wykresów i aktywacja dodatkowych opcji wyświetlania 
6.  Zrzut danych [Priorytet 3 - Frontend] - możliwość wykonania zrzutu danych do postaci surowej tabeli lub pdfa.


# **Architektura technologiczna**


**Architektura rozwoju:**

- Azure,
- Python,
- Visual Studio Code,
- github


**Architektura uruchomieniowa**

- Azure SQL DB,
- Azure Logic Apps,
- Azure App Services,
- biblioteki Python wykorzystywane w aplikacji wraz z wersją uwzględnione są w pliku requirements.txt
- biblioteka scikit-learn używana w przyuczaniu modeli uczenia maszynowego

# **Scenariusze testów**

### **1. Stworzenie algorytmu uczenia maszynowego do predykcji klasy użytkownika**
```python
#Zbiór uczony i trenowany
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2)
#Skalowanie zmiennych
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)


Drzewo decyzyjne

#Klasyfikacja
clf = DecisionTreeClassifier()
clf = clf.fit(X_train, y_train)

#Predykcja
predictions = clf.predict(X_test)
predictions

Accurancy: 51,84%


KNN

#KNN Klasyfikacja
from sklearn.neighbors import KNeighborsClassifier
classifier = KNeighborsClassifier(n_neighbors=3)
classifier.fit(X_train, y_train)

#Predykcja
y_pred = classifier.predict(X_test)

Accurancy: 48%



Random Forest 

#Tworzenie klsyfikacji
clf=RandomForestClassifier(n_estimators=100)

#Dopasowanie modelu
clf.fit(X_train,y_train)

#Predykcja nowych wartości
y_pred=clf.predict(X_test)

#Import biblioteki do obliczania wyników accurancy
from sklearn import metrics
# Model Accuracy, how often is the classifier correct?
print("Accuracy:",round(metrics.accuracy_score(y_test, y_pred), 2))

Accurancy: 73%

```
Model został przyuczony lokalnie na podstawie wcześniej pozyskanych danych (<a url=https://www.kaggle.com/datasets/kukuroo3/body-performance-data>Kaggle Dataset</a>) udostępnionych na podstawie licencji otwartej <a rel="license" url=https://creativecommons.org/publicdomain/zero/1.0>CC0 1.0 Universal (CC0 1.0) Public Domain Dedication </a>. Na podstawie wyników accurancy score wybrany został model oparty o lasy losowe.
Wykonane zostały trzy modele uczenia maszynpowego w celu wybrania tego z najwyższą wartością ACC. W każdym modelu do podzielenie zbioru danych na trenowany i testowany użyty został train_test_split biblioteki sklearn.model_selection. Dane zostały również zeskalowane poprzez użycie StandardSkaler. W drzewie decyzyjnym model został przyuczony i wykonana została predykcja wartości na podstawie wartości testowanych. Podobny proces został zastosowany w modelu KNN, gdzie użytko modelu z sklearn KNeighborsClassifier. W przypadku lasów losowych klasyfikacja została dokonana funkcją RandomForestClassifier z sklearn przy ustawieniu 100 drzew w lesie. Następnie wykonana została predykcja na zbiorze testowym oraz sprawdzenie jej poprawności. 
Wyniki wykazały, iż nawiększą istotność miał model lasów losowych, dlatego też został on użyty w aplikacji.

**Próbka danych wykorzystanych do przyuczenia modelu**

| age | gender | bmi         | body_fat_perc | diastolic | systolic | grip_force | sit_ups | broad_jump_cm | class | 
|-----|--------|-------------|---------------|-----------|----------|------------|---------|---------------|-------| 
| 25  | 0      | 20.49586777 | 15.7          | 77        | 126      | 36.4       | 53      | 229           | A     | 
| 42  | 1      | 23.54006338 | 32.2          | 72        | 135      | 22.7       | 18      | 146           | C     | 
| 42  | 0      | 22.84425666 | 19.3          | 63        | 110      | 43.5       | 68      | 211           | A     | 
| 57  | 1      | 20.93212012 | 20.9          | 69        | 106      | 21.5       | 0       | 90            | C     | 
| 45  | 1      | 24.95945572 | 30.9          | 93        | 144      | 34.1       | 30      | 155           | A     | 
| 26  | 0      | 22.09244157 | 9.7           | 64        | 135      | 59.6       | 61      | 239           | A     | 
| 59  | 1      | 25.79736274 | 30.2          | 76        | 143      | 36.8       | 25      | 122           | A     | 



age	- wiek użytkownika 

gender - (0- Male, 1- Female) Płeć badanej użytkownika

body_fat_perc - Procentowa ilość tkanki tłuszczowej w ciele

diastolic - Ciśnienie krwi rozkurczowe

systolic - Ciśnienie krwi skurczowe

grip_force - Siła uchwytu

sit-ups - Liczba skłonów tułowia

broad_jump_cm - Skok w dal z miejsca

bmi - Wskaźnik BMI 	Wyliczony na podstawie zmiennych dotyczących wzrostu (height) i wagi (weight) zawartych w oryginalnym zbiorze danych

class (A-najlepsza, B-przeciętna, C-najgorsza) - Klasa oceny sprawności fizycznej


-------------------------------------------
### **2. Uruchomienie lokalne**

1. Wykorzystując plik pythona, lokalnie otworzyć formularz i jednocześnie stronę główną w rozszerzeniu HTML- plik *FLASK.html* poprzez adres lokalny strony 127.0.0.1:5000.
```python
@app.route('/', methods = ['POST', 'GET'])
    def index():
        return render_template('FLASK.html')
```
Dekator app wykorzystywany jest do określenia ścieżki na stronie i tego co jest wynikiem takiej akcji/funkcji. Jest to podstawowa klasa obiektów we Flask dla których określa się metody i funkcje, które powoduje wywołanie strony.

![ankieta](https://github.com/pkaweck/Flask_app/blob/master/images/ankieta_screen.png?raw=true "Ankieta")


2. Wprowadzenie danych użytkownika i zatwierdzenie danych formularza wraz z przejściem przy pomocy przycisku "SUBMIT"

```HTML
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
   <title>Performance Dashboard</title>
</head>


<body style="font-family:arial, sans-serif; background:#adc1fd">
    <h1 style="background:#EDF0F5;padding:1px; font-size: 340%">
       <p>Performance survey</p>
    </h1>
<style> label,input, select, option {font-size:150%; font-family: arial}</style>

<form action="/results", method="POST">
    <label for="age">Age:</label>
    <input type="number" min = "18" max = "100" id = "age" name="age" value="" required>
    ...
    <p> <label for="broad_jump_cm">Broad jump in centimeters</label>
        <input type="number" name="broad_jump_cm" min = "0" max = 400 id ="broad_jump_cm" min = "0" max="" value="" required></p>
        <input type="submit" value="Submit" style = "font-size:140%">
</form> 
</body>
</html>
```

Wyświetlana zawartość strony określona jest w języku HTML opartym na tagach. Tagi wyznaczają początek i koniec obiektów lub wspólnie określonych parametrów obiektów. Powyższy kod zawiera nagłówek strony, tag zawierający parametry dla wyszczególnionych obiektów oraz obiekt formularza, którego zatwierdzenie przyciskiem wywołuje przejście na inną stronę.

3. Odpytywanie bazy danych Azure SQL - pozyskiwanie danych do wykresów na dashboardzie użytkownika.
```python
sql_query = pd.read_sql_query ('''
        SELECT class, lower_limit as bmi ,count(per.id) as 'count'
        from [dbo].[tbl_performance] as per
        join [dbo].[tbl_range] as rng
        on per.bmi > rng.lower_limit and per.bmi <= rng.upper_limit
        group by class, lower_limit
        order by class asc, lower_limit asc
        '''
        ,cnxn)
```

![dashboard](https://github.com/pkaweck/Flask_app/blob/master/images/Dashboard.png?raw=true "Dashboard")

Na potrzeby wizualizacji, odpytywana jest baza danych przy pomocy języka SQL.

4. Wprowadzanie nowych danych do bazy Azure SQL przy pomocy pipeline'a w Azure Logic Apps

![logic pipeline](https://github.com/pkaweck/Flask_app/blob/master/images/logic-apps-process.PNG?raw=true "Logic Apps pipeline")


Przykładowy request HTTP metodą POST wysyłany na adres pipeline'a Logic Apps:
```json
{
        "age": 30,
        "gender":1,
        "bmi": 20.5,
        "body_fat":25.5,
        "diastolic": 70,
        "systolic": 120,
        "grip_force": 35.4,
        "sit_ups":25,
        "broad_jump_cm": 250,
        "class": "T2"
}
```
![logic pipeline test](https://github.com/pkaweck/Flask_app/blob/master/images/logic-apps-process-testing.PNG?raw=true "Logic Apps testing")

Wyniki odpytania bazy testowej przedstawiają poprawnie załadowane dane z requesta w drugim rzędzie tabeli:

![sql results](https://github.com/pkaweck/Flask_app/blob/master/images/sql_results.PNG?raw=true "Wyniki SQL")


----------------------------------------
### **Uruchomienie webowe**

1. Wdrożenie aplikacji na środowisko wirtualne Azure App Services i wejście na stronę przy użyciu wygenerowanej domeny:
https://se-performance-app-v2.azurewebsites.net/

2. Wprowadzenie danych testowych (a) i zatwierdzenie formularza w celu sprawdzenia przekierowania i działania dashboardu (b):

 ## **a)** 

![live app form](https://github.com/pkaweck/Flask_app/blob/master/images/live_app_form.PNG?raw=true "Aplikacja webowa ankieta")

 ## **b)**
![live app dashboard](https://github.com/pkaweck/Flask_app/blob/master/images/live_app_dashboard.PNG?raw=true "Aplikacja webowa dashboard")

