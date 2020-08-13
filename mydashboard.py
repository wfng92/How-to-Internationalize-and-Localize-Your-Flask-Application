from flask import Flask, render_template
import locale
import datetime
import glob
import json

app = Flask(__name__)

def get_stats(input):
    return locale.format_string('%d', input)

def get_currencies(input):
    return locale.currency(input, international=True)

def fetch_data():
    global stats
    global currencies
    global last_updated_time

    stat = {"message": 22450, "view": 578902, "share": 442, "user": 1824}
    currency = {"germany": 32.7, "united_kingdom": 16.5, "russia": 14.3, "spain": 10.8, "india": 7.6, "france": 4.9}

    stats = {k: get_stats(v) for k, v in stat.items()}
    currencies = {k: get_currencies(v) for k, v in currency.items()}

    last_updated_time = datetime.datetime.now().strftime(date_format)


@app.route('/dashboard/<language>')
def dashboard(language):
    if(language not in languages):
        language = app_language

    return render_template('index.html', **languages[language], stats = stats, currencies = currencies, update_time = last_updated_time)

if __name__ == '__main__':
    app_language = 'en_SG'
    locale.setlocale(locale.LC_ALL, app_language)

    languages = {}
    stats = {}
    currencies = {}
    date_format = "%d %b %Y %H:%M:%S %Z"
    last_updated_time = ""

    language_list = glob.glob("language/*.json")
    for lang in language_list:
        filename = lang.split('\\')
        lang_code = filename[1].split('.')[0]

        with open(lang, 'r', encoding='utf8') as file:
            languages[lang_code] = json.loads(file.read())

    fetch_data()
    app.run('0.0.0.0', port=5000)
