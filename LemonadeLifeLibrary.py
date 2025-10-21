def get_girl_name_list() -> list[str]:
    return [
        "Anna",
        "Anni",
        "Alina",
        "Alisa",
        "Aino",
        "Astrid",
        "Eerika",
        "Enni",
        "Esteri",
        "Minttu",
        "Minja",
        "Moona",
        "Monna",
        "Nella",
        "Niina",
        "Olivia",
        "Onerva",
        "Piia",
        "Pinja",
        "Ronja",
        "Siiri",
        "Siina",
        "Satu",
        "Sylvi",
        "Terhi",
        "Tiina",
        "Tiia",
        "Taina",
        "Viivi",
        "Venla"
    ]

def get_boy_name_list() -> list[str]:
    return [
        "Antto",
        "Aarni",
        "Ahmed",
        "Aron",
        "Aaron",
        "Alvar",
        "Antti",
        "Arttu",
        "Aimo",
        "Eetu",
        "Elias",
        "Konsta",
        "Lukas",
        "Oskari",
        "Pekka"
    ]

def generate_last_name() -> list[str]:
    return [
        "Korhonen",
        "Virtanen",
        "Mäkinen",
        "Nieminen",
        "Mäkelä",
        "Hämäläinen",
        "Laine",
        "Heikkinen",
        "Koskinen",
        "Järvinen",
        "Rutanen",
        "Kuikka",
        "Leino",
        "Saarinen",
    ]

def get_name_var_from_dict(itemsdict:dict) -> any:
    return itemsdict["name"]