import json
import re
from sacremoses import MosesDetokenizer

detokenizers = {
    "text_en": MosesDetokenizer(lang="en"),
    "text_de": MosesDetokenizer(lang="de"),
    "text_fr": MosesDetokenizer(lang="fr"),
    "text_it": MosesDetokenizer(lang="it"),
}

def detokenize_field(text, detokenizer):
    text = "\n".join(
        detokenizer.detokenize(line.split(" "))
        for line in text.split("\n")
    )
    # Moses leaves stray spaces around apostrophes in elisions/possessives/Swiss number separators
    # e.g. "l 'effettuazione" → "l'effettuazione", "l' auto" → "l'auto", "70 '000" → "70'000"
    text = re.sub(r"(\w) '(\w)", r"\1'\2", text)
    text = re.sub(r"(\w)' (\w)", r"\1'\2", text)
    # French typography inserts a space before : ; ! ? — remove as tokenization artifact
    text = re.sub(r" ([;:!?])", r"\1", text)
    # Moses detaches / and - from surrounding tokens
    # e.g. "2010 / 2011" → "2010/2011", "e - mobility" → "e-mobility"
    # Run in a loop because re.sub consumes the left \w, so chained cases like
    # "vis - à - vis" need multiple passes to fully collapse.
    for pattern, repl in [(r"(\w) / (\w)", r"\1/\2"), (r"(\w) - (\w)", r"\1-\2"), (r"(\w) – (\w)", r"\1–\2")]:
        prev = None
        while prev != text:
            prev = text
            text = re.sub(pattern, repl, text)
    return text

with open("swissgov_cleaned.json") as f:
    data = json.load(f)

for doc in data:
    for field, detokenizer in detokenizers.items():
        if doc.get(field):
            doc[field] = detokenize_field(doc[field], detokenizer)

with open("swissgov_cleaned_detokenized.json", "w") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Saved {len(data)} documents to swissgov_cleaned_detokenized.json")
