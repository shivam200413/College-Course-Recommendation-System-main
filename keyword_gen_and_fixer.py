import pandas
from keybert import KeyBERT
import neattext.functions as nt_func


def keybert_loader():
    kw_model = KeyBERT(model='all-mpnet-base-v2')
    return kw_model

def data_simlifier(dataframe):
    dataframe["Simplified_Title"] = dataframe["course_title"].apply(nt_func.remove_stopwords)
    dataframe["Simplified_Title"] = dataframe["Simplified_Title"].apply(nt_func.remove_special_characters)
    dataframe["Simplified_Title"] = dataframe['Simplified_Title'].str.lower()
    dataframe["course_title_l"] = dataframe["course_title"].str.lower()
    return dataframe 



#Generates keywords in empty cells if the keyword_gen misses to fill empty cells
def keyword_fixer(dataframe, csv):
    kw_model = keybert_loader()
    
    i=0
    for keyword_list in dataframe['keywords']:
        try:
            x = eval(keyword_list)
        
        
        except:
            keywords = kw_model.extract_keywords(dataframe._get_value(i,"course_title_l"), keyphrase_ngram_range=(1,3), stop_words="english", highlight =False, top_n=10)
            keywords_list = list(dict(keywords).keys())
            dataframe.at[i,"keywords"] = keywords_list
            i+=1
    dataframe.to_csv(csv)



#Generates keywords
def keyword_gen(dataframe,csv):
    kw_model = keybert_loader()
    dataframe = data_simlifier(dataframe)
    dataframe['keywords'] = ""
    allkey_list = []
    for title in dataframe["course_title_l"]:
        keywords = kw_model.extract_keywords(title, keyphrase_ngram_range=(1,3), stop_words="english", highlight =False, top_n=10)
        keywords_list = list(dict(keywords).keys())
        #print(keywords_list)
    
        title_index = dataframe.index[dataframe["course_title_l"] == title].tolist()
        title_index = title_index[0]
        print(title_index)
        dataframe.at[title_index, "keywords"] = keywords_list

    dataframe.to_csv(csv) 


csv = input("Enter database file")

dataframe = pandas.read_csv(csv)

keyword_gen(dataframe,csv)
keyword_fixer(dataframe,csv)