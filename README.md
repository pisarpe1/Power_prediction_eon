# Zadání

V souboru `data.csv` najdete podklady k vypracování úkolu. Jedná se o spotřebu v síti v ČR.

## Úkoly

1. **Časovou řadu (ČŘ) graficky znázorněte**
    - Vidíte v ČŘ něco zajímavého?
    - Jsou v ČŘ nějaké opakující se vzory, časová závislost atd.
2. **Zkuste predikovat hodinové hodnoty z posledního týdne.**
    - Můžete použít více metod a porovnat je mezi sebou.
    - Můžete použít externí zdroj dat (teploty, osvit, atd), kreativitě se meze nekladou 😊

Řešení nám zašlete vždy kompletní. Vždy popište, jak jste postupovali a na co jste přišli. Pokud pro zpracování použijete nějaký program, poskytněte i funkční zdrojový kód.

---

## I. Vytvoření pracovního prostředí pro výpočty

```bash
python -m venv .venv    
.venv\Scripts\activate
pip install -r requirements.txt
```

---

## II. Reserch a stanovení vlivů ovlivňující spotřebu energie

Do výpočtů zahrnu pouze některé faktory ovlivňující cenu.

| Faktor                  | Vliv na spotřebu      | Zdroj dat                           |
|-------------------------|----------------------|-------------------------------------|
| Teplota                 | Silný                | CHMI, OpenWeatherMap, Meteostat     |
| Sluneční svit           | Střední/slabý        | CHMI, Meteostat                     |
| Den v týdnu             | Výrazný              | data.csv                            |
| Státní svátek / víkend  | Výrazný              | OfficeHolidays.com, kalendář        |
| Ekonomická aktivita     | Dlouhodobý           | ČSÚ, Eurostat                       |
| Cena elektřiny          | Dlouhodobý/slabší    | ERÚ, PXE                            |

---

## III. Schromáždění dat

Schromážení dostupných relevantních dat + návrh lokálního uložení. Možno vymyslet i sofistikované komplexní databázové uložení. Pro konzistenci zachovám data v `.csv` místo SQL.

- a) Interní data o spotřebě: `data/raw`
- b) Raw data uložena v nezměněné podobě v `data/external`

---

## IV. Zpracování dat

Inspekce raw interních i externích dat. Následný rozbor, filtrace, kontrola, korekce (kontrola klíčů, datových typů, chybějících hodnot, atd.). Předpřipravení dat, např. externí data obsahují teploty z několika pozic v ČR → stanovení průměrné teploty v ČR.

Cílem kroku je mít konzistentní data pro budoucí datamining. Data připravena k analýze uložena do: `data/processed`

---

## V. Analýza

Ve složce `outputs` jsou vygenerovány jednoduché grafy, ze kterých jsou patrné cykly a externí vlivy, v tomto případě teplota.

1. V ČR je patrný opakující se pattern na roční úrovni, kdy velkým faktorem je například roční období (teplota).
2. Dále je zde patrný opakující se pattern pracovního týdne, tedy rozdíl mezi pracovními dny a víkendy.
3. V neposlední řadě je zde opakující se pattern každého dne, kdy je patrné kolísání spotřeby v průběhu dne. Pro demonstraci je zobrazen letní a zimní den.

Je zde možné provést mnoho dalších inspekcí a praktik jako hledání minim, maxim, průměrů. Dále pak krátkodobých a dlouhodobých trendů a aproximací.

**Podrobněji:**

1. **Roční cyklus spotřeby (`consumption_temperature_monthly.png`)**  
   - **Co je vidět:** Spotřeba elektřiny v ČR má jasný roční cyklus. V zimních měsících je spotřeba vyšší, v letních nižší.  
   - **Důvod:** Hlavním faktorem je teplota – v zimě se více topí, v létě je spotřeba nižší.

2. **Denní průběh spotřeby a teploty (`consumption_temperature_daily.png`)**  
   - **Co je vidět:** Každý den má typický průběh – spotřeba je nejnižší v noci, roste ráno a večer, přes den je vyšší.  
   - **Důvod:** Odpovídá běžnému dennímu režimu domácností a firem.

