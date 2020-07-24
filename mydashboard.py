from flask import Flask, render_template
import locale
import datetime
import glob
import json

app = Flask(__name__)

def convert_info_from_locale(input):
    return locale.format_string('%d', input)

def convert_currency_from_locale(input):
    return locale.currency(input, international=True)

def get_data_from_api():
    global info_dict
    global currency_dict
    global last_updated_time

    info = {"message": 22450, "view": 578902, "share": 442, "user": 1824}
    currency = {"germany": 32.7, "united_kingdom": 16.5, "russia": 14.3, "spain": 10.8, "india": 7.6, "france": 4.9}

    info_dict = {k: convert_info_from_locale(v) for k, v in info.items()}
    currency_dict = {k: convert_currency_from_locale(v) for k, v in currency.items()}

    last_updated_time = datetime.datetime.now().strftime(date_format)


@app.route('/dashboard/<language>')
def dashboard(language):
    if(language not in language_dict):
        language = app_language

    return render_template('index.html', **language_dict[language], info = info_dict, currency = currency_dict, update_time = last_updated_time)

if __name__ == '__main__':
    app_language = 'en_SG'
    locale.setlocale(locale.LC_ALL, app_language)

    language_dict = {}
    info_dict = {}
    currency_dict = {}
    date_format = "%d %b %Y %H:%M:%S %Z"
    last_updated_time = ""

    language_list = glob.glob("language/*.json")
    for lang in language_list:
        filename = lang.split('\\')
        lang_code = filename[1].split('.')[0]

        with open(lang, 'r', encoding='utf8') as f:
            json_string = "".join(f.readlines())
            language_dict[lang_code] = json.loads(json_string)

    get_data_from_api()
    app.run('0.0.0.0', port=5000)
