# imovie_helper

Diagnostica dei file media mancanti in un progetto iMovie tramite terminale e Python.

## Problema

iMovie segnala "file multimediali mancanti" senza indicare quali. Il progetto è un bundle (directory mascherata) che contiene file `.plist` con riferimenti assoluti ai media originali. Se un file è stato spostato, rinominato o cancellato, il riferimento rimane ma il file non esiste più.

## Requisiti

- macOS
- Python 3 (incluso nel sistema)
- Nessuna dipendenza esterna

## Utilizzo

### 1. Trova il bundle del progetto

```bash
find ~/Movies -name "*.imovielibrary" -o -name "*.imoviemovie" 2>/dev/null
```

### 2. Esegui lo script

Modifica `library_path` con il percorso reale del tuo progetto, poi:

```bash
python3 check_missing.py
```

### 3. Interpreta l'output

Per ogni file mancante viene stampato:

```
MANCANTE: /percorso/assoluto/al/file.mov
  (ref in /percorso/al/file.plist)
```

Se l'output è vuoto, tutti i file referenziati esistono su disco.

## Script

```python
# check_missing.py
import plistlib, os

library_path = os.path.expanduser("~/Movies/NomeProgetto.imovielibrary")

missing = []

for root, dirs, files in os.walk(library_path):
    for f in files:
        if not f.endswith(".plist"):
            continue
        path = os.path.join(root, f)
        try:
            with open(path, "rb") as fh:
                data = plistlib.load(fh)
        except Exception:
            continue

        def check(obj):
            if isinstance(obj, str) and obj.startswith("/"):
                if not os.path.exists(obj):
                    missing.append((path, obj))
            elif isinstance(obj, dict):
                for v in obj.values():
                    check(v)
            elif isinstance(obj, list):
                for v in obj:
                    check(v)

        check(data)

if missing:
    for plist_file, missing_path in missing:
        print(f"MANCANTE: {missing_path}\n  (ref in {plist_file})\n")
else:
    print("Nessun file mancante trovato.")
```

## Note

- I plist in formato binario vengono letti correttamente da `plistlib`. Se un plist è corrotto o in formato non standard, viene silenziosamente ignorato.
- Se vuoi convertire manualmente un plist in XML leggibile: `plutil -convert xml1 file.plist -o output.xml`
- I file media originali di iMovie si trovano tipicamente in `~/Movies/iMovie Library.imovielibrary/` organizzati per data di importazione.

## Risoluzione

Una volta identificati i file mancanti, le opzioni sono:

1. **Ripristinare i file** nei percorsi originali (o usare `ln -s` per symlink).
2. **Reimportare i media** in iMovie e ricollegarli manualmente nella timeline.
3. **File irrecuperabili**: rimuovere le clip corrispondenti dalla timeline prima di esportare.
