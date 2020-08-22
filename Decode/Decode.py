from fontTools.ttLib import TTFont
import re
import glob
import wget
import pandas as pd
import ast
import time


def start(waiting_decode,add_new=True):
    if add_new:
        import_data(waiting_decode)
    else:
        pass
    save_path = ('/').join(waiting_decode.split("/")[:-1])+'/1-decode.csv'
    df = pd.read_csv(waiting_decode)
    sub_un = df.fillna('0')
    sub_un = sub_un[sub_un.font=='0']
    subset = df.dropna()
    subset = subset.drop_duplicates(subset=['font'])
    columns = ['name', 'base_money', 'real_money', 'starting_date', 'business_statue', 'social_code', 'regist_code',
               'tax_code', 'orgnization_code', 'company_type',
               'industry', 'time', 'reg_orgnization', 'run_time', 'tax', 'employee', 'insurance', 'old_name',
               'eng_name', 'adress', 'business', 'list_name', 'comp_name']
    new_result = pd.DataFrame(columns=columns)
    tnum = 0
    for i, r in subset.iterrows():
        font = r['font']
        new_df = df[df.font == font]
        address = r['font'].split('/')[-3:-1]
        file_name = address[1]
        partial_path = 'Where the defonts should be saved/'
        de_fond = partial_path + file_name + '.txt'
        file = open(de_fond, "r")
        contents = file.read()
        dictionary = ast.literal_eval(contents)

        for ind, row in new_df.iterrows():
            try:
                date = row['time']
                de_date = start_decode(date, dictionary)
                new_df.at[ind, 'time'] = de_date
            except:
                new_df.at[ind, 'time'] = 'error'
        new_df = new_df[columns]
        num = len(new_df.index)
        tnum = tnum + num
        new_result = new_result.append(new_df)
    new_result = new_result.append(sub_un,ignore_index=True)
    print(save_path)
    new_result.to_csv(save_path)
    print('decode finish')


def start_decode(date, dictionary):
    new_date = ''
    dictionary['-'] = '-'
    for i in date:
        if i in dictionary.keys():
            new_date = new_date+dictionary[i]
        else:
            new_date = new_date +i
    return new_date


def import_data(path):
    df = pd.read_csv(path)
    df=df.drop_duplicates(subset=['font'])
    df = check_duplicate(df)
    print(len(df.index))
    for i,r in df.iterrows():
        if type(r['font']) != float:

            address = r['font'].split('/')[-3:-1]

            partial = 'https://static.tianyancha.com/fonts-styles/fonts/'
            new_add = ('/').join(address)
            file_nameadd = '/tyc-num.ttf'

            file_name = address[1]
            partial_path = 'Where the fond be saved/'
            file_save = partial_path + file_name + '.ttf'
            full_path = partial+new_add+file_nameadd
            download_data(full_path, file_save)


def check_duplicate(df):
    exist_files = glob.glob('/Users/xinyue/PycharmProjects/web_scraping/font/*.ttf')
    exist_list = []
    drop_list = []
    df = df.dropna()
    for i in exist_files:
        filename = i.split('/')[-1]
        filename = filename.split('.')[0]
        exist_list.append(filename)
    for ind,r in df.iterrows():
        address = r['font'].split('/')[-3:-1]
        file_name = address[1]
        if file_name in exist_list:
            drop_list.append(ind)
    df=df.drop(drop_list)
    return df



def download_data(link,file):
    wget.download(link, file)
    time.sleep(2)
    de_font(file)


def de_font(file):
    simple_decode(file)



def simple_decode(font_file):
    font = TTFont(font_file)
    save_add = font_file.split('/')[-1]
    save_add = save_add.split('.')[0]
    path = '/Users/xinyue/PycharmProjects/web_scraping/de_font/' + save_add + '.xml'
    font.saveXML(path)  # 保存为tyc-num.xml
    with open(path, 'r') as f:
        xml = f.read()  # 读取tyc-num.xml赋值给xml
    GlyphID = re.findall(r'<GlyphID id="(.*?)" name="(\d+)"/>', xml)
    DigitalDicts = {str(i): str(i - 2) for i in range(2, 12)}
    GlyphIDDicts = {str(Gname): DigitalDicts[Gid] for Gid, Gname in GlyphID}
    key_list = []
    print(GlyphIDDicts)
    for k in GlyphIDDicts.keys():
        key_list.append(k)
    key_list2 = key_list.copy()
    key_list.sort()
    new_dic = {}
    for i in range(len(key_list)):
        new_dic[key_list2[i]] = key_list[i]
    save_dic = '/Users/xinyue/PycharmProjects/web_scraping/de_font/' + save_add + '.txt'
    f = open(save_dic, "w")
    f.write(str(new_dic))
    f.close()




waiting_decode = 'Where is the originsl csv file.csv'
start(waiting_decode,add_new=True)