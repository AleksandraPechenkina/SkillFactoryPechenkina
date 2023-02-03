import requests
import json
from config import currency

class ConvertionException(Exception):
    pass

class Schitalka:
    @staticmethod
    def get_price(quote, base, amount):

        if quote == base:
            raise ConvertionException('Нельзя перевести валюту саму в себя.')

        if quote not in currency.keys():
            raise ConvertionException(f'Какая-то валюта не обнаружена.\nУвидеть список всех доступных валют можно по команде /values. Вводить нужно маленькими буквами.')

        if base not in currency.keys():
            raise ConvertionException(f'Какая-то валюта не обнаружена.\nУвидеть список всех доступных валют можно по команде /values. Вводить нужно маленькими буквами.')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException('Нужно написать число!')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={currency[quote]}&tsyms={currency[base]}')
        total_base = json.loads(r.content)[currency[base]]*amount

        return total_base