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

II. Stanovení vlivů ovlivňující spotřebu energie.

    Faktor	                Vliv na spotřebu	    Zdroj dat

    Teplota	                Silný	                CHMI, OpenWeatherMap, Meteostat
    Sluneční svit	        Střední/slabý	        CHMI, Meteostat
    Den v týdnu	            Výrazný	                data.csv
    Státní svátek / víkend	Výrazný	                OfficeHolidays.com, kalendář
    Ekonomická aktivita	    Dlouhodobý	            ČSÚ, Eurostat
    Cena elektřiny	        Dlouhodobý/slabší	    ERÚ, PXE

III. Schromáždění dat
    Schromážení dostupných relevantních dat. Následný rozbor, filtrace, kontrola, korekce.
