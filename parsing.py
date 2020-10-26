import random
import json
from tqdm import tqdm
from parser_class  import *
from collections import OrderedDict

def preprocessing():
    all_data_num = 0
    input_data_num = 0
    data_dict = OrderedDict()
    data_example = []

    with open('articles_with_url.json') as JF:
        json_data = json.load(JF)
        news_list = list(json_data.keys())
        
        for news_date in news_list:
            news_paper = json_data[news_date]
            json_data_list = []
            
            for idx in range(len(news_paper)):
                temp_dict = {}
                all_data_num += 1
                
                self_class = MakeParser(news_paper[idx]['_companyId'])
                if self_class == None or self_class == '--': continue

                article_class = self_class()
                new_src, new_tgt = article_class.parsing(news_paper[idx]['_extcontent'], news_paper[idx]['_text'])
                    
                if new_src == None : continue
                
                data_example.append([new_src, new_tgt, news_paper[idx]['_companyId']])
                
                temp_dict['_id'] = news_paper[idx]['_id']
                temp_dict['_debug'] = news_paper[idx]['_debug']
                temp_dict['_companyId'] = news_paper[idx]['_companyId']
                temp_dict['_extcontent'] = new_src
                temp_dict['_text'] = new_tgt
                temp_dict['_originalUrl'] = news_paper[idx]['_originalUrl']
                json_data_list.append(temp_dict)
                input_data_num += 1

            data_dict[news_date] = json_data_list

    print(f"All data : {all_data_num}")
    print(f"PreprocessingData.json : {input_data_num}")
    return data_dict, data_example


if __name__ == '__main__':
    data, data_example = preprocessing()
    num = 0

    with open('PreprocessingData.json', 'w', encoding="utf-8") as make_file:
        json.dump(data, make_file, ensure_ascii=False)
    with open('PreprocessingExample.txt', 'w', encoding='utf-8') as f:
        da = random.sample(data_example, 100)
        for i in range(len(da)) : 
        
            f.write(da[i][2])
            f.write("\nSource\n")
            f.write(da[i][0])
            f.write("\nTarget\n")
            f.write(da[i][1])
            f.write("\n---------------------------------------\n")
    



