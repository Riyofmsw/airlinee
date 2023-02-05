import re
import string
from string import digits
def clean_tweets(text):
    remove_digits = str.maketrans('','', digits)
    text =text.translate(remove_digits)
    text=text.translate(str.maketrans('', '', string.punctuation))#removing all ponctuations
    text = re.sub("@[_A-Za-z0-9]+","",text) #Removing mention
    text=re.sub("[^\w\s#@/:%.,_-]", "", text, flags=re.UNICODE)#REmove emoji
    text=re.sub(r'\s*[A-Za-z]+\b', '' , text)#remove no arabic word
    text=re.sub(r'#','',text)# removing hachtag
    text=re.sub(r'https?:\/\/\s+','',text)#remove the hyper link
    text = re.sub("\n"," ",text)
    text=re.sub(r'^[A-Za-z0-9.!?:؟]+'," ",text) ##Removing digits and punctuations
    text = re.sub("\n"," ",text)
    text = re.sub(u'\xa0','',text)
    text = re.sub(r'[\u064B\u064C\u064D\u064E\u064F\u0650\u0651\u0652]','',text)
    #text = re.sub("[إأٱآا]", "ا", text)
    text = re.sub("[ااا]+","ا",text)
    #text = re.sub("[ي","+[يييي",text)
    text = re.sub("[a-zA-Z]+","",text)
    text = re.sub("²", "", text)
    text = re.sub("[0-9]+","",text)

    text = re.sub("[ﷺöüçāīṣııšḥāḫםבםבḥāā]", "",text)
    text = re.sub("[헨리생일축하해요왕자어린]", "",text)
    text = re.sub(r'http', '',text)
    text=re.sub('[٠١٢٣٤٥٦٧٨٩]',"",text)
  
    text = re.sub('öü','',text)
    
    
    return text
arabic_punctuations = '''`https?://[A-Za-z./]*@[\w]*[^a-zA-Z#][a-zA-Z0-9][a-zA-Z0-9]|[:;]-?؟،؛[()ODp][A-Z][a-z]+|\d+|[A-Z]+(?![a-z])^w^{<>_()*&^%][^`^l/:"^=.,'{}~+|!^`^}^`^`^|^`^s^`'''
english_punctuations = string.punctuation
latin_alphabic =  '''abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'''
num = '''0123456789'''
punctuations_list = arabic_punctuations + english_punctuations + latin_alphabic + num

arabic_diacritics = re.compile("""
                             ّ    | # Tashdid
                             َ    | # Fatha
                             ً    | # Tanwin Fath
                             ُ    | # Damma
                             ٌ    | # Tanwin Damm
                             ِ    | # Kasra
                             ٍ    | # Tanwin Kasr
                             ْ    | # Sukun
                             ـ     # Tatwil/Kashida
                         """, re.VERBOSE)

def normalize_arabic(text):
    text = re.sub("[إأآا]", "ا", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("ؤ", "ء", text)
    text = re.sub("ئ", "ء", text)
    text = re.sub("ة", "ه", text)
    text = re.sub("گ", "ك", text)
    return text

def remove_diacritics(text):
    text = re.sub(arabic_diacritics, '', text)
    return text

def remove_symbols_from_text(text):
  symbols = '!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~https?://[A-Za-z./]*@[\w]*[^a-zA-Z#][a-zA-Z0-9][a-zA-Z0-9]|[:;]-?[()ODp][A-Z][a-z]+|\d+|[A-Z]+(?![a-z])'
  for symbol in symbols:
    text = text.replace(symbol, '')
  return text

def remove_punctuations(text):
    translator = str.maketrans('', '', punctuations_list)
    return text.translate(translator)


def remove_repeating_char(text):
    return re.sub(r'(.)\1+', r'\1', text)

def remove_emoji(string):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)

def clean_text(text):
    text=remove_symbols_from_text(text)
    text=remove_punctuations(text)
    text=remove_repeating_char(text)
    text=remove_emoji(text)
    text=remove_diacritics(text)
    text=normalize_arabic(text)
    return text