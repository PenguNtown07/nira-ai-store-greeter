import re


# ==================================================
# DETECT SKIN TYPE
# ==================================================

def detect_skin_type(message):

    message = message.lower().strip()

    # ----------------------------------------------
    # CHECK WHETHER CUSTOMER IS TALKING ABOUT HAIR
    # ----------------------------------------------

    hair_context_words = [
        "hair",
        "scalp",
        "shampoo",
        "conditioner",
        "frizz",
        "frizzy",
        "haircare",
        "hair care"
    ]

    has_hair_context = any(
        word in message
        for word in hair_context_words
    )

    # ----------------------------------------------
    # EXPLICIT SKIN TYPES
    # ----------------------------------------------

    if any(
        phrase in message
        for phrase in [
            "oily skin",
            "very oily skin",
            "skin is oily",
            "skin gets oily",
            "my skin is oily"
        ]
    ):
        return "Oily"

    if any(
        phrase in message
        for phrase in [
            "dry skin",
            "very dry skin",
            "skin is dry",
            "skin feels dry",
            "my skin is dry"
        ]
    ):
        return "Dry"

    if any(
        phrase in message
        for phrase in [
            "combination skin",
            "combination skin type"
        ]
    ):
        return "Combination"

    if any(
        phrase in message
        for phrase in [
            "normal skin",
            "normal skin type"
        ]
    ):
        return "Normal"

    if any(
        phrase in message
        for phrase in [
            "sensitive skin",
            "very sensitive skin",
            "skin is sensitive"
        ]
    ):
        return "Sensitive"

    # ----------------------------------------------
    # GENERIC TERMS
    # ----------------------------------------------
    # Only interpret generic "dry", "oily", etc.
    # as skin-related when the customer is NOT
    # clearly discussing hair.

    if not has_hair_context:

        if "oily" in message:
            return "Oily"

        if "dry" in message:
            return "Dry"

        if "sensitive" in message:
            return "Sensitive"

    return None


# ==================================================
# DETECT SKIN CONCERN
# ==================================================

def detect_skin_concern(message):

    message = message.lower().strip()

    # ----------------------------------------------
    # ACNE / BREAKOUTS
    # ----------------------------------------------

    if any(
        phrase in message
        for phrase in [
            "acne",
            "acne-prone",
            "acne prone",
            "breakout",
            "breakouts",
            "pimples",
            "pimple",
            "blemishes"
        ]
    ):
        return "Breakouts"

    # ----------------------------------------------
    # DULLNESS
    # ----------------------------------------------

    if any(
        phrase in message
        for phrase in [
            "dullness",
            "dull skin",
            "dull-looking skin",
            "dull looking skin",
            "my skin looks dull",
            "skin looks dull",
            "dull"
        ]
    ):
        return "Dullness"

    # ----------------------------------------------
    # DRYNESS / DEHYDRATION
    # ----------------------------------------------

    # Avoid interpreting hair dryness as skin dryness.

    hair_context_words = [
        "hair",
        "scalp",
        "shampoo",
        "conditioner",
        "frizz",
        "frizzy"
    ]

    has_hair_context = any(
        word in message
        for word in hair_context_words
    )

    if not has_hair_context:

        if any(
            phrase in message
            for phrase in [
                "dryness",
                "dehydrated skin",
                "dehydration",
                "skin feels dehydrated",
                "skin feels dry",
                "dry skin"
            ]
        ):
            return "Dryness"

    # ----------------------------------------------
    # SUN PROTECTION
    # ----------------------------------------------

    if any(
        phrase in message
        for phrase in [
            "sunscreen",
            "sun protection",
            "sun exposure",
            "uv protection",
            "protect my skin from the sun",
            "protect my skin from sun"
        ]
    ):
        return "Sun Protection"

    # ----------------------------------------------
    # OIL CONTROL
    # ----------------------------------------------

    if any(
        phrase in message
        for phrase in [
            "oil control",
            "excess oil",
            "too much oil",
            "oily skin",
            "skin gets oily",
            "skin is oily"
        ]
    ):
        return "Oil Control"

    return None


# ==================================================
# DETECT HAIR CONCERN
# ==================================================

def detect_hair_concern(message):

    message = message.lower().strip()

    # ----------------------------------------------
    # SCALP CARE
    # ----------------------------------------------

    if any(
        phrase in message
        for phrase in [
            "scalp",
            "scalp care",
            "scalp problem",
            "scalp concern",
            "itchy scalp"
        ]
    ):
        return "Scalp Care"

    # ----------------------------------------------
    # HAIR DAMAGE
    # ----------------------------------------------

    if any(
        phrase in message
        for phrase in [
            "damaged hair",
            "hair damage",
            "hair is damaged",
            "very damaged hair",
            "repair my hair",
            "repair damaged hair"
        ]
    ):
        return "Hair Damage"

    # ----------------------------------------------
    # FRIZZ / DRY HAIR
    # ----------------------------------------------

    if any(
        phrase in message
        for phrase in [
            "frizzy hair",
            "frizzy",
            "frizz",
            "dry hair",
            "hair is dry",
            "very dry hair",
            "dry and frizzy hair"
        ]
    ):
        return "Frizz and Dryness"

    # ----------------------------------------------
    # HAIR CLEANSING
    # ----------------------------------------------

    if any(
        phrase in message
        for phrase in [
            "shampoo",
            "hair cleansing",
            "clean my hair",
            "cleanse my hair",
            "cleansing my hair"
        ]
    ):
        return "Hair Cleansing"

    return None


# ==================================================
# DETECT BUDGET
# ==================================================

