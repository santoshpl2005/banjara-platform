import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('stopwords')

# Keyword-to-category mapping for Banjara topics
TOPIC_MAP = {
    'festival': ['teej', 'navratri', 'holi', 'diwali', 'sevalal', 'banjara', 'festival', 'celebration'],
    'temple': ['temple', 'mandir', 'sevalal', 'yatrasthal', 'pilgrimage', 'worship', 'devsthan'],
    'dress': ['dress', 'costume', 'clothing', 'outfit', 'ghagra', 'traditional', 'attire', 'jewellery'],
    'music': ['music', 'song', 'dance', 'geet', 'instrument', 'folk', 'natak'],
    'language': ['language', 'gor boli', 'gormat', 'dialect', 'word', 'speak'],
    'history': ['history', 'origin', 'migration', 'ancient', 'tribe', 'community', 'lamani'],
    'recipe': ['food', 'recipe', 'dish', 'cook', 'eat', 'traditional food', 'bajra', 'jowar'],
    'handicraft': ['craft', 'embroidery', 'art', 'handmade', 'textile', 'bead', 'jewelry'],
}

def get_answer(query, mysql):
    tokens = word_tokenize(query.lower())
    stop_words = set(stopwords.words('english'))
    keywords = [w for w in tokens if w not in stop_words and w.isalpha()]

    detected_category = None
    for category, words in TOPIC_MAP.items():
        if any(kw in words for kw in keywords):
            detected_category = category
            break

    cur = mysql.connection.cursor()

    if detected_category == 'temple':
        cur.execute("SELECT name, description FROM temples LIMIT 3")
        rows = cur.fetchall()
        if rows:
            return "Here are some Banjara pilgrimage sites: " + \
                   "; ".join([f"{r[0]}: {r[1][:120]}..." for r in rows])

    if detected_category in ('festival', 'dress', 'music', 'language', 'history', 'handicraft'):
        cur.execute("SELECT title, description FROM cultural_content WHERE category=%s LIMIT 3",
                    (detected_category,))
        rows = cur.fetchall()
        if rows:
            return f"About Banjara {detected_category}: " + \
                   "; ".join([f"{r[0]} – {r[1][:120]}..." for r in rows])

    if detected_category == 'recipe':
        cur.execute("SELECT name, ingredients FROM recipes LIMIT 3")
        rows = cur.fetchall()
        if rows:
            return "Traditional Banjara dishes: " + \
                   ", ".join([r[0] for r in rows])

    # Fallback: full-text keyword search
    cur.execute("""
        SELECT title, description FROM cultural_content
        WHERE MATCH(title, description) AGAINST(%s IN NATURAL LANGUAGE MODE)
        LIMIT 3
    """, (query,))
    rows = cur.fetchall()
    if rows:
        return "Related results: " + "; ".join([f"{r[0]}: {r[1][:100]}..." for r in rows])

    return ("I couldn't find specific information about that. "
            "Try asking about Banjara festivals, temples, dress, music, language, or recipes.")