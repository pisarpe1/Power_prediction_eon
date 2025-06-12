Zadání
V souboru data.csv najdete podklady k vypracování úkolu. Jedná se o spotřebu v síti v ČR.

Úkoly:
1.	Časovou řadu (ČŘ) graficky znázorněte
    a.	Vidíte v ČŘ něco zajímavého? 
    b.	Jsou v ČŘ nějaké opakující se vzory, časová závislost atd. 
2.	Zkuste predikovat hodinové hodnoty z posledního týdne. 
    a.	Můžete použít více metod a porovnat je mezi sebou. 
    b.	Můžete použít externí zdroj dat (teploty, osvit, atd), kreativitě se meze nekladou 😊

Řešení nám zašlete vždy kompletní. Vždy popište, jak jste postupovali a na co jste přišli. Pokud pro zpracování použijete nějaký program, poskytněte i funkční zdrojový kód. 


I. Vytvoření pracovního prostředí pro výpočty.

    python -m venv .venv    
    .venv\Scripts\activate
    pip install -r requirements.txt

II. Reserch a stanovení vlivů ovlivňující spotřebu energie. Do výpočtů zahrnu pouze některé faktory ovlivňující cenu.

    Faktor	                Vliv na spotřebu	    Zdroj dat

    Teplota	                Silný	                CHMI, OpenWeatherMap, Meteostat
    Sluneční svit	        Střední/slabý	        CHMI, Meteostat
    Den v týdnu	            Výrazný	                data.csv
    Státní svátek / víkend	Výrazný	                OfficeHolidays.com, kalendář
    Ekonomická aktivita	    Dlouhodobý	            ČSÚ, Eurostat
    Cena elektřiny	        Dlouhodobý/slabší	    ERÚ, PXE

III. Schromáždění dat
    Schromážení dostupných relevantních dat + návrh lokálního uložení. Možno vymyslet i sofistikované komplexní databazové uložení. Pro konzistenci zachovám data v .csv místo SQL.
    a) Interní data o spotřebě: "data/raw"
    b) Raw data uložena v nezměnené podobě v "data/external"
    

IV. Zpracování dat
    Inspekce raw interních i externích dat. Následný rozbor, filtrace, kontrola, korekce.
    (kontrola klíčů, datových typů, chybějících hodnot, atd.) Předpřipravení dat př. externí 
    data obsahují teploty z několika pozic v čr -> stanovení průměrné teploty v ČR.

    Cílem kroku je mít konzistentní data pro budoucí datamining. Data připravena k analýze
    uložena do: "data/processed"


V. Analýza
    Ve složce outputs jsou vygenerovány jednoduché grafy zkterých jsou patrné cykly a externí vlivy v tomto případě teplota.
    1) 
        v čr je patrný opakující se patern na roční úrovni kdy velkám faktorem je například oční období (teplota).
        Dále je zde patrný opakující se patern pracovního týdne tedy rozdíl mezi pracovními dny a víkendy.
        V neposledí řadě je zde opakující se pattern každého dne kdy je patrné kolísání spotřeby v průběhu dne.
        Pro demostraci je zobrazen letní a zimní den.

        Je zde možné provést mnoho dalších inspekcí a praktik jako hledání minim, maxim, průměrů. Dále pak krátkodobých a dlouhodobých trendů a aproximací. 
     

VI. Predikce hodnot