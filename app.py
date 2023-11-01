import streamlit as st
import pandas as pd
import random

# Load data
data = pd.read_csv("newdata.csv")

# Function to get book recommendations based on genre and author
def get_recommendations(book_name, author, interaction_matrix, num_recommendations=2):
    filtered_books = data[((data['genre'] == genre) || (data['author'] == author)) & (data['book name'] != book_name)]
    if filtered_books.empty:
        return None
    
    random_recommendations = filtered_books.sample(min(num_recommendations, len(filtered_books)))
    return random_recommendations[['book id', 'book name', 'author', 'genre', 'Price', 'Rating', 'publication', 'number of pages']]

# Streamlit app
def main():
    
    st.set_page_config(
        page_title="Book Recommender",
        page_icon="📚",
    )

    st.title("Book Recommender")
    st.markdown("Discover personalized book recommendations.")
    
    # User input
    book_name = st.selectbox("Select Book Name", data['book name'].unique())
    author = st.selectbox("Select Author", data['author'].unique())
   
    # Recommendation button
    if st.button("Get Recommendations"):
        recommendations = get_recommendations(book_name, author, data)
        
        if recommendations is not None and not recommendations.empty:
            st.subheader("Recommended Books:")
            st.table(recommendations)
        else:
            st.subheader("No Recommendations Found")

if __name__ == "__main__":
    main()
