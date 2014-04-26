Specyfikacja techniczna
=======================

Author: Jacek Bzdak

Pojęcia (encje) w systemie
--------------------------

Role w systemie
***************

**Użytkownik**

    Osoba która założyła sobie konto w aplikacji. Może ona
    rejestrować się na wydarzenia oraz tworzyć nowe wydarzenia
    (które podlegają akceptacji administratora)

**Organizator**

    Oosba która tworzy dane wydarzenie. Jest ona zwykłym **użytkownikiem**,
    ale pojawia się ona dostateczne często by dostać własny rzeczownik ;)

**Administrator**

    Osoba administrująca aplikacją. Może akceptować wydarzenia.

**Osoba wdrażająca**

    Osoba która wdraża daną aplikację. Może ona robić proste zmiany i
    zna Pythona.

.. _spec-v10-organizer:

Organizator
***********

By stworzyć jakieś wydarzenie należy podać jego organizatora, przy czym:
organizator nijak nie ma się do osób kont użytkowników.

Dane jakie zbieramy o organizatorze są modyfikowalne przez osobę wdrażającą 
oprogramowanie. Zawsze organizator będzie zawierał takie dane:

* Nazwa instytucji
* Adres instytucji
  * Rozbite na atomowe pola :)
* Numer telefonu

.. note::

    Może warto byłoby zrobić jakieś powiązanie organizaora i konta użytkownika,
    ale na razie tego nie robimy.

.. _spec-v10-event:

Wydarzenie
**********

Wydarzenie jest zbiorem podwydarzeń, rejestrujemy się na podwydarzenia.

.. note::

    W języku Harcerskim wydarzeniem będzie na przykład: Zlot Kadry 2012,
    mial on podwydarzenia: LAS, Zlot harcmistrzów, Zlot Akademików itp.

Podstawowe dane wydarzenia:

* Nazwę wydarzenia
* Opis Wydarzenia
* Numer edycji wydarzenia (na przykład nazwą będzie Zlot Kadry a edycją 2016).
  Pole edycja jest nieobowiązkowe.
* Dane organizatora.
* Datę rozpoczęcia i zakończenia wydarzenia
  * Zawsze podajemy datę rozpoczęcia
  * Data zakończenia jest opcjonalna, jeśli organizator zaznaczy że wydarzenie
    jest jednodniowe.

.. _spec-v10-subevent:

Podwydarzenie
*************

Podwydarzenia są czymś na co uczestnicy się rejestrują. Podwydarzenie ma takie pola:

**Podstawowe dane**

* Nazwa podwydarzenia **obowiązkowe**
* Opis **obowiązkowe**
* Limit miejsc/brak limitu **obowiązkowe**

**Dodatkowe dane**

* Płatność/informacja o darmowości **obowiązkowe**, patrz: :ref:`spec-v10-payment`.
* Czas rezerwacji miejsca **obowiązkowe jeśli jest limit miejsc i płatność**.
  * Osoba która będzie się rejestrować na to podwydarzenie będzie miała tyle
    dni na dokonanie zapłaty. W przypadku gdy wpłata nie dotrze miejsce będzie
    zwalniane.
* Połączenie z rejestracją na wydarzenie
* Ograniczenia na uczestnika (walidacje), parz :ref:`spec-v10-validacje`.

  .. warning::

        Oprogramowanie tego może być skomplikowane w przypadku:

        * Manualnej rejestracji wpłat.
        * Automatycznego rejestrowania przekazów pocztowych

**Podpinanie dynamicznej ankiety**

Każde podwydarzenie ma możliwość podopięcia dynamicznej ankiety zbierającej
dodatkowe (wpisane przez Organizatora) dane o uczestnikach.

Informacje o tej funkcjonalności w :ref:`spec-v10-dynamic-forms`.

.. note::

    Limit miejsc prawdopowobnie wypadnie z pierwszej wersji aplikacji.


Dodatkowa konfiguracja wydarzenia
*********************************

