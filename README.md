# MusicRecommenderSystem using Spotify API Dataset
## Heavy research based project that works with english language as well as hindi songs, pioneering a novel task of a mixed playlist, using content based filtering. 
- Provided a collaborative based filtering method but due to no users only the means has been provided i.e. MySQL database for all user data and history of playlists and rating by the user. 

- The data collected has been on our own and tarining is also done on local systems.

- Also provided a login and signup process for users and other advanced feature. But i'm here to discuss the implementation of such or any recommendation system (they are all the same in the working).
  
# Data
This project takes in training data of about 10000 songs for our purpose, and their respective artist, date period, genre, sub genre, language, and other metadata like - tempo, chords, MFCC, spectral features, and similar 30 features appx. 
- Any new song can be added by downloading and the program will automatically extract features and add the song to the database.
# Method
1.First we address the cold start problem which says that any new user with no previous data will not be provided with accurate recommendations. For that we ask the user to select their preferences and make a playlist based on which we will recommend songs.

2.Second comes the content based filtering which basically uses above mentioned features of the song (or metadata) and implements KNN algorithm to find the best match of songs that the user history provides, using that and Deep learning algorithms we find the next 10 best songs according to the rating is provided to the user.

3.Third is the collaborative filtering which takes in all the other users' history and preferences and find the best neighbours of the current user for which the recommendations are to be made. These users are recommended the songs that their best match listens and vice versa. This algorithm is the most accurate method to provide recommendations but the limitation is the cold start problem and sometimes the content based method provides better solution. For these situations the above two methods are used.