def detect_budget(message):

    message = message.lower().strip()

    patterns = [

        # ₹800
        r"₹\s?(\d+)",

        # Rs 800 / Rs. 800
        r"rs\.?\s?(\d+)",

        # under 800
        r"under\s+₹?\s?(\d+)",

        # below 800
        r"below\s+₹?\s?(\d+)",

        # less than 800
        r"less\s+than\s+₹?\s?(\d+)",

        # within 800
        r"within\s+₹?\s?(\d+)",

        # budget of 800
        r"budget\s+(?:of\s+)?₹?\s?(\d+)",

        # budget is 800
        r"budget\s+(?:is\s+)?₹?\s?(\d+)",

        # spend 800
        r"spend\s+(?:up\s+to\s+)?₹?\s?(\d+)",

        # don't want to spend more than 800
        r"spend\s+more\s+than\s+₹?\s?(\d+)",

        # maximum 800
        r"maximum\s+₹?\s?(\d+)",

        # max 800
        r"max\s+₹?\s?(\d+)"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            message
        )

        if match:

            return int(
                match.group(1)
            )

    return None


# ==================================================
# DETECT SHOPPING INTENT
# ==================================================

def detect_shopping_intent(message):

    message = message.lower().strip()

    # ----------------------------------------------
    # BROWSING
    # ----------------------------------------------

    if any(
        phrase in message
        for phrase in [
            "just browsing",
            "only browsing",
            "just looking",
            "just exploring",
            "only looking",
            "just checking",
            "just checking things out"
        ]
    ):
        return "Browsing / Exploring"

    # ----------------------------------------------
    # BEGINNER
    # ----------------------------------------------

    if any(
        phrase in message
        for phrase in [
            "new to skincare",
            "new to skin care",
            "beginner",
            "skincare beginner",
            "never used skincare",
            "never tried skincare",
            "don't know where to start",
            "dont know where to start",
            "don't know what i need",
            "dont know what i need",
            "i have no idea what i need",
            "completely new to skincare"
        ]
    ):
        return "Beginner / Uncertain"

    # ----------------------------------------------
    # GIFT SHOPPING
    # ----------------------------------------------

    if any(
        phrase in message
        for phrase in [
            "for my sister",
            "for my brother",
            "for my mother",
            "for my mom",
            "for my father",
            "for my dad",
            "for my friend",
            "for my girlfriend",
            "for my boyfriend",
            "for someone else",
            "as a gift",
            "gift",
            "gift for"
        ]
    ):
        return "Gift Shopping"

    # ----------------------------------------------
    # ROUTINE SHOPPING
    # ----------------------------------------------

    if any(
        phrase in message
        for phrase in [
            "routine",
            "complete routine",
            "full routine",
            "skincare routine",
            "haircare routine",
            "hair care routine",
            "multiple products",
            "several products",
            "build a routine",
            "build my routine"
        ]
    ):
        return "Routine Shopper"

    # ----------------------------------------------
    # SINGLE PRODUCT
    # ----------------------------------------------

    if any(
        phrase in message
        for phrase in [
            "one product",
            "single product",
            "just one",
            "only one"
        ]
    ):
        return "Single Product Shopper"

    # ----------------------------------------------
    # DEFAULT
    # ----------------------------------------------

    return "Product Exploration"


# ==================================================
# DETECT CUSTOMER CONSTRAINTS
# ==================================================

def detect_constraints(message):

    message = message.lower().strip()

    constraints = []

    # ----------------------------------------------
    # NO CROSS-SELLING
    # ----------------------------------------------

    if any(
        phrase in message
        for phrase in [
            "only want one",
            "only want one product",
            "just one product",
            "just want one",
            "only one product",
            "don't recommend anything else",
            "dont recommend anything else",
            "do not recommend anything else",
            "don't suggest anything else",
            "dont suggest anything else",
            "do not suggest anything else",
            "nothing else",
            "no extras",
            "no additional products",
            "don't need anything else",
            "dont need anything else"
        ]
    ):
        constraints.append(
            "No Cross-Selling"
        )

    # ----------------------------------------------
    # SIMPLICITY
    # ----------------------------------------------

    if any(
        phrase in message
        for phrase in [
            "keep it simple",
            "something simple",
            "simple routine",
            "simple skincare routine",
            "not too many products",
            "don't want too many products",
            "dont want too many products",
            "minimal routine",
            "minimal skincare"
        ]
    ):
        constraints.append(
            "Prefers Simplicity"
        )

    # ----------------------------------------------
    # PRICE SENSITIVITY
    # ----------------------------------------------

    if any(
        phrase in message
        for phrase in [
            "too expensive",
            "very expensive",
            "expensive",
            "can't afford",
            "cannot afford",
            "cheaper option",
            "more affordable",
            "affordable option",
            "budget-friendly",
            "budget friendly",
            "cheap option"
        ]
    ):
        constraints.append(
            "Price Sensitive"
        )

    # ----------------------------------------------
    # DISCOUNT / VALUE SEEKING
    # ----------------------------------------------

    if any(
        phrase in message
        for phrase in [
            "discount",
            "offer",
            "deal",
            "value for money",
            "best value",
            "save money",
            "saving"
        ]
    ):
        constraints.append(
            "Value Seeking"
        )

    return constraints


# ==================================================
# CREATE CUSTOMER PROFILE
# ==================================================

def analyze_customer(message):

    profile = {

        "skin_type": detect_skin_type(message),

        "skin_concern": detect_skin_concern(message),

        "hair_concern": detect_hair_concern(message),

        "budget": detect_budget(message),

        "shopping_intent": detect_shopping_intent(message),

        "constraints": detect_constraints(message)
    }

    return profile