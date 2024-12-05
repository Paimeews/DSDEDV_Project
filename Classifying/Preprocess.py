import nltk
import json
import os
from glob import glob

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

def preprocess_text(text):
    text = text.strip().lower()
    lemmatizer = nltk.stem.WordNetLemmatizer()
    words = text.split()
    words = [lemmatizer.lemmatize(word) for word in words if word not in nltk.corpus.stopwords.words('english')]
    return ' '.join(words)

root_folders = ['2018/', '2019/', '2020/', '2021/', '2022/', '2023/']
count1 = 0
count2 = 0
count3 = 0

abstracts_list = []
citation_title_list = []
author_keywords_list = []
lit_info_list = []

for root in root_folders:
    data_files = glob(os.path.join(root, '**/*'), recursive=True)
    for json_file in data_files:
        print(f"Processing file: {json_file}")
        unique_for_file = {}
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                citation_title = (
                        data.get("abstracts-retrieval-response", {})
                        .get("item", {})
                        .get("bibrecord", {})
                        .get("head", {})
                        .get("citation-title", str)
                    )
                if (citation_title):
                    citation_title_list.append(preprocess_text(citation_title))
                    unique_for_file['citation_title'] = preprocess_text(citation_title)
                else:
                    count1 += 1
                    unique_for_file['citation_title'] = ''
                
                abstracts = (
                        data.get("abstracts-retrieval-response", {})
                        .get("item", {})
                        .get("bibrecord", {})
                        .get("head", {})
                        .get("abstracts", str)
                    )
                if (abstracts):
                    abstracts_list.append(preprocess_text(abstracts))
                    unique_for_file['abstracts'] = preprocess_text(abstracts)
                else:
                    count2 += 1
                    abstracts_list.append("")
                    unique_for_file['abstracts'] = ''
                
                author_keywords = (
                        data.get("abstracts-retrieval-response", {})
                        .get("authkeywords",{})
                    )
                if (author_keywords):
                    author_keyword = author_keywords.get("author-keyword", [])
                    unique_auth_keyword = set()
                    for akw in author_keyword:
                        if isinstance(akw, dict) and "$" in akw:
                            unique_auth_keyword.add(akw['$'])
                        else:
                            unique_auth_keyword.add(author_keyword['$'])
                    author_keywords_list.append(list(unique_auth_keyword))
                    unique_for_file['author_keywords'] = list(unique_auth_keyword)
                else:
                    count3 += 1
                    author_keywords_list.append('')
                    unique_for_file['author_keywords'] = ''

                lit_info_list.append(unique_for_file)
                    
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in file {json_file}: {e}")
        except Exception as e:
            print(f"Error processing file {json_file}: {e}")
    print(count1, count2, count3)

    abstract_output_file = "Classifying/" + root + "/abstracts.json"
    citation_title_output_file = "Classifying/" + root + "/citation_title.json"
    author_keywords_output_file = "Classifying/" + root + "/author_keywords.json"
    literature_info_output_file = "Classifying/" + root + "/literature_info.json"
    try:
        os.makedirs(os.path.dirname(abstract_output_file), exist_ok=True)
        with open(abstract_output_file, 'w', encoding='utf-8') as f:
            json.dump(abstracts_list, f, indent=4)
        print(f"Already saved to {abstract_output_file}")
        
        os.makedirs(os.path.dirname(citation_title_output_file), exist_ok=True)
        with open(citation_title_output_file, 'w', encoding='utf-8') as f:
            json.dump(citation_title_list, f, indent=4)
        print(f"Already saved to {citation_title_output_file}")
        
        os.makedirs(os.path.dirname(author_keywords_output_file), exist_ok=True)
        with open(author_keywords_output_file, 'w', encoding='utf-8') as f:
            json.dump(author_keywords_list, f, indent=4)
        print(f"Already saved to {author_keywords_output_file}")
        
        os.makedirs(os.path.dirname(literature_info_output_file), exist_ok=True)
        with open(literature_info_output_file, 'w', encoding='utf-8') as f:
            json.dump(lit_info_list, f, indent=4)
        print(f"Already saved to {literature_info_output_file}")
    except Exception as e:
        print(f"Error saving to file: {e}")