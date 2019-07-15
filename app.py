from flask import Flask
import requests
from flask_ask import Ask, statement, question
import unidecode
app = Flask(__name__)

ask = Ask(app, '/alexa')

def get_horoscope():
    pass

@app.route('/')
def home():
    return "Hey im working"

@ask.launch
def start_skill():
    welcome_message = 'Hello Asshole fucker bitch, would you like news or horoscope ?'
    return question(welcome_message)

def fetch_news():
    headlines = []
    url ='https://newsapi.org/v2/everything?q=India&from=2019-06-15&sortBy=publishedAt&apiKey=bc36ea3012a94e8083cbc191495a9aae'
    try:
        response = requests.get(url)
        data = response.json()
        for article in data['articles'][:6]:
            headlines.append(unidecode.unidecode(article['title']))
        headlines = '... '.join(headlines)
        return headlines
    except:
        return None

def fetch_horoscope(sign):
    horoscope = ''
    url = 'http://sandipbgt.com/theastrologer/api/horoscope/{}/today/'.format(sign)
    try:
        response = requests.get(url)
        data = response.json()
        horoscope += 'Your horoscope for today is here...'
        horoscope_text = data['horoscope'][:data['horoscope'].index('(c)')]
        horoscope += '{}'.format(horoscope_text)
        horoscope += '...Your mood seems to be {} today.'.format(data['meta']['mood'])
        return horoscope
    except Exception as E:
        print(E)
        return None

@ask.intent('NewsOrHoroScopeIntent',  mapping={'user_response': 'user_response'})
def horoscope(user_response):
    if user_response == 'news':
        news = fetch_news()
        if not news:
            message = 'Sorry! There was a problem fetching news for you'
            return statement(message)
        message = 'Trending headlines are {}'.format(news)
        return statement(message)
    
    elif user_response == 'horoscope':
        message = 'What is your zodiac sign ?'
        return question(message)
    else:
        message = 'Sorry ! I didn\'t understand what the fuck you are talking.'
        return statement(message)
@ask.intent('HoroscopeIntent', mapping={'sign': 'sunsign'})
def tell_horoscope(sign):
    sign = sign.lower()
    signs = [
                "aries",
                "taurus",
                "gemini",
                "cancer",
                "leo",
                "virgo",
                "libra",
                "scorpio",
                "sagittarius",
                "capricorn",
                "aquarius",
                "pisces"
            ]
    if sign not in signs:
        message = 'Sorry! thats an invalid zodiac sign'
        return statement(message)
    horoscope = fetch_horoscope(sign)
    if not horoscope:
        return statement('Sorry! There was a problem fetching your horoscope')
    return statement(horoscope)
if __name__=='__main__':
    app.run(port=5000, host='0.0.0.0', debug=True)