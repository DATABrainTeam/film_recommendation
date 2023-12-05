# film_recommendation
Our film recommendation system harnesses the power of databases from TMDB and IMDB, meticulously selecting films based on a set of criteria to cater specifically to the unique demographics of the Creuse department, where the majority of the population is aged over 50.

Selection Criteria:
    Duration: Films ranging between 75 to 250 minutes.
    Production Year: Post-1950, with an exception for all French films.
    Content: No explicit content; excluding adult films.
    Origin: Films from the US, GB, European countries, Korea, and Japan.
    Language: Films translated into French or English.
    Quality Thresholds: Only films with a rating higher than the lowest quartile and a total number of votes exceeding 30 (median of total voting).
    Format: Exclusively films and shorts, excluding series, TV movies, and reality shows.

Specialization for Cinema:
Our system caters to a cinema specializing in popular French actors from the 60s to the 90s. The first page showcases five randomly chosen movies featuring these iconic actors.

Machine Learning Algorithm:

Features: The algorithm relies on various features for movie selection.
    Genre
    Presence of the top 200 actors, top 100 directors, and top 50 composers (given five times more weight than other features).
    Country of production.
    Keywords: Extracted using natural language processing, we selected 250 key words from the most frequent 500 words, aiding in determining film subjects.
    Coordinate System:

Each film is represented by a 1K-dimensional coordinate for the machine learning algorithm.

      
