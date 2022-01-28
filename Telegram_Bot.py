import re
import os
import googleapiclient.discovery
import json
import telebot #pyTelegramBotApi
import string
import requests
import pandas as pd
import keras
from datetime import datetime


#Create DartaFrame for manipulation later
# df=pd.read_csv('csv_path')
#key_words=df.columns.tolist()[-300:]
#Which words model will detect also it is last 300 loumns in primary DF
key_words=['love', 'like', 'god', 'one', 'lok', 'get', 'make', 'people', 'know', 'song', 'realy', 'time', 'much', 'want', 'guy', 'think', 'please', 'great', 'thank', 'thing', 'ben', 'lol', 'amazing', 'got', 'way', 'new', 'watch', 'even', 'best', 'say', 'video', 'day', 'n', 'movie', 'stil', 'fel', 'never', 'back', 'year', 'going', 'beter', 'come', 'beautiful', 'wel', 'life', 'man', 'show', 'omg', 'first', 'made', 'music', 'right', 'shit', 'work', 'fuck', 'thought', 'take', 'girl', 'kep', 'chanel', 'watching', 'real', 'fucking', 'wait', 'actualy', 'awesome', 'use', 'trending', 'wow', 'sound', 'world', 'give', 'many', 'litle', 'said', 'lot', 'nice', 'bad', 'hope', 'live', 'put', 'let', 'try', 'start', 'stop', 'end', 'help', 'funy', 'game', 'ye', 'cal', 'youtube', 'hapy', 'prety', 'black', 'col', 'mean', 'old', 'voice', 'next', 'last', 'cute', 'gona', 'lov', 'coment', 'hair', 'hapen', 'makeup', 'white', 'two', 'part', 'name', 'tel', 'fan', 'play', 'damn', 'friend', 'find', 'face', 'long', 'big', 'wish', 'sem', 'making', 'done', 'geting', 'sen', 'hate', 'job', 'kid', 'person', 'favorite', 'sure', 'hard', 'money', 'eye', 'us', 'talk', 'iphone', 'soap', 'bok', 'diferent', 'phone', 'saw', 'trying', 'maybe', 'wrong', 'ned', 'point', 'around', 'nothing', 'stuf', 'loking', 'whole', 'son', 'kil', 'baby', 'kind', 'perfect', 'buy', 'what', 'family', 'idea', 'eat', 'fod', 'view', 'care', 'word', 'saying', 'away', 'hear', 'review', 'learn', 'fun', 'dude', 'believe', 'literaly', 'theyre', 'bit', 'schol', 'sory', 'house', 'hel', 'place', 'hand', 'came', 'fre', 'vid', 'wek', 'probably', 'check', 'second', 'remember', 'sad', 'found', 'film', 'understand', 'top', 'lmao', 'skin', 'went', 'gun', 'yeah', 'heart', 'super', 'cat', 'wana', 'milion', 'boy', 'turn', 'question', 'true', 'yet', 'reason', 'story', 'enough', 'absolutely', 'que', 'talking', 'trailer', 'cake', 'might', 'heard', 'listen', 'coming', 'cause', 'american', 'jesu', 'problem', 'hot', 'together', 'night', 'light', 'ask', 'dog', 'enjoy', 'hit', 'almost', 'episode', 'laugh', 'far', 'aple', 'change', 'definitely', 'today', 'read', 'album', 'sub', 'mi', 'high', 'human', 'die', 'month', 'home', 'haha', 'water', 'left', 'fact', 'using', 'dead', 'must', 'wonder', 'country', 'remind', 'ago', 'mind', 'side', 'le', 'wtf', 'vlog', 'glad', 'ful', 'head', 'may', 'woman', 'minute', 'least', 'women', 'knew', 'talent', 'stupid', 'suck', 'excit', 'shot', 'product', 'car', 'weird', 'season', 'joke', 'tho', 'waiting', 'proud', 'original', 'star', 'style', 'gorgeou', 'lost', 'cover', 'type', 'feling']

# We will not use other data from DataFrame so lower memory usage
# df=df[['preferences','video_id']]
#Light CSV ver
df=pd.read_csv('pref_light_300.csv')


#Telegram bot
token = 'telegram_bot_api'
bot = telebot.TeleBot(token)

#YouTube API
api_key='YOUTUBE_API'

