import logging

import requests
import json


class DeepLTranslationService:
    languages = {
        'en-US': 'EN',
        'en-GB': 'EN',
        'fr-FR': 'FR',
        'pt-BR': 'PT',
        'pt-PT': 'PT',
        'es-ES': 'ES',
        'de-DE': 'DE',
        'nl-NL': 'NL'
    }

    def __init__(self, source_lang, target_lang, auth_key):
        self.source_lang = DeepLTranslationService.languages[source_lang]
        self.target_lang = DeepLTranslationService.languages[target_lang]
        self._auth_key = auth_key
        self.logger = logging.getLogger(self.__class__.__name__)

    def handle(self, text):
        split_sentences = '0'
        url = 'https://api.deepl.com/v2/translate'
        headers = {'content_type': 'application/x-www-form-urlencoded',
                   'content_length': str(len(text))}

        body = {
            'auth_key': self._auth_key,
            'text': text,
            'source_lang': self.source_lang,
            'target_lang': self.target_lang,
            'split_sentences': split_sentences
        }

        response = requests.post(url, data=body, headers=headers)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            self.logger.error(f"Could not translate sentence. "
                              f"Response from server: {response}")
            return {
                'translations': [
                    {'text': 'Translation not available. Check the logs',
                     'error': True}
                ]}