* Data rozpoczęcia rejestracji.
* Data zakończenia rejestracji.

  * Z opcjonalnym grace-period na wpłaty metodami nienatychmiastowymi.


.. note::

    Opcjonalnie: czy nie rozważyć by te dane były określane per podwydarzenie.



Procesy powiązane z wydarzeniem
********************************

.. _spec-v10-akceptacja:

Tworzenie wydarzenia
####################

**tworzone**


    Kiedy wydarzenie jest **tworzone** nie wyświetla się na liście wydarzeń.
    Jest ono wtedy edytowalne dla osoby je tworzącej.

**Do akceptacji**

    Kiedy osoba tworząca wydarzenie kliknęła odpowiedni guzik, wydarzenie uzyskuje
    status do akceptacji.

    Wydarzenie przestaje być wtedy edytowalne
    (patrz: :ref:`spec-v10-edit-event-state`).

    W zależności od konfiguracji wydarzenie albo automatycznie przechodzi w status
    zaakceptowane, albo wymaga to kliknięcia przez administratora
    (patrz: :ref:`spec-v10-event-accept`).

**Zaakceptowane**

    Wydarzenie nie jest edytowalne ale jest widoczne na liście wydarzeń.

Rejestracja otwarta/zamknięta
=============================


**Rejestracja otwarta**

    W tym stanie możliwe jest rejestrowanie się.

    Stan zmienia się na **rejestracja zamknięta** w momencie w którym
    nadejścia chwili zakończenia rejestracji. Jeśli administrator wydarzenia
    nie wpisał tej wartości to stan przechodzi w **wydarzenie trwa/rejestracja trwa**
    w momencie rozpoczęcia wydarzenia.

    .. note::

        Możliwa jest również zamknięcie rejestracji pod wpływem odpowiednich
        validacji (przekroczenie limitu osób).



**Rejestracja zamknięta**

    Nie ma możliwości rejestracji, stan przechodzi w **wydarzenie trwa/rejestracja zamknięta**
    w chwili rozpoczęcia wydarzenia.


Wydarzenie trwa
===============

.. note::

    To nie jest priorytet

**Wydarzenie trwa**

    Stan ten ma dwa podstany:

    * rejestracja trwa
    * rejestracja zamknięta.

**Wydarzenie zakończone**

    Stan po zakończeniu wydarzenia.

.. _spec-v10-edit-event-state:

Edytowalność wydarzenia a jego stan
***********************************

Na razie zamykamy wprowadzanie jakichkolwiek zmian do wydarzenia podczas jego
trwania. Potem będzie trzeba włączyć częściową funkcjonalność zmiany
wydarzenia.

.. note::

    Decyzja po rozmowie z Michałem w REJCEN-29

.. _spec-v10-payment:

Płantość
********

.. note::

    Generalnie całkiem ważne może być wprowadzenie dynamicznej
    metody obliczania ceny. Tutaj nie mam pomysłu jak to uelastycznić 
    w sposób sensowny.

    Przykłady zastosowania:

    * Rejestracja przed daną datą: mniejsza kwota
    * Rejestracja dużej drużyny mniejsza kwota

Płatność zawiera dwie niezależne informacje:

* Kwotę opłaty.
* Metodę opłaty.
* Informacje powiązane z metodą opłaty.


.. _spec-v10-payment-mwthod:

Metoda opłaty
^^^^^^^^^^^^^

Mamy takie metody opłaty:

**Płatność darmowa**

  Specjalny rodzaj platności oznaczający coś bezpłatnego.

**Weryfikacja ręczna przez organizatora**

  Aplikacja w żaden sposób nie obsługuje płatności.

  Organizator wypełnia pole tekstowe, które wyświetla się użytkownikowi
  gdy ma opłacić urzestnictwo.

  Następnie za pomocą interfejsu administracyjnego zaznacza kto zapłacił.

