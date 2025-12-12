import html
import json
import re
from statistics import mean

import folium
from branca.element import MacroElement, Template

RAW_DATA = """1\tGIC DJOUMA\t\tBamguel, Maroua \tExtreme nord\t14° 03′ Est\t10° 48′ N
2\tNDOUMESSI\t\tKribi, Centre\tSud\t9,9167° E\t2,9250° N
3\tGIC PRODUCTEURS DES OIGNONS \t675020727\tNord\tNord\t13.393389\t9.3226016
4\tGIC PRODUCTEURS DES PEPINIERES DE MAYO-LOUE\t699701299\tNord\tNord\t13,2174246° E\t8,2410564° N
5\tGIC MADINA DES PRODUCTEURS DES CULTURES MARAICHERES DE BARGARAM\t652591465\tIlarifa, Extreme nord\t Extreme nord\t14° 57' 00" Est\t12° 26' 24" N
6\t"groupe des élèves de Volaille de
Rouge "\t676502725\tDonry-BENOUE\tNord\t13.393389\t9.3226016
7\tSociété coopérative simplifiée des éleveurs de poulet, de chair\t691772660\tNASSARAO-GAROUA\tNord\t13° 11′ 00″ Est\t9° 20′ 00″ Nord
8\tMandu, à Wawo, épouse Mbakom\t696112432\tfoumbot\tOuest\t10° 37' 57.00" E\t5° 30' 28.91" N
9\tGROUPE D'INITIATIVE COMMUNE DES PRODUCTEURS ET COMMERCANTS DES FRUITS DU MAYO-DANAY\t698252640\tCaïcaï, dans le quartier Mangal(maroua)\t Extreme nord\t15.0284567° E\t10.6667589° N
10\tSCOOPS PROD. MAÏS ET OIGNONS KOZA\t696676662\tCaïcaï, dans le quartier Mangal(maroua)\t Extreme nord\t15.0284567° E\t10.6667589° N
11\tSOCIETE COOPERATIVE AVEC CONSEIL D'ADMINISTRATION DES PRODUCTEURS D'OIGNON DE NGONG\t695245414\tTamoundé, en allant vers Tukalongo\tLittoral\t13° 10′ 60″ Est\t13.1833 9° 1′ 0″ Nord
12\tSociété des Producteurs d'Oignons\t69000012\tDockbar, en allant vers Tamoundé\tLittoral\t13° 10′ 60″ Est\t 13.1833 9° 1′ 0″ Nord
13\tNOPING\t691027853\tDOUALA\tLittoral\t9° 41′ 08″ E\t4° 03′ 05″ N
14\tSanaga Farms\t699612687\tBAFOUSSAM\tOuest\t10° 25' 3.32" E\t5° 28' 39.90" N
15\tMadame Saïz épouse Wemny\t677766234 / 696606480\tYaoundé et à Ebolowa\tSud\t11° 08' 60.00" E\t2° 54' 59.99" N
16\tCoopérative d'éleveurs de canards et de poulets de Bupindi\t674853303\tBipindi\tSud\t10° 24' 59.99" E\t3° 04' 60.00" N
17\tTIOMELA CLOTILDE\t675151364\tfoumbot\tOuest\t10° 37' 57.00" E\t5° 30' 28.91" N
18\tGROUPE D'INITIATIVE COMMUNE DE FABRICATION NATURELLE DE YAOURT DU LITTORAL CENTRE\t699788027\tLittoral\tLittoral\t9° 41′ 08″ E\t4° 03′ 05″ N
19\tGIC DES PRODUCTRICES DE MANIOC\t678227820\tLittoral\tLittoral\t9° 41′ 08″ E\t4° 03′ 05″ N
20\t"LYCEE DE GARI-GOMBO
 "\t651942556\tLittoral\tLittoral\t9° 41′ 08″ E\t4° 03′ 05″ N
21\tSOCIETE COOPERATIVE AVEC CONSEIL D'ADMINISTRATION AGROPASTORALE DES ACTEURS DU DEVELOPPEMENT DE NITOUKOU\t677750389\tTshukou,\tExtreme nord\t10° 52' 48.00"E\t4° 37' 48.00"N
22\tGroupe Initiatives Communes Agropastoral\t677-76-6234 / 696-60-6480\tFOUMBOT\tOuest\t10° 37' 57.00" E\t5° 30' 28.91" N
23\tSOCIETE COOPERATIVE SIMPLIFIEE RECOLTE 237 FERME NKOUE\t690767345\tYaoundé \tCentre\t12.343439\t7.365302
24\t"SOCIÉTÉ COOPERATIVE SIMPLIFIEE DES PRODUCTEURS DE PATATE DE BONJONG
 "\t697324852\tAdamaoua\tAdamaoua\t13° 31' 50.56"E\t6° 20' 1.18"N
25\tSCOOPS PTASPL\t656102611\tyaoundé\tCentre\t12.343439\t7.365302
26\tSOCIETE COOPERATIVE AVEC CONSEIL D'ADMINISTRATION DES PRODUCTEURS DE MANIOC WARACK MADIKOUM\t696492700\tAdamaoua\tAdamaoua\t78° 49' 26.785" E\t28° 3' 38.65" N
27\tLeprince \t698843700\t\t\t\t
28\tSTE COOP-CA DE PRODUCTION ET TRANSFORMATION DE MANIOC ET ACTIVITÉS CONNEXES DE MBANGASSINA\t675493737\t\tCentre\t11° 42′ 25″ est\t4° 37′ 47″ nord
29\tSOCIETE COOPÉRATIVE AVEC CONSEIL D'ADMINISTRATION DES PRODUCTEURS DE MANIOC SAPE DE BERTOUA\t691977154\tBertoua\tEst\t13° 41′ 04″ est\t4° 34′ 30″ nord
30\tcoopacam - \t699814462\tMFOU\tCentre\t11° 38′ 00″ est\t4° 27′ 00″ nord
31\tSCOOP MAN DE MBALMAYO\t696819231\tMbalmayo\tCentre\t11° 30′ est\t3° 31′ nord
32\tMaraiamou\t696255220\tMaroua\tExtreme Nord\t14° 19′ est\t10° 35′ nord
33\tGroupe produccteur de poisson\t682247271\tBenbis à sangmelina\tSud\t12° 27' Est\t3° 26' Nord
34\tVente poisson fumé\t695752643\tBertoua\tEst\t13° 41′ 04″ est\t4° 34′ 30″ nord
35\tVente poulet fumé\t695752643\tBertoua\tEst\t13° 41′ 04″ est\t4° 34′ 30″ nord
36\tGic producteur de Haricot\t67038821\tFoumbot\tOuest\t10° 37' 57.00" E\t5° 30' 28.91" N
37\tintegrity-fruits\t\tDouala\tLittoral\t9° 41′ 08″ E\t4° 03′ 05″ N
38\tGic producteur de poissonHenri Samet au numéro \t699 90 92 98\tKribi, Centre\tCentre\t9,9167° E\t2,9250° N
39\tmakou-epse-fotsing-delphine \t\tDouala\tLittoral\t9° 41′ 08″ E\t4° 03′ 05″ N
40\torganisation interprofessionnelle de la filière lait de vaches au Cameroun\t698319292\tTCHABAM-FARO\tNord\t1° 25' 0.829" E\t9° 1' 46.265" N
41\tMélanie Tekaneng\t698336566\tBertoua\tEst\t13° 41′ 04″ est\t4° 34′ 30″ nord
42\tMoisso-Michel\t694884692\tKRIBI\tSud\t9,9167° E\t2,9250° N
43\tPompou Mangac\t697181400\tmbang-BATOURI\tEst\t14° 22' 0" Est\t 4° 25' 60" Nord
44\tsociété coopérative\t656 02 80 82\tNDOM,AKONOLINGA\tCentre\t12° 15' 00'' E\t3° 46' 00'' N
45\tNYANO Patrice\t699936505\tNkolbisson YAOUNDE\tCentre\t11° 27′ 18″ est\t3° 52′ 19″ nord
46\tKINDAG adlist sarl\t653 90 79 49\tMakak Centre \tCentre\t11° 01′ 40″ est\t3° 32′ 55″ nord
47\tsociété Harris Yaourt\t670 10 09 31\tYaoundé Ngoa ékelle\tCentre\t11° 49′ 59″ est\t3° 59′ 10″ nord
48\tSCOOPS C.A.B.K.J\t690,777,710\tNgaoundéré\tAdamaoua\t13° 35′ est\t7° 19′ nord
			Mfou			
49\tGIC FAPAC DE MFOU\t699989564\tMfou\tCentre\t11° 38′ 00″ est\t4° 27′ 00″ nord
50\t"OMBOLO BELLA du GIC JAEO d’Obala
"\t678200307\tObala\tCentre\t11° 32′ 00″ est\t4° 10′ 00″ nord
51\tETS AGRITECH YAOUNDE\t670545408\tYaoundé odza\tCentre\t11° 32' 0" East\t3° 47' 0" North
52\tGic nel-agro\t69995991\tNkolafamba \tCentre\t11° 39′ 53″ est\t3° 51′ 32″ nord,
53\tGIC ESPERANCE\t675820484\t\t\t\t
54\tGIC AIDONS NOUS D'OBALA\t656529861\tEKOUMDOUM\tCentre\t11° 32′ 00″ est\t3° 49′ 00″ nord
55\tBANANA GROUP\t677649089\tSimaleng yaoundé\tCentre\t11° 33' 7.19" E\t3° 43' 12.59" N
56\tSCOOPS SAPAS\t693521000\tGuidè au nord\tNord\t10°10'53.6"E\t36°48'23.4"N
57\tGIC AGRONE de Nanga Eboko \t673434672/679229967\tNanga Eboko \tCentre\t12° 22′ 00″\test\t4° 41′ 00″ nord
58\t"GIC LA RESERVE, à Djoandjila,
"\t694 16 99 10\tDjoandjila\t\t\t
59\tGIC MAIN VERTE, à Batchenga\t699428768\tBatchenga\tCentre\t11° 39′ 00″ est\t4° 17′ 00″ nord
60\tGIC UNION FAIT LA FORCE DE PANGARI \t677 64 70 25\tPANGARI \tadamaoua\t13° 21′ 45″ est\t 6° 00′ 36″ nord
61\tAGRIDEVERT\t653359507\tADAMAWA / BANQUIM\tAdamaoua\t11.1333° E\t6.2833° N
62\tGKIBIA AGROPORT\t674158302\tADAMAWA / BANQUIM\tAdamaoua\t11.1333° E\t6.2833° N
63\tBEGEL SARL à Mindourou\t 699 771 423/696 006 048\tMindourou\tEst\t13.5394° E\t3.4158° N
64\tL'UNION DES SOCIETES COOPERATIVES AVEC CONSEIL D'ADMINISTRATION DES TRANSFORMATEURS DE LAIT DE MAROUA 1ER\t696154363\tNord\tNord\t13.393389\t9.3226016
65\tsociété Aris Yaourt\t670 10 09 31\tYaoundé Ngoa ékelle\tCentre\t11° 49' 59" Est\t3° 59' 10" Nord
66\tGIC GENGAL\t677605789\tSoa\tCentre\t11° 35′ 45″ est\t3° 58′ 41″ nord
67\tONGOLA EDZIMBI EPSE NDJOCK NGUIDJOL ELISABETH LAETITIA\t691191603\tFandena\tCentre\t11° 32′ 27″ Est\t3° 53′ 07″ Nord
68\tsociété Gic Niyya femme prod lait MINDIF\t697996495\tMindif departement Maye kany\textreme nord\t14° 26′ est\t10° 24′ nord
69\tATADJAM EPSE BAKARY\t6-94-53-32-32\tMAROUA, DOMAYO, BAR LAITIER NDJAREN\textreme nord\t14° 09′ Est\t10° 33′ Nord
70\tDAKGO POLYCARPE\t677-003157\tDouala\tlittoral\t9° 41′ 08″ E\t 9.01667
"""


