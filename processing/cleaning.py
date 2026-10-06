def clean_text(value):
    if value is None:
        return None

    value = str(value)

    
    value = value.replace("\xa0", " ")

    
    value = value.replace("\n", " ")
    value = value.replace("\t", " ")

  
    value = " ".join(value.split())

    return value

def strip_quotes(value):
    if value is None:
        return None

    value = clean_text(value)

    if value.startswith("“") and value.endswith("”"):
        value = value[1:-1]

    elif value.startswith('"') and value.endswith('"'):
        value = value[1:-1]

    return value

def clean_price(value):
    if value is None:
        return None

    value = clean_text(value)

   
    value = value.replace("£", "").strip()

    try:
        return float(value)
    except ValueError:
        return None

def clean_rating(value):
    if value is None:
        return None

    if isinstance(value, int):
        return value

    rating_words = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }

    value = clean_text(value)

    if value in rating_words:
        return rating_words[value]

    try:
        rating = int(value)

        if 1 <= rating <= 5:
            return rating

    except ValueError:
        return None

    return None

def clean_tags(value):
    if value is None:
        return ""

    if isinstance(value, list):
        tags = value
    else:
        tags = str(value).split(";")

    cleaned_tags = []

    for tag in tags:
        tag = clean_text(tag)

        if tag:
            cleaned_tags.append(tag.lower())

    cleaned_tags = sorted(set(cleaned_tags))

    return ";".join(cleaned_tags)

def normalize_url(value):
    if value is None:
        return None

    value = clean_text(value)

    if value.startswith("http://") or value.startswith("https://"):
        return value

    return None