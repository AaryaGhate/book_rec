import streamlit as st
import pandas as pd
import random
from sklearn.metrics.pairwise import cosine_similarity

# Load data
data = pd.read_csv("newdata.csv")

# Create interaction matrix and find similarity
interaction_matrix = data.pivot_table(index='User ID', columns='book id', values='Rating', fill_value=0)
product_similarity = cosine_similarity(interaction_matrix.T)

# Function to get book recommendations based on book name, author or genre
def get_recommendations(user_id, book_name, attribute, interaction_matrix, product_similarity, num_recommendations=2):
    if user_id not in interaction_matrix.index:
        return None
    
    user_interactions = interaction_matrix.loc[user_id].values
    
    if attribute == 'author':
        attribute_values = data['author']
    elif attribute == 'genre':
        attribute_values = data['genre']
    else:
        raise ValueError("Invalid attribute. Use 'author' or 'genre'.")
    
    attribute_indices = attribute_values[attribute_values == book_name].index
    similar_scores = product_similarity[attribute_indices].mean(axis=0)
    recommended_indices = similar_scores.argsort()[-num_recommendations:][::-1]
    recommended_books = interaction_matrix.columns[recommended_indices]
    
    return recommended_books

# Streamlit app
def main():
    
    st.set_page_config(
        page_title="Book Recommender",
        page_icon="📚",
    )

    st.title("Book Recommender")
    st.markdown("Discover personalized book recommendations.")
    
    # User input
    user_id = st.number_input("Enter User ID", min_value=1, max_value=1000)
    book_name = st.selectbox("Select Book Name", data['book name'].unique())
    attribute_type = st.radio("Select Attribute for Similarity", ('author', 'genre'))
   
    # Recommendation button
    if st.button("Get Recommendations"):
        recommendations = get_recommendations(user_id, book_name, attribute_type, interaction_matrix, product_similarity)
        
        if recommendations is not None and len(recommendations) > 0:
            random_recommendations = random.sample(list(recommendations), min(2, len(recommendations)))
        
            # Display recommended books
            st.subheader("Recommended Books:")
            recommended_books_info = data[data['book id'].isin(random_recommendations)][['book id', 'book name', 'author', 'genre', 'Price', 'Rating', 'publication', 'number of pages']]
            
            if not recommended_books_info.empty:
                st.table(recommended_books_info)
            else:
                st.subheader("No Recommendations Found")
        else:
            st.subheader("No Recommendations Found")

if __name__ == "__main__":
    main()
