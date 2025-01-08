import faiss
import numpy as np
import json
from sentence_transformers import SentenceTransformer

# Load course data from courses.json (scraped course details)
with open('courses.json', 'r') as f:
    courses = json.load(f)

# Initialize the pre-trained model for generating embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

# Extract course titles and generate embeddings for each title
course_titles = [course['title'] for course in courses]
embeddings = model.encode(course_titles)

# Convert embeddings to numpy array (FAISS requires numpy arrays)
embeddings = np.array(embeddings).astype('float32')

# Create a FAISS index for similarity search
index = faiss.IndexFlatL2(embeddings.shape[1])  # Using L2 distance metric

# Add embeddings to the FAISS index
index.add(embeddings)

# Save the FAISS index to a file (for future use)
faiss.write_index(index, "course_embeddings.index")

# Optionally save the course titles to map back results
with open('course_titles.json', 'w') as f:
    json.dump(course_titles, f, indent=4)

print("Embeddings generated and FAISS index created successfully!")