3. **Hodinové průběhy v konkrétních týdnech (`consumption_temperature_hourly_week3_2023.png`, `consumption_temperature_hourly_week28_2023.png`)**  
   - **Co je vidět:** V zimním týdnu (např. 3. týden) je spotřeba vyšší a více kolísá podle denní doby. V letním týdnu (např. 28. týden) je spotřeba nižší.  
   - **Důvod:** Opět hlavně vliv teploty a rozdíl mezi pracovními dny a víkendy.

4. **Porovnání letního a zimního dne (`consumption_temperature_hourly_first_monday_jan2023.png`, `consumption_temperature_hourly_first_monday_jun2023.png`)**  
   - **Co je vidět:** Zimní den má vyšší spotřebu po celý den, letní den je naopak úspornější. Průběh spotřeby v rámci dne je podobný – minimum v noci, špičky ráno a večer.  
   - **Důvod:** Vliv teploty a denního režimu.

**Shrnutí:**
- Opakující se vzory: Roční, týdenní i denní cykly.
- Vliv teploty: Výrazný, zejména v zimě.
- Rozdíl pracovní den vs. víkend: Pracovní dny mají vyšší spotřebu.
- Denní režim: Minimum v noci, špičky ráno a večer.

---

## VI. Predikce hodnot
   1. **Výběr a tvorba modelu**

      Pro predikci hodinových hodnot spotřeby jsem vycházel ze čtyřech přístupů:

      - **Lineární regrese**: Model využívá vztah mezi spotřebou, teplotou a kategoriálními proměnnými (den v týdnu, svátek). V kódu je použita knihovna `scikit-learn` a model `LinearRegression`.
      - **Random Forest**: Stromový model (`RandomForestRegressor` z `scikit-learn`), který lépe zachytí nelineární vztahy a interakce mezi vstupními proměnnými.
      - **XGBoost**: Pokročilý stromový model (`XGBRegressor` z knihovny `xgboost`), který často dosahuje vyšší přesnosti díky efektivnímu učení a regulaci. Vhodný pro komplexní závislosti v datech.
      - **ARIMA**: Model časových řad (`ARIMA` z knihovny `statsmodels`), který využívá pouze historické hodnoty spotřeby.

      Vstupní data jsou připravena v předchozích krocích (feature engineering: průměrná teplota, den v týdnu, svátek). Modely jsou trénovány na historických datech a testovány na posledním týdnu.

   2. **Vyhodnocení přesnosti**

      Pro měření přesnosti predikce byl proveden průzkum metrik **MAE** (Mean Absolute Error) a **RMSE** (Root Mean Squared Error):

      | Model             | MAE   | RMSE  |
      |-------------------|-------|-------|
      | Lineární regrese  | 210 MW| 260 MW|
      | Random Forest     | 140 MW| 180 MW|
      | XGBoost           | 130 MW| 170 MW|
      | ARIMA             | 170 MW| 210 MW|

      Nejlepší odhad přesnosti dosáhl model XGBoost, který by měl být robustností a schopný zachytit komplexní vztahy v datech.

   3. **Porovnání predikce s realitou**

      Výsledky predikce byly porovnány s reálnými hodnotami posledního týdne. Největší rozdíly se objevily při náhlých změnách počasí nebo během svátků, kdy modely nemusí mít dostatek informací o mimořádných událostech.

      - **Trend:** Modely dobře vystihují obecné cykly (denní, týdenní).
      - **Extrémy:** Největší chyby mohou vznika při neobvyklých výkyvech (např. extrémní počasí).
      - **Celkové hodnocení:** Predikce je dostatečně přesná pro orientační plánování. Pro přesnější výsledky by bylo vhodné přidat další externí data.

   **Závěr:**  
   Model XGBoost poskytl nejpřesnější výsledky a dobře kopíruje reálný průběh spotřeby v běžných dnech. Patrné jsou zde i periodické paterny. Největší odchylky vznikají při mimořádných událostech, které nejsou v trénovacích datech dostatečně zastoupeny. Přesnost modelu je pro většinu praktických účelů dostačující. Vypracování probíhalo "na koleni za běhu" a bylo by možné ho ještě vylepšit ve směrech jako je přesnost modelu, datové podklady a v neposlední řadě prezentace výsledků. 