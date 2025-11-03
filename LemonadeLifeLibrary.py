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
        "Arola"
    ]

def get_name_var_from_dict(itemsdict:dict) -> any:
    return itemsdict["name"]

def input_anything_to_continue(CustomText: str = "Enter anything to continue", CustomInputPrompt: str = "->") -> None:
    """By default print enter anything to continue and waits until its given an input. Will return none"""
    print(CustomText)
    input(CustomInputPrompt)

def ask_for_digit_and_check_in_dict(dictToCompare: dict) -> any:
    """Ask for an input until given input is a digit and in given dictionary"""
    while True:
        inputToCheck = input("->")
        if inputToCheck.isdigit() and int(inputToCheck) in dictToCompare:
            return dictToCompare[int(inputToCheck)]
        elif inputToCheck == "":
            return None
        else:
            print("Invalid number.\nTry again.")