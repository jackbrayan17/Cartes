import re
import pandas as pd

def normalize_coord(coord, is_longitude=True):
    if pd.isna(coord):
        return None

    coord = str(coord).strip().replace(",", ".")  # uniformiser

    # Identifier direction
    direction = None
    possible_dirs = ["N", "S", "E", "O", "W", "EST", "OUEST", "NORD", "SUD"]
    for d in possible_dirs:
        if d.lower() in coord.lower():
            direction = d.upper()
            break

    mapping = {"EST": "E", "OUEST": "W", "NORD": "N", "SUD": "S", "O": "W"}
    direction = mapping.get(direction, direction)

    # Essayer conversion decimal
    numbers = re.findall(r"[-+]?\d*\.\d+|\d+", coord)
    if numbers:
        val = float(numbers[0])
        return decimal_to_dms(val, direction, is_longitude)

    # Format DMS déjà présent
    numbers = [int(n) for n in re.findall(r"(\d+)", coord)]
    if numbers:
        deg = numbers[0]
        min_ = numbers[1] if len(numbers) > 1 else 0
        sec = numbers[2] if len(numbers) > 2 else 0
        if not direction:
            direction = default_direction(is_longitude, deg)
        return f'{deg}° {min_:02d}\' {sec:02d}" {direction}'

    return None

def default_direction(is_longitude, deg):
    if is_longitude:
        return "E" if deg >= 0 else "W"
    else:
        return "N" if deg >= 0 else "S"

def decimal_to_dms(decimal, direction, is_longitude):
    if not direction:
        direction = default_direction(is_longitude, decimal)

    decimal = abs(decimal)
    deg = int(decimal)
    minutes_float = (decimal - deg) * 60
    min_ = int(minutes_float)
    sec = int(round((minutes_float - min_) * 60))  # arrondi pour Excel
    return f'{deg}° {min_:02d}\' {sec:02d}" {direction}'

def process_file(input_excel, output_excel):
    df = pd.read_excel(input_excel, sheet_name="Analyse resultats")
    df = df.dropna(axis=1, how="all").dropna(axis=0, how="all")
    df = df.iloc[:, :12]
    df.columns = [
        "#", "Nom", "Tel", "Ville", "longitude", "latitude",
        "Effectif", "Volume_prod", "Structure_accomp",
        "CA_FCFA", "Filieres", "Produits"
    ]

    # Normalisation
    df["longitude"] = df["longitude"].apply(lambda x: normalize_coord(x, True))
    df["latitude"] = df["latitude"].apply(lambda x: normalize_coord(x, False))

    df.to_excel(output_excel, index=False)
    print("✔ Coordonnées normalisées dans :", output_excel)

# Run
process_file("carte.xlsm", "coordonnees_normalisees2.xlsx")
