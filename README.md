# movie_recommended_system

CineMatch is a content-based movie recommendation system built with Python and deployed as an
interactive web application using Streamlit. The system analyses a movie's metadata — genres, keywords,
cast, crew, and plot overview — and recommends the most similar films from a database of approximately
4,800 TMDB movies. Real-time movie posters, ratings, runtime, and overviews are fetched live from The
Movie Database (TMDB) API.
 Key Highlights
•   Content-based filtering using Cosine Similarity on NLP feature vectors
•   4,800+ movies from the TMDB 5000 dataset
•   Live movie metadata fetching via TMDB REST API
•   Dual view modes: Card View and List View
•   Personal Watchlist stored in Streamlit session state
•   Configurable number of recommendations (3–10)
•   Fully responsive dark-themed UI with custom CSS

