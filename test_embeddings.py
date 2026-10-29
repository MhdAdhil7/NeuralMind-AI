from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

model = SentenceTransformer("all-MiniLM-L6-v2")

sentences = [
    "The puppy enjoys playing.",
    "The young dog likes to play.",
    "The car needs fuel."
]

embeddings = model.encode(sentences)

similarity_1 = cos_sim(embeddings[0], embeddings[1])
similarity_2 = cos_sim(embeddings[0], embeddings[2])

print("Puppy vs young dog:", similarity_1.item())
print("Puppy vs car:", similarity_2.item())