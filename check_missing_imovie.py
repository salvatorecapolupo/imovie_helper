import plistlib, glob, os, re

library_path = os.path.expanduser("/Users/salvatore/Movies/Libreria iMovie2.imovielibrary")

missing = []
for root, dirs, files in os.walk(library_path):
    for f in files:
        if not f.endswith(".plist"):
            continue
        path = os.path.join(root, f)
        try:
            with open(path, "rb") as fh:
                data = plistlib.load(fh)
        except:
            continue
        # Cerca ricorsivamente stringhe che sembrano path
        def check(obj):
            if isinstance(obj, str) and obj.startswith("/"):
                if not os.path.exists(obj):
                    missing.append((path, obj))
            elif isinstance(obj, dict):
                for v in obj.values(): check(v)
            elif isinstance(obj, list):
                for v in obj: check(v)
        check(data)

for plist_file, missing_path in missing:
    print(f"MANCANTE: {missing_path}\n  (ref in {plist_file})\n")