def merge_rows(raw: str):
    rows = []
    buffer = ""
    for line in raw.splitlines():
        candidate = f"{buffer} {line}".strip() if buffer else line
        parts = candidate.split("\t")
        if len(parts) >= 7:
            if len(parts) > 7:
                parts = parts[:6] + [" ".join(parts[6:])]
            rows.append([part.strip() for part in parts[:7]])
            buffer = ""
        else:
            buffer = candidate
    if buffer:
        tail_parts = buffer.split("\t")
        if len(tail_parts) > 7:
            tail_parts = tail_parts[:6] + [" ".join(tail_parts[6:])]
        rows.append([part.strip() for part in tail_parts])
    return rows


def pick_direction(coord: str, is_lat: bool):
    lookup = {
        "N": "N",
        "NORD": "N",
        "NORTH": "N",
        "S": "S",
        "SUD": "S",
        "SOUTH": "S",
        "E": "E",
        "EST": "E",
        "EAST": "E",
        "O": "W",
        "W": "W",
        "OUEST": "W",
        "WEST": "W",
    }
    for token in lookup:
        if re.search(rf"\\b{token}\\b", coord, flags=re.IGNORECASE):
            return lookup[token]
    return "N" if is_lat else "E"


def to_decimal(coord: str, *, is_lat: bool):
    if not coord:
        return None
    coord = coord.replace("\u00a0", " ").replace(",", ".")
    direction = pick_direction(coord, is_lat=is_lat)
    numbers = [float(n) for n in re.findall(r"[-+]?\d+(?:\.\d+)?", coord)]
    if not numbers:
        return None
    if len(numbers) > 3:
        numbers = numbers[-3:]
    if len(numbers) == 1:
        decimal = numbers[0]
    elif len(numbers) == 2:
        deg, minutes = numbers
        decimal = abs(deg) + minutes / 60
    else:
        deg, minutes, seconds = numbers
        decimal = abs(deg) + minutes / 3600 * 60 + seconds / 3600
    if direction in {"S", "W"}:
        decimal *= -1
    return decimal


