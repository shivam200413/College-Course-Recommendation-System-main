import pandas
import neattext.functions as nt_func
import numpy
from sklearn.metrics.pairwise import cosine_similarity, linear_kernel
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from keybert import KeyBERT


dataframe = pandas.read_csv("courses_with_keywords_test.csv")




kw_model = KeyBERT(model='all-mpnet-base-v2')
i=0

for keyword_list in dataframe['keywords']:
    
    
    
    try:
        x = eval(keyword_list)
        
        
    except:
        keywords = kw_model.extract_keywords(dataframe._get_value(i,"course_title_l"), keyphrase_ngram_range=(1,3), stop_words="english", highlight =False, top_n=10)
        keywords_list = list(dict(keywords).keys())
        print(keywords_list)
        print(i) 
        dataframe.at[i,"keywords"] = keywords_list

    
    i+=1



dataframe.to_csv('courses_with_keywords_test.csv') 