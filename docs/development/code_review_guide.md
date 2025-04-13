# Code Review Útmutató

Ez az útmutató a Neural-AI-Next projektben alkalmazott kód felülvizsgálati (code review) folyamatot és szempontokat tartalmazza. A code review célja a kód minőségének biztosítása, a hibák korai felismerése és a tudásmegosztás elősegítése.

## 1. Code Review Alapelvek

### 1.1. Konstruktív visszajelzés
- Fókuszálj a kódra, ne a szerzőre
- Fogalmazz javaslatként, ne parancsként
- Indokold meg a javaslataidat
- Dicsérj, ha valami jól van megcsinálva

### 1.2. Hatékonyság
- Törekedj a gyors visszajelzésre (24-48 órán belül)
- Először a nagyobb problémákra koncentrálj
- Ne vessz el a formázási kérdésekben (ezeket automatizáljuk)

## 2. Ellenőrzési szempontok

### 2.1. Funkcionális szempontok
- [ ] A kód megvalósítja az Issue-ban leírt követelményeket
- [ ] Helyesen kezeli a szélsőséges eseteket (edge case)
- [ ] Megfelelően kezeli a hibákat és kivételeket
- [ ] A kimenet formátuma és tartalma megfelelő

### 2.2. Kód minőség
- [ ] Követi a projekt kódolási konvencióit
- [ ] Világos, érthető változó- és függvénynevek
- [ ] Nincsenek duplikált kódrészletek
- [ ] Megfelelő absztrakció és modularitás
- [ ] A függvények egy felelősség elvét követik (Single Responsibility Principle)
- [ ] Optimális teljesítmény és erőforrás-használat

### 2.3. Tesztelés
- [ ] Megvannak a megfelelő unit tesztek
- [ ] A tesztek lefedik a főbb funkcionalitást és edge case-eket
- [ ] A tesztek függetlenek és megismételhetők
- [ ] A teszt név világosan jelzi, mit tesztel

### 2.4. Dokumentáció
- [ ] A kód megfelelően dokumentált (docstrings, kommentek)
- [ ] A README vagy más dokumentáció frissítve lett, ha szükséges
- [ ] Az API változásokat dokumentálták

## 3. Code Review Folyamat

### 3.1. Előkészületek
1. Ellenőrizd, hogy a PR leírása tartalmazza a szükséges információkat
2. Győződj meg róla, hogy az automatizált tesztek sikeresek
3. Nézd át a kapcsolódó Issue-t és a kontextust

### 3.2. A review menete
1. Először átfutás a teljes PR-en, hogy megértsd a változtatás célját és struktúráját
2. A fájlok részletes áttekintése, kezdve a kritikusabbakkal
3. Megjegyzések hozzáadása az észrevételekhez
4. Összefoglaló visszajelzés írása a PR-hez

### 3.3. Döntéshozatal
1. **Approve**: Ha a változtatás megfelelő és készen áll a mergelésre
2. **Request changes**: Ha kritikus problémák vannak, amelyeket javítani kell
3. **Comment**: Ha észrevételeid vannak, de nem blokkolják a PR-t

## 4. Gyakori Review Megjegyzések

### Példák hasznos review megjegyzésekre
- "Ez a függvény túl hosszú és nehezen olvasható. Javaslom kisebb, fókuszált függvényekre bontani."
- "Itt lehetne használni a már létező X segédfüggvényt a duplikáció elkerülése érdekében."
- "Ez a rész nem kezeli azt az esetet, amikor Y bemenet üres. Tudnál hozzáadni egy ellenőrzést?"
- "Jó megoldás, hogy X-et használtad Y helyett, ez sokkal hatékonyabb."

### Kerülendő megjegyzések
- "Ez a kód rossz."
- "Nem így kell csinálni."
- "Írd át az egészet."
- Személyeskedő vagy lekezelő megjegyzések

## 5. Utókövetés

1. A PR szerzője javítja a felvetett problémákat
2. A reviewer ellenőrzi a javításokat
3. Ha minden rendben, a PR elfogadásra kerül
4. A PR mergelése és lezárása
