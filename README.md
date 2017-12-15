# Sentimental Analysis & Clustering using Mobile App Review (NLP)

1. Data Collection
  * Scraping reviews from play.google.com

2. Make Pipeline to store data into mongoDB Collection (EC2, RDS)

3. Bring collection as DataFrame and do somethings like preprocessing and so on.

4. Sentimental Analysis (Positive: 5 star, Negative: 1 to 4 star)
  * Using Konlpy (Twitter, mecab, kkma)
  * CountVectorizer, TFIDF
  * ngram_range, stopwords, min_df, max_df
  * Naive Bayes, Logistic Regression, RandomForest, Support Vector Machine
  
5. Clustering over Negative reviews(1-4 star)
  * gensim Word2Vec --> LDA or other algorithm
    * other algorithm: Making Weight Vector using 'Core keywords' of assessing mobile app. Then dot product with TDM(Term-Document Matrix, Binary CountVectorizer can do it!) ==> Classify documents as keywords with high scores.
    
6. Making Web Service using python Flask (To-do)