#SOTP_WORDS Words outside model.
minus_words=stop_words=['inside','ever','instead','already','theres','anything','thats','always','could','hers', 'only', 'neednt', 'doesnt', 'without', 'have', 'its', 'don', 'ive', 'into', 'before', 'mustn', 'any', 'now', 'such', 'you', 'trump', 'below', 'since', 'which', 'doesn', 'hasn', 'itself', 'all', 'someone', 'couldn', 'some', 'down', 'under', 'her', 'weren', 'once', 'yourselves', 'youd', 'myself', 'didnt', 'thi', 'the', 'dont', 'but', 'their', 'werent', 'yourself', 'over', 'mightnt', 'hes', 'too', 'each', 'yal', 'when', 'that', 'hey', 'everything', 'with', 'out', 'who', 'both', 'few', 'else', 'than', 'mightn', 'own', 'haven', 'everyone', 'then', 'our', 'was', 'themselves', 'isnt', 'gues', 'arent', 'where', 'youll', 'how', 'again', 'hasnt', 'another', 'why', 'more', 'hadnt', 'shant', 'doing', 'having', 'while', 'were', 'youve', 'been', 'she', 'and', 'there', 'needn', 'hadn', 'wasnt', 'against', 'him', 'wont', 'cant', 'these', 'wasn', 'himself', 'theirs', 'same', 'because', 'wouldn', 'your', 'whom', 'until', 'does', 'here', 'video', 'aren', 'just', 'thatll', 'mustnt', 'nor', 'shouldn', 'wouldnt','would', 'will', 'them', 'above', 'his', 'youre', 'couldnt', 'has', 'wil', 'shan', 'isn', 'herself', 'ain', 'anyone', 'this', 'about', 'after', 'shouldve', 'further', 'every', 'from', 'what', 'shes', 'shouldnt', 'during', 'something', 'between', 'other', 'yours', 'though', 'ours', 'had', 'also', 'should', 'for', 'those', 'they', 'not', 'most', 'off', 'through', 'being', 'did', 'didn', 'can', 'ourselves', 'havent', 'won', 'very', 'are']

#Create new DF for stats and new train data
df_new_data=pd.DataFrame(columns=['video_id', 'real_rating','predicted_rating','user_id','user_name','input_data'])

#My error. In case of custom error
class SomeError(Exception):
    def __init__(self, text):
        self.txt = text


#Find code of video in link
#ex.:https://www.youtube.com/watch?v=Ed47sWpgvf0 or https://youtu.be/Bj7q5VAf8-w
def clear_link(link):
    try:
        blanks=['watch.v=(.{11,11})','https://youtu.be/(.{11,11})']
        if 'youtu.be' in link:
            code=(re.findall(blanks[1],link)[0])
        else:
            code = (re.findall(blanks[0], link)[0])
    except :
        raise SomeError('Bad link')
    return code


#Youtube API&. Collecting comments of video
def get_comments(code_video):
    clear_comments=[]
    for i in range(30): #Read first 3k comments, but not fewer than 100

        if i==0: #We do not need next_page tooken for first page
            next_page_token=''
        #request and params
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        api_service_name = "youtube"
        api_version = "v3"
        DEVELOPER_KEY = api_key
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=DEVELOPER_KEY)
        request = youtube.commentThreads().list(
            part="snippet",
            maxResults=100,
            order="relevance",
            pageToken=next_page_token,
            videoId=code_video
        )
        response = request.execute()
        comments = response['items'] #Dict of items

        # Stop search if comments o this page=0
        if len(comments)==0:
            break

        #Find and collect text from comments
        for item in comments:
            clear_comments.append(item['snippet']['topLevelComment']['snippet']['textDisplay'])

        try:  #try to find next page token else break
            next_page_token = response['nextPageToken']
        except :
           break

    # Custom exc in case if not enugh comments
    if len(clear_comments) < 100:
        print(len(clear_comments))
        raise SomeError("Comments less than 100")

    return str(clear_comments[1:]) #Sometimes first comment writed channel owner and I need str for next functions


#Drop duplicaste
#Yes, we have lost duplicates in useful words, but I hope that this will not destroy our model
def remove_duplicates_in_words(word): #Dooooon't tyyyype coooommmmments liiiiike thaaat =>Don't type coments like that
    l = ''
    new_word = ''
    for i in word:
        if i != l:
            new_word += i
        l = i
    return new_word


#Remove s or ed on end of words
def delete_s_ed(word):
    if word[-1:]=='s':
        new_word=word[:-1]
    elif word[-2:]=='ed':
        new_word=word[:-2]
    else:
        new_word=word
    return new_word


#Make list of words from str text. "I like that" =>['i','like','that']
def text_tolist(text): #Only text and text to list of words
    try:
        text = text.lower()
        text=''.join([x for x in text if x in string.ascii_letters + ' '])
    except: #Sometimes no words in comments
        text=" "
    return text.split(" ")


