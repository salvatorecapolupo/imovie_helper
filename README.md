# imovie_helper

Systematic diagnosis of missing media files in an iMovie project using the terminal and Python.

![problem example](Screenshot 2026-05-09 alle 06.56.23.png)

## Problem

iMovie reports "missing media files" without specifying which ones. A project is a bundle (a directory disguised as a single file) containing `.plist` files that hold absolute paths to the original media. If a file has been moved, renamed, or deleted, the reference remains while the file no longer exists on disk.

## Requirements

- macOS
- Python 3 (included with the system)
- No external dependencies

## Usage

### 1. Locate the project bundle

```bash
find ~/Movies -name "*.imovielibrary" -o -name "*.imoviemovie" 2>/dev/null
```

### 2. Run the script

Set `library_path` to the actual path of your project, then:

```bash
python3 check_missing.py
```

### 3. Read the output

Each missing file is reported as:

```
MISSING: /absolute/path/to/file.mov
  (referenced in /path/to/file.plist)
```

If the output is empty, all referenced files exist on disk.

## Script

```python
# check_missing.py
import plistlib, os

library_path = os.path.expanduser("~/Movies/YourProject.imovielibrary")

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
        print(f"MISSING: {missing_path}\n  (referenced in {plist_file})\n")
else:
    print("No missing files found.")
```

## Notes

- Binary plists are handled correctly by `plistlib`. Corrupted or non-standard plists are silently skipped.
- To manually convert a binary plist to readable XML: `plutil -convert xml1 file.plist -o output.xml`
- iMovie's original media files are typically stored under `~/Movies/iMovie Library.imovielibrary/`, organised by import date.

## Resolution

Once missing files are identified, the options are:

1. **Restore the files** to their original paths, or use `ln -s` to create symlinks pointing to their new location.
2. **Re-import the media** into iMovie and relink the clips manually in the timeline.
3. **Unrecoverable files**: remove the corresponding clips from the timeline before exporting.

# imovie_helper

Diagnostica dei file media mancanti in un progetto iMovie tramite terminale e Python.

![problem example](Screenshot 2026-05-09 alle 06.56.23.png)

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