def build_dataset():
    entries = []
    for row in merge_rows(RAW_DATA):
        if not row or not row[0].strip().isdigit():
            continue
        _, name, tel, city, region, lon_raw, lat_raw = row
        lat = to_decimal(lat_raw, is_lat=True)
        lon = to_decimal(lon_raw, is_lat=False)
        if lat is None or lon is None:
            continue
        entries.append(
            {
                "name": name,
                "tel": tel,
                "city": city,
                "region": region,
                "lat": lat,
                "lon": lon,
            }
        )
    return entries


def build_map(output_file: str = "index.html"):
    data = build_dataset()
    if not data:
        raise RuntimeError("Aucune donnée géographique valide trouvée.")

    center = (mean([item["lat"] for item in data]), mean([item["lon"] for item in data]))
    fmap = folium.Map(location=center, zoom_start=6, tiles="OpenStreetMap")

    data_js = json.dumps(data, ensure_ascii=False)
    search_template = Template(
        f"""
        {{% macro html(this, kwargs) %}}
        <div id="company-search-panel" style="position:absolute;top:10px;left:10px;z-index:1000;background:white;padding:8px;border-radius:6px;box-shadow:0 2px 8px rgba(0,0,0,0.3);display:flex;gap:6px;align-items:center;flex-wrap:wrap;">
            <input id="company-search-input" type="text" placeholder="Rechercher une entreprise" style="flex:1;min-width:220px;padding:6px 8px;border:1px solid #ccc;border-radius:4px;" />
            <button id="company-search-btn" style="padding:6px 10px;border:1px solid #007bff;background:#007bff;color:white;border-radius:4px;cursor:pointer;">Recherche</button>
            <div id="company-search-feedback" style="width:100%;font-size:12px;color:#555;margin-top:4px;"></div>
        </div>
        <script>
        (function() {{
            const data = {data_js};
            function getMap() {{
                for (const key in window) {{
                    try {{
                        if (window[key] && window[key] instanceof L.Map) return window[key];
                    }} catch (e) {{}}
                }}
                return null;
            }}
            const map = getMap();
            if (!map) return;

            const markers = {{}};
            data.forEach((item) => {{
                const marker = L.circleMarker([item.lat, item.lon], {{
                    radius: 5,
                    color: '#3388ff',
                    weight: 2,
                    fill: false,
                }}).addTo(map);
                const popupHtml = `<b>${{item.name}}</b><br>Région : ${{item.region}}<br>Ville / zone : ${{item.city}}<br>Tél : ${{item.tel || '—'}}`;
                marker.bindPopup(popupHtml);
                marker.bindTooltip(item.name);
                markers[item.name.toLowerCase()] = marker;
            }});

            const input = document.getElementById('company-search-input');
            const feedback = document.getElementById('company-search-feedback');
            const btn = document.getElementById('company-search-btn');

            function focusOn(item) {{
                const marker = markers[item.name.toLowerCase()];
                map.setView([item.lat, item.lon], 10);
                if (marker) marker.openPopup();
            }}

            function search() {{
                const term = (input.value || '').trim().toLowerCase();
                if (!term) {{
                    feedback.textContent = 'Saisir un nom.';
                    return;
                }}
                const match = data.find(d => d.name.toLowerCase().includes(term));
                if (!match) {{
                    feedback.textContent = 'Aucun résultat.';
                    return;
                }}
                feedback.textContent = `Affichage : ${{match.name}}`;
                focusOn(match);
            }}

            btn.addEventListener('click', search);
            input.addEventListener('keypress', (e) => {{
                if (e.key === 'Enter') search();
            }});
        }})();
        </script>
        {{% endmacro %}}
        """
    )
    macro = MacroElement()
    macro._template = search_template
    fmap.get_root().add_child(macro)

    fmap.save(output_file)
    print(f"Carte mise à jour générée dans {output_file} avec {len(data)} points.")


if __name__ == "__main__":
    build_map()