**Płatność przelewem**

  Nie różni się niczym od weryfikacji ręcznej... poza tym że zamiast pola
  tekstowego pojawia się pole na numer konta, która posiada walidację
  czy dany numer konta jest poprawny.

**Płatności Dot Pay**

  Aplikacja obsługuję opłatę przez DotPay.

  Organizator podaje numer konta Dot Pay na które będą przesyłane pieniądze,
  oraz inne dane konieczne do zrealisoania płatności.

  Aplikacja samodzielnie rejestruję wpłtę.


.. _spec-v10-rejetracja:

Rejestracja na zajęcia
**********************

.. note::

    Wypada z pierwszej wersji.

.. _spec-v10-validacje:

Walidacje dostępu do wydarzenia
*******************************

.. note::

    Wydaje mi się że walidację należałoby rozbić na dwa etapy: przed płatnością 
    i po platności. Na przykład walidacją przed płatnością byłoby sprawdzenie
    że użytkownik ma stopień harcmistrza (na przykład na Zlocie Harcmistrzów...)
    a walidacja po platności to sprawdzenie wykonania zadania przedrajdowego.

    Na razie implementujemy walidację przed płatnością.

.. note::

    TODO przemyśleć mechanizm uelastyczniania walidacji.


Lista walidacji jakie będą potrzebne w wersji harcwrsjiej:

* Sprawdzenie stopnia instruktorskiego
* Sprawdzenie wieku


.. _spec-v10-dynamic-forms:

Dynamiczne dane do formularza rejestracji
*****************************************

Generalnie każde wydarzenie będzie zbierało *jakieś* dodatakowe dane o
każdym zgłoszeniu. Chcemy by organizator mógł do każdej atrakcji
podpiąć dodatkowy formularz rejestracji z dynamiczną zawartością.

.. _spec-v10-register-basic-data:

Podstawowe dane związane z rejestracją
**************************************

Podczas rejestracji użytkownik dla każdego wydarzenia podaje ten sam zestaw
podstawowych danych.

Dla wersji ogólnej będzie to:

TODO

Dla wersji harcerskiej:

