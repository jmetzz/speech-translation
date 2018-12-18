import requests
import os


class Translator:
    @classmethod
    def handle(cls, text):
        print(" --------" + text)
        source_lang = 'NL'
        target_lang = 'FR'
        split_sentences = '0'
        url = 'https://api.deepl.com/v2/translate'
        headers = {'content_type': 'application/x-www-form-urlencoded',
                   'content_length': str(len(text))}

        body = {
            'auth_key': os.getenv('DEEPL_API_KEY'),
            'text': text,
            'source_lang': source_lang,
            'target_lang': target_lang,
            'split_sentences': split_sentences
        }

        response = requests.post(url, data=body, headers=headers)
        return response.text
