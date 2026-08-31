import csv
import os


# ==================================================
# PRODUCT DATABASE
# ==================================================

PRODUCT_FILE = "products.csv"


# ==================================================
# LOAD PRODUCTS
# ==================================================

def load_products():

    products = []

    if not os.path.exists(PRODUCT_FILE):

        raise FileNotFoundError(
            f"{PRODUCT_FILE} was not found."
        )

    with open(
        PRODUCT_FILE,
        "r",
        encoding="utf-8-sig"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            try:
                row["price"] = int(
                    float(row["price"])
                )

            except (ValueError, TypeError):
                row["price"] = 0

            products.append(row)

    return products


# ==================================================
# PRODUCT CONTEXT
# ==================================================

def create_product_context():

    products = load_products()

    context = ""

    for product in products:

        context += f"""
Product: {product["product_name"]}
Price: ₹{product["price"]}
Category: {product["category"]}
Primary Need: {product["primary_need"]}
Suitable For: {product["suitable_for"]}
Key Benefit: {product["key_benefit"]}
Complementary Products: {product["complementary_products"]}
Bundle: {product["bundle"]}

"""

    return context


# ==================================================
# FORMAT COMPLETE CATALOGUE
# ==================================================

def format_all_products():

    products = load_products()

    face_products = []
    hair_products = []

    for product in products:

        if product["category"].lower() == "face care":
            face_products.append(product)

        elif product["category"].lower() == "hair care":
            hair_products.append(product)

    output = ""

    output += "### Face Care\n\n"

    for product in face_products:

        output += (
            f"**{product['product_name']}** — "
            f"₹{product['price']}\n"
            f"{product['key_benefit']}\n\n"
        )

    output += "### Hair Care\n\n"

    for product in hair_products:

        output += (
            f"**{product['product_name']}** — "
            f"₹{product['price']}\n"
            f"{product['key_benefit']}\n\n"
        )

    return output


# ==================================================
# PRODUCT COUNT
# ==================================================

def get_product_count():

    products = load_products()

    return len(products)


# ==================================================
# DETECT PRODUCT COUNT REQUEST
# ==================================================

def is_product_count_request(message):

    message = message.lower()

    phrases = [
        "how many products",
        "how many product",
        "number of products",
        "product count",
        "total products",
        "how many items",
        "how many items do you have"
    ]

    return any(
        phrase in message
        for phrase in phrases
    )


# ==================================================
# DETECT CATALOGUE REQUEST
# ==================================================

def is_catalogue_request(message):

    message = message.lower()

    phrases = [
        "show all products",
        "show me all products",
        "show me the products",
        "show all your products",
        "give me all products",
        "give me the product list",
        "show product list",
        "complete product list",
        "full product list",
        "all products",
        "product catalogue",
        "product catalog",
        "entire catalogue",
        "entire catalog"
    ]

    return any(
        phrase in message
        for phrase in phrases
    )


# ==================================================
# FIND PRODUCT BY NAME
# ==================================================

def find_product_by_name(user_message):

    message = user_message.lower()

    products = load_products()

    for product in products:

        product_name = (
            product["product_name"]
            .lower()
        )

        # Exact product name
        if product_name in message:
            return product

        # Match meaningful words
        product_words = (
            product_name
            .replace("-", " ")
            .split()
        )

        meaningful_words = [
            word
            for word in product_words
            if len(word) > 3
            and word != "nira"
        ]

        if not meaningful_words:
            continue

        matches = sum(
            1
            for word in meaningful_words
            if word in message
        )

        if matches == len(meaningful_words):
            return product

    return None


# ==================================================
# DETECT PRODUCT EXISTENCE QUESTION
# ==================================================

def is_product_existence_question(user_message):

    message = user_message.lower()

    phrases = [
        "do you sell",
        "do you have",
        "is there",
        "is this product available",
        "do you stock",
        "available",
        "have you got"
    ]

    return any(
        phrase in message
        for phrase in phrases
    )


# ==================================================
# DETECT SPECIFIC PRODUCT REQUEST
# ==================================================

def is_specific_product_request(user_message):

    message = user_message.lower()

    product_words = [
        "serum",
        "cleanser",
        "moisturizer",
        "moisturiser",
        "sunscreen",
        "shampoo",
        "conditioner",
        "mask",
        "cream",
        "oil",
        "toner"
    ]

    question_phrases = [
        "do you sell",
        "do you have",
        "is there",
        "available",
        "looking for",
        "want"
    ]

    has_product_word = any(
        word in message
        for word in product_words
    )

    has_question_phrase = any(
        phrase in message
        for phrase in question_phrases
    )

    return (
        has_product_word
        and has_question_phrase
    )


# ==================================================
# FIND RELEVANT PRODUCTS
# ==================================================

def get_relevant_products(profile):

    products = load_products()

    relevant_products = []

    skin_type = profile.get("skin_type")
    skin_concern = profile.get("skin_concern")
    hair_concern = profile.get("hair_concern")
    budget = profile.get("budget")

    for product in products:

        score = 0

        suitable_for = (
            product["suitable_for"]
            .lower()
        )

        primary_need = (
            product["primary_need"]
            .lower()
        )

        need_match = False
        type_match = False

        # ------------------------------------------
        # SKIN CONCERN
        # ------------------------------------------

        if skin_concern:

            concern = skin_concern.lower()

            if concern == "breakouts":

                if (
                    "breakout" in primary_need
                    or "acne" in primary_need
                ):
                    need_match = True

            elif concern == "dullness":

                if (
                    "dull" in primary_need
                    or "bright" in primary_need
                ):
                    need_match = True

            elif concern == "dryness":

                if (
                    "dry" in primary_need
                    or "hydration" in primary_need
                ):
                    need_match = True

            elif concern == "sun protection":

                if "sun protection" in primary_need:
                    need_match = True

            elif concern == "oil control":

                if "oil control" in primary_need:
                    need_match = True

        # ------------------------------------------
        # HAIR CONCERN
        # ------------------------------------------

        if hair_concern:

            concern = hair_concern.lower()

            if concern == "scalp care":

                if "scalp" in primary_need:
                    need_match = True

            elif concern == "frizz and dryness":

                if (
                    "frizz" in primary_need
                    or "dryness" in primary_need
                ):
                    need_match = True

            elif concern == "hair damage":

                if (
                    "damage" in primary_need
                    or "repair" in primary_need
                ):
                    need_match = True

            elif concern == "hair cleansing":

                if "cleansing" in primary_need:
                    need_match = True

        # ------------------------------------------
        # SKIN TYPE
        # ------------------------------------------

        if skin_type:

            skin = skin_type.lower()

            if (
                skin in suitable_for
                or "all skin types" in suitable_for
            ):
                type_match = True

        # ------------------------------------------
        # RELEVANCE FILTER
        # ------------------------------------------

        if skin_concern or hair_concern:

            if not need_match:
                continue

        # ------------------------------------------
        # SCORING
        # ------------------------------------------

        if need_match:
            score += 5

        if type_match:
            score += 3

        # ------------------------------------------
        # BUDGET
        # ------------------------------------------

        if budget:

            if product["price"] <= budget:
                score += 2
            else:
                score -= 4

        # ------------------------------------------
        # KEEP PRODUCT
        # ------------------------------------------

        if score > 0:

            relevant_products.append(
                (score, product)
            )

    # ------------------------------------------
    # SORT
    # ------------------------------------------

    relevant_products.sort(
        key=lambda item: item[0],
        reverse=True
    )

    return [
        product
        for score, product in relevant_products
    ]


# ==================================================
# FORMAT RELEVANT PRODUCTS
# ==================================================

def format_relevant_products(products):

    if not products:

        return (
            "No strongly matching NIRA "
            "products were identified."
        )

    context = ""

    for product in products:

        context += f"""
Product: {product["product_name"]}
Price: ₹{product["price"]}
Category: {product["category"]}
Primary Need: {product["primary_need"]}
Suitable For: {product["suitable_for"]}
Key Benefit: {product["key_benefit"]}
Complementary Products: {product["complementary_products"]}
Bundle: {product["bundle"]}

"""

    return context