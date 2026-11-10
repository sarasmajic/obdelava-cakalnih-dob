import pandas as pd

datoteka = "tedensko_cakalne.xlsx"
izhodna_datoteka = "cakalne_dobe_obdelano.csv"

# posegi ki jih klinika UKC Ljubljana  izvaja
ukc_ljubljana_klinike = {
    "Kardiološki pregled - prvi": "UKC LJUBLJANA INTERNA KLINIKA",
    "Operacija sive mrene (katarakte)": "UKC LJUBLJANA OCESNA KLINIKA",
    "Endoproteza kolka delna (PEP)/totalna (TEP)": "UKC LJUBLJANA - ORTOPEDSKA KLINIKA",
    "Operacija kile": "UKC LJUBLJANA KIRURŠKA KLINIKA",
    "Endoproteza kolena": "UKC LJUBLJANA - ORTOPEDSKA KLINIKA"
}

# preberemo podatke iz Excela
podatki = pd.read_excel(datoteka, sheet_name="Tb 02")

koncna_tabela = []

# gremo čez vsak poseg posebej (ključi in vrednosti slovarja hkrati)
for poseg, naziv_klinike in ukc_ljubljana_klinike.items():
    vrstice = podatki[
        (podatki["Naziv izvajalca"] == naziv_klinike) &
        (podatki["VZS naziv"] == poseg)
    ]

    # lahko bi preverjali tudi ce je "vrstice" prazno ampak ni smislna, ker so obdelani podatki tukaj rocno vpisani
    # podatki so obdelani tako, da zaupamo viru, da podatkov ne podvaja in so zagotovljeni

    vrstica = vrstice.iloc[0]

    cakalna_doba = vrstica["ČD na prvi prosti termin REDNO"]
    cakajocih = vrstica["Število čakajočih Redno"]
    nad_dopustno = vrstica["Število čakajočih NAD dop. ČD Redno"]

    # delež čakajočih nad najdaljšo dopustno čakalno dobo
    if pd.notna(cakajocih) and pd.notna(nad_dopustno) and cakajocih > 0:
        delez = round(100 * nad_dopustno / cakajocih, 1) #izracuno delez cakajocih nad dopustno dobo
    else:
        delez = ""

    # če posamezen podatek manjka, pustimo prazno vrednost
    if pd.notna(cakalna_doba):
        cakalna_doba = int(cakalna_doba)
    else:
        cakalna_doba = ""

    if pd.notna(cakajocih):
        cakajocih = int(cakajocih)
    else:
        cakajocih = ""

    if pd.notna(nad_dopustno):
        nad_dopustno = int(nad_dopustno)
    else:
        nad_dopustno = ""

    koncna_tabela.append({
        "izvajalec": naziv_klinike,
        "poseg": poseg,
        "cakalna_doba_dni": cakalna_doba,
        "stevilo_cakajocih": cakajocih,
        "stevilo_nad_dopustno": nad_dopustno,
        "delez_nad_dopustno_pct": delez
    })

# shranimo v CSV datoteko
tabela = pd.DataFrame(koncna_tabela)
tabela.to_csv(izhodna_datoteka)

print()
print(tabela.to_string)
print()
print("Podatki so shranjeni", izhodna_datoteka)