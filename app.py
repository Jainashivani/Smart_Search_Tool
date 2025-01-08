import faiss
import numpy as np
import json
from sentence_transformers import SentenceTransformer
import gradio as gr

# Load the pre-trained SentenceTransformer model for embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load the course data and FAISS index
with open('courses.json', 'r') as f:
    courses = json.load(f)

# Load the FAISS index
index = faiss.read_index("course_embeddings.index")

# Load the course titles (which corresponds to the embeddings)
with open('course_titles.json', 'r') as f:
    course_titles = json.load(f)

# Function to generate query embedding and search for similar courses
def search_courses(query):
    # Generate the embedding for the input query
    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding).astype('float32')
    
    # Search for the top 3 most similar courses using the FAISS index
    D, I = index.search(query_embedding, k=3)  # D: distances, I: indices
    
    # Retrieve the top courses based on the indices
    top_courses = [courses[i] for i in I[0]]
    
    # Format results to display
    results = []
    for course in top_courses:
        results.append(f"**Title**: {course['title']}\n**Price**: {course['price']}\n[Link to Course]({course['link']})\n")
    
    return "\n".join(results)

# Set up Gradio interface
def course_search_interface(query):
    return search_courses(query)
print("App is starting...")
gr.Interface(fn=course_search_interface, 
             inputs="text", 
             outputs="text", 
             title="Analytics Vidhya Course Search", 
             description="Enter a search query to find the most relevant free courses on Analytics Vidhya.").launch()