#This function remove useless words and fix useful if it needs
def words_cleaning(words):
    new_words=[]
    for word in words:
        word=remove_duplicates_in_words(word)
        if len(word)<13 and len(word)>=3: # In comments words with length more than 12 are rare and less than 3 are useless
                if word not in stop_words: #Is word in minus(stop) words?
                    new_words.append(delete_s_ed(word))
    return new_words


#Normalize data for our model
def get_input_line(code,key_words=key_words):
    comments=get_comments(code)
    dirty_list_of_words=text_tolist(comments)
    list_of_words=words_cleaning(dirty_list_of_words)
    key_words = key_words #Words like in basic DF
    input_line=[list_of_words.count(i) for i in key_words] #Input line is number of words in comments
    input_line=[i/max(input_line) for i in input_line] #Normalize input_line
    return input_line


#Load model and make predition
model=keras.models.load_model('model_path')
def get_predict(input_line,model=model):
    prediction=model.predict([input_line])
    return round(float(prediction[0][0])*100,2)


#Request to service where we can check real data.So far it is working
def get_real_rating(code):
    link=f'https://returnyoutubedislikeapi.com/votes?videoId={code}'
    resp=requests.get(link).text
    resp=json.loads(resp)
    rating=resp['likes']/(resp['likes']+resp['dislikes'])
    return round(rating*100,2)


#Calculating percent rank of videos using test sample
def get_top(rating,df=df):
    better_than=len(df[df['preferences'] <= rating])/len(df)*100
    return round(better_than,2)


#Current time for naming
def get_current_time():
    now = datetime.now()
    current_time = now.strftime("%d_%m__%H_%M")
    return  current_time


#Saving DataFrame. Name with time stamp
def  df_save(df):
    df_new_data=df
    df_new_data.to_csv(f'new_data_{get_current_time()}.csv', index=False)
    df_new_data.drop(df_new_data.index, inplace=True)
    return df_new_data


#Telegram bot and his functions with decorators

#Comand start
@bot.message_handler(commands=['start'])
def starter(message):

    user=message.from_user.first_name
    #Hello messages
    bot.send_message(message.chat.id, 'Hello, {}\n'
                                      'A tragedy has happened in the world. Youtube removed dislikes. The development of mankind has slowed down more than after the popularization of tiktok.\n'.format(user))
    file_id='CgACAgQAAxkBAAIjGmHqo47Gh76ANTcSCZBQpCVWJnbEAALuAgACWH4sU1Kh7FBsq3vSIwQ'
    bot.send_animation(message.chat.id, file_id)
    bot.send_message(message.chat.id, 'Today, dislikes are still available via the API, but this method will soon be closed. So, I trained a neural network that can predict the rating based on comments (TF/keras).')
    bot.send_message(message.chat.id,
                     'Just send link to the video\nBot can read just eng comments!!!')
    id = str(message.chat.id)
    print(id,user)


#If any text it try to find key data else error
@bot.message_handler(content_types=['text'])
def current_bot(message):
    try:
        print(message.chat.id)
        user = message.from_user.first_name
        id = str(message.chat.id)

        #Find code of video
        code = clear_link(message.text)
        bot.send_message(message.chat.id, 'Link is okay. It needs few seconds')

        #Create normal data from comments
        bot.send_message(message.chat.id, 'Reading comments...')
        input_line = get_input_line(code)

        bot.send_message(message.chat.id, 'Normalizing comments...')
        #Predict rating
        rating = get_predict(input_line)
        bot.send_message(message.chat.id, 'Predicting rating...')

        #Calculating top ranking
        top = get_top(rating/100)
        bot.send_message(message.chat.id, 'Calculating top ranking...')

        # Try to find real rating
        try:
            real = get_real_rating(code)
        except:
            real = "Can't find real rating"
        bot.send_message(message.chat.id, 'Cheking real rating...')


        text=f"""The neural network predicts that the video has {rating}% likes \nThis is more than {top}% of the test sample videos\nActual rating {real}% likes (so far available)"""

        if rating<=85:
            print('rating is low ')
            bot.send_message(message.chat.id, "Rating below 85%. So it will not be accurate, so far there are few videos in the training dataset with such ratings. But anyway it is bad video")

        print(code,rating,real, user, id)
        bot.send_message(message.chat.id, text)

        #Save data for analysis and additional trainig
        data_for_df =[code,real,rating,id,user,tuple(input_line)]
        df_new_data.loc[len(df_new_data)] = data_for_df
        df_new_data.drop_duplicates()
        if len(df_new_data)==100: #
            df_save(df_new_data)
            #Restart loop by error for saving DF
            raise SomeError('Data Saved')

    #Errors to message
    except Exception as ex:
        #Send error text as message
        bot.send_message(message.chat.id,ex)
        print(ex,message.from_user.first_name)

#Activation of telegram bot
bot.polling(none_stop=True)


