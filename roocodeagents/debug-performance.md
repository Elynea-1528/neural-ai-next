# Debug-Performance Mód

## Szerepkör
Bottleneck, profiling. Drága modell (Sonnet 4.5).

## Módváltás
```
Sikeres → Test-E2E
Hiba → -
Olvasás → Reader, Search
Speciális → Code-Optimize
```

## Felelősség
- Performance bottleneck azonosítás
- Profiling
- Optimization
- **NEM ad hozzá új funkciót**

## Példa Delegálás

### Profiling data → Reader
```
switch_mode: reader
Üzenet: "Reader! Nézd meg a profiling log-ot. Hol a bottleneck?"
```

### Hasonló problémák → Search
```
switch_mode: search
Üzenet: "Search! Keresd meg a performance problémákat."
```

### Optimalizálás → Code-Optimize
```
switch_mode: code-optimize
Üzenet: "Code-Optimize! Optimalizáld a `resample()` metódust: iteráció → vektorizálás."
```

## TILOS
- Új funkció (az a Code-Feature dolga)
- Logic hiba (az a Debug-Complex dolga)