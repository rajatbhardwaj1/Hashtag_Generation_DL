import pandas as pd 
import yake 
df = pd.read_csv('data/dataset.csv')
kw_extractor = yake.KeywordExtractor(lan = "en"  ,windowsSize= 1 , top = 20 , stopwords=None);
doc = df.iat[0 , 0]
keywords = kw_extractor.extract_keywords(doc)
num_rows = len(df)

scores = 0 

for i in range(0 , num_rows):
    curr_score = 0 
    doc = df.iat[i,0]
    doc = doc.lower()
    keywords = kw_extractor.extract_keywords(doc)
    list_of_hashtags = []
    for word, cs in keywords:
        list_of_hashtags.append(word) 
    human_keywords = df.iat[i,1].split(",")
    for word in human_keywords:
        if word in list_of_hashtags:
            curr_score = curr_score + 1 
    curr_score = curr_score / len(human_keywords)
    scores = scores + curr_score 
        
scores = (scores / num_rows) * 100 
print(scores)


# test