* Imie
* Nazwisko
* Numer PESEL
* Numer karty członkowskiej (organizator wybiera czy pole to jest obowiązakowe(
* Adres

  * Podzielony na atomowe dane

* Stopień harcerski
* Stopień instruktorski

.. note::

    Całość można zamiemienić na system z wykorzystaniem dynamicznych ankiet.
    Reszta informacji o decyzji na ``REJCEN-26``.

Generyczny mechanizm pluginów
-----------------------------

Sporo rzeczy w tej aplikacji będzie zmienialne na poziomie wdrożenia, dobrze 
byłoby mieć jakiś wspólny mechanizm pluginów który pozwalałby elegancko 
podmieniać poszczególne używane modele w Django. 

Na pewno za pomocą pluginów opisywane będą: 

* Podstawowe informacje podawane podczas rejestracji (przez użytkownika)
* Podstawowe informacje o wydarzeniu

 * Podstawowe informacje o podwydarzeniu

* Podstawowe informacje o organizatorze


Integracja z ESHD
-----------------

Rejestracja jednoosobowa
************************

Tutaj integracja jest prosta, za pomocą: numeru PESEL, numery karty, imienia
i nazwiska sprawdzamy czy ktoś jest w ESHD. Jeśli go nie ma to odrzucamy 
osoba nie może się zarejestrować. 

Rejestracja wieloosobowa
************************

.. note::

    Wypada.


Raporty
-------

TODO

Scenariusze użycia
------------------

Logowanie i zakładanie konta
****************************

Logowanie
^^^^^^^^^

.. note::

    Zasadniczo logowanie zostaje poza zakresem głównej aplikacji, powinna być 
    możliwość doklejenia dowolnego mechanizmu logowania.

System pozwala na logowanie za pomocą dwóch metod:

**Loginem i hasłem**


    By zalogować się należy podać swój login i hasło.

    Logowanie i zakładanie konta robimy za pomocą ``django-registration``.

    .. note::

        W przyszłości zrobimy logowanie emailem.


**Za pomocą konta ``zhp.net.pl`` (mechanizm openid)**

    By zalogować się należy kliknąć w odpowiedni guzik, który wykona procedurę 
    logowania open-id.

Utworzenie wydarzenia
*********************

Każdy ma prawo stworzyć nowe wydarzenie. Użytkownik klika guzik: dodaj wydarzenie
i przenosi go na formularz dodawania wydarzenia.

.. note::

    Ewentualnie można rozważyć wymaganie posiadania odpowiedniego przywileju
    django.

Formularze ten zawiera podstawowe dane wydarzenia oraz dane organizatora 
(opis tutaj: :ref:`spec-v10-event`, oraz :ref:`spec-v10-organizer`).

Użytkownik wypełnia ten formularz i jeśli nie ma błędów wydarzenie dodaje
się w stanie: 'Nowe'.

Dodanie podwydarzenia
*********************

Użytkownik dodał już wydarzenie i teraz dodaje podwydarzenie. Znajduje swoje
wydarzenie i klika: dodaj podwydarzenie.

Wypełnia podstawowe dane podwydarzenia (patrz: :ref:`spec-v10-subevent`).

Jeśli dane są poprawne do wydarzenia dodaje się podwydarzenie.

.. note::

    Na liśice wydarzeń organizator wydarzenia widzi jego status.

Dodanie płatności do podwydarzenia
**********************************

Podwydarzenie domyślnie jest bezpłatne, po jego dodanoiu na liście podwydarzeń
w wydarzeniu pojawia się guzik "Dodaj płatność", po jego kliknięciu użytkownik
widzi formularz zawierający: 

* Typ płatności (patrz: :ref:`spec-v10-payment-mwthod`).  
* Kwotę płatności (nie pojawia się dla darmowej płatności).
* Dodatkowe informacje określane przez typ płatności.

Dodanie (dynamicznej) ankiety do podwydarzenia
**********************************************

Domyślnie podwydarzenie nie ma dynamicznej ankiety.

Po dodaniu podwydarzenia na liście podwydarzeń
w wydarzeniu pojawia się guzik "Dodaj ankietę".

Po jego kliknięciu organizator widzi listę już dodanych
pytań z możliwością ich edycji oraz formularz 
umożliwiający dodanie pytania.

TODO opisać dokladniej.

Wysłanie wydarzenia do weryfikacji
**********************************

Po dodaniu wszystkich podwydarzeń organizator klika na guzik:
rozpocznij zbieranie zgłoszeń.

Jeśli w konfigiuracji systemu *nie wymagamy* weryfikacji wydarzeń
wydarzenie otrzymuje status: **zaakceptowane**. Jeśli data rozpoczęcia
zbierania zgłoszeń już minęła status zmienia się na **otwarte**.

Jeśli wymagamy weryfkiacji to status zmienai się na: **Do akceptacji**, oraz:

* Administrator aplikacji otrzyma wiadomość e-mail o konieczności weryfikacji
  danego wydarzenia.
* Organizator dostanie e-maila o konieczności weryfikacji.

.. _spec-v10-event-accept:

Weryfikacja wydarzena
*********************

Administrator w panelu administracyjnym ma listę wydarzeń do potwierdzenia.

Dla każdego z nich może zaakceptować je lub odrzucić.

* Zaakceptowane otrzymuje status **zaakceptowane**
* Odrzucone otzymuje status **nowe** (można ją zmienić i przesłać do akceptacji ponownie).

W obu przypadkach organizator otrzymuje wiadomość e-mail.

W przypadku odrzucenia rejestracji administrator musi podać powód, który
pojawi się w mailu do organizatora.

Automatyczna zmiana stanów wydarzeń
***********************************

Dodajemy komendę administracyjną django (django management command), która
przy wywołaniu odświerza stan rejestacji.

Rejestracja
***********

Użytkownik na liście wydarzeń