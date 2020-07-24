# Movie Recommendation
Movie Recommendation using Neo4j Database.


Initial Datasets required for the project can be found in this link : https://grouplens.org/datasets/movielens/


We create 7 datasets to build this structure. 3 of them for nodes (Users, Movies, Genres) and others for relationships. You can find details of below

### Nodes
1. **Users** (userId): It includes users’ id and it has only one column. It is created with using “ratings.csv” data. We create “Users” node and it will has relations with “Movies” and “Genres” nodes
2. **Movies** (movieId, title, rating_mean): It includes movies’ id, title and rating_mean fields. It is created with using “movies.csv” data. “Movies” node will has relations with “Users” and “Genres” nodes and it has also relationship to itself based on similarity
3. **Genres** (genres): It is small data it has 19 rows and it keeps genres

### Relationships
1. **Users_movies** (userId, movieId, rating): It uses to create a relationship between “Users” and “Movies” nodes.
2. **Movies_genres** (movieId, genres): It uses to create a relationship between “Movies” and “Genres” nodes.
3. **Users_genres** (userId, genres): It uses to create a relationship between “Users” and “Genres” nodes. “genres” is a calculated field. It includes the favorite genre of the users. To calculate the favorite genre, I use count of the genres from movies which is already watched by users. I thought to use movies’ ratings but after making some checks I decided to use counts
4. **Movies_similarity** (movieId, sim_movieId, relevance): It is the most critical dataset in this pipeline. It includes 5 rows for each movies and they are similar movies ids. I calculate similarity through movies. I use 3 groups of similarity and they are tag similarity, genre similarity and rating (rating, year, rating count) similarity. Then I mix them. It will be explained in details.

After executing the MovieRecommendation.py file and obtaining the datasets, we have to import the .csv files into the neo4j database. 
The data obtained from executing the python file can be found here : 
https://drive.google.com/drive/folders/1TgCJ4d7ssKlLTzfLwW2GGMwSdogIAiLp?usp=sharing

**Refer .pptx file for further info**

