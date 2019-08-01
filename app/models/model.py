def fetchCard(card_name):
    base = 'https://api.scryfall.com/cards/named?fuzzy='
    card_name=card_name.lower()
    card_name=card_name.replace(" ","+")
    return base + card_name

# def populatePage():
    