import typing as t
from abc import ABC, abstractmethod

import requests


from ..enums import Resolution


__all__ = [
    'BaseClient',
    'AbstractClient'
]


class BaseClient:
    API_URL = 'https://api.wallex.ir'
    PUBLIC_API_VERSION = 'v1'

    REQUEST_TIMEOUT: float = 10

    SIDE_BUY = 'BUY'
    SIDE_SELL = 'SELL'

    ORDER_TYPE_LIMIT = 'LIMIT'
    ORDER_TYPE_MARKET = 'MARKET'
    ORDER_TYPE_STOP_LOSS = 'STOP_LOSS'
    ORDER_TYPE_STOP_LOSS_LIMIT = 'STOP_LOSS_LIMIT'
    ORDER_TYPE_TAKE_PROFIT = 'TAKE_PROFIT'
    ORDER_TYPE_TAKE_PROFIT_LIMIT = 'TAKE_PROFIT_LIMIT'
    ORDER_TYPE_LIMIT_MAKER = 'LIMIT_MAKER'

    def __init__(
            self, api_key: t.Optional[str] = None, requests_params: t.Optional[t.Dict[str, str]] = None,
    ):
        self.API_KEY = api_key

        self._requests_params = requests_params
        self.session = self._init_session()

    @staticmethod
    def _get_kwargs(locals_: t.Dict, del_keys: t.List[str] = None, del_nones: bool = False) -> t.Dict:
        _del_keys = ['self', 'cls']
        if del_keys is not None:
            _del_keys.extend(del_keys)

        if del_nones is True:
            return {key: value for key, value in locals_.items() if (key not in _del_keys) and (value is not None)}

        return {key: value for key, value in locals_.items() if key not in _del_keys}

    @staticmethod
    def _get_headers() -> t.Dict:
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        return headers

    def _init_session(self):
        raise NotImplementedError

    def _create_api_uri(self, path: str, version: str = PUBLIC_API_VERSION) -> str:
        return self.API_URL + '/' + version + '/' + path

    def _get_request_kwargs(self, method, signed: bool, **kwargs) -> t.Dict:
        # set default requests timeout
        kwargs['timeout'] = self.REQUEST_TIMEOUT

        # add our global requests params
        if self._requests_params:
            kwargs.update(self._requests_params)

        data = kwargs.get('data', None)
        if data and isinstance(data, dict):
            kwargs['data'] = data

            # find any requests params passed and apply them
            if 'requests_params' in kwargs['data']:
                # merge requests params into kwargs
                kwargs.update(kwargs['data']['requests_params'])
                del (kwargs['data']['requests_params'])

        if signed is True:
            headers = kwargs.get('headers', {})
            headers.update({'x-api-key': self.API_KEY})
            kwargs['headers'] = headers

        # if get request assign data array to params value for requests lib
        if data and method == 'get':
            kwargs['params'] = '&'.join('%s=%s' % (data[0], data[1]) for data in kwargs['data'])
            del (kwargs['data'])

        return kwargs

    @staticmethod
    def _pick(result: t.Union[t.Dict, t.List], key: str, value: str = None) -> t.Union[t.Dict, t.List]:
        result = result.copy()
        if isinstance(result, dict):
            symbol_data = result.get(key)
            result.clear()
            result[key] = symbol_data

            return result
        if isinstance(result, list):
            assert value is not None, "value is required for list"
            # print(f"Looking for {key=} with {value=} in {result}")
            result_ = [item for item in result if item[key] == value]

            return result_


class AbstractClient(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def _init_session(self) -> requests.Session:
        raise NotImplementedError('_init_session not implemented')

    @abstractmethod
    def _request(self, method, uri: str, signed: bool, **kwargs):
        raise NotImplementedError('_request not implemented')

    @staticmethod
    @abstractmethod
    def _handle_response(response: requests.Response):
        raise NotImplementedError('_handle_response not implemented')

    @abstractmethod
    def _request_api(
            self, method, path: str, signed: bool = False, version=BaseClient.PUBLIC_API_VERSION, **kwargs
    ):
        raise NotImplementedError('_request_api not implemented')

    @abstractmethod
    def _get(self, path, signed=False, version=BaseClient.PUBLIC_API_VERSION, **kwargs) -> t.Dict:
        raise NotImplementedError('_get not implemented')

    @abstractmethod
    def _post(self, path, signed=False, version=BaseClient.PUBLIC_API_VERSION, **kwargs) -> t.Dict:
        raise NotImplementedError('_post not implemented')

    @abstractmethod
    def _put(self, path, signed=False, version=BaseClient.PUBLIC_API_VERSION, **kwargs) -> t.Dict:
        raise NotImplementedError('_put not implemented')

    @abstractmethod
    def _delete(self, path, signed=False, version=BaseClient.PUBLIC_API_VERSION, **kwargs) -> t.Dict:
        raise NotImplementedError('_delete not implemented')

    @abstractmethod
    def get_market_stats(self, symbol: str = None) -> t.Dict:
        raise NotImplementedError('get_market_stats not implemented')

    @abstractmethod
    def get_currencies(self, currency: str = None) -> t.Dict:
        raise NotImplementedError('get_currencies not implemented')

    @abstractmethod
    def get_currencies_stats(self, currency=None) -> t.Dict:
        raise NotImplementedError('get_currencies_stats not implemented')

    @abstractmethod
    def get_orderbook(self, symbol: str) -> t.Dict:
        raise NotImplementedError('get_orderbook not implemented')

    @abstractmethod
    def get_recent_trades(self, symbol: str = 'None', **kwargs) -> t.Dict:
        raise NotImplementedError('get_recent_trades not implemented')

    @abstractmethod
    def get_ohlc_data(
            self, symbol: str = None, resolution: Resolution = None, from_date: int = None, to_date: int = None
    ) -> t.Dict:
        raise NotImplementedError('get_ohlc_data not implemented')

    @abstractmethod
    def get_profile(self) -> t.Dict:
        raise NotImplementedError('get_profile not implemented')

    @abstractmethod
    def get_cards(self) -> t.Dict:
        raise NotImplementedError('get_cards not implemented')

    @abstractmethod
    def add_card(self, card_number: str) -> t.Dict:
        raise NotImplementedError('add_card not implemented')

    @abstractmethod
    def delete_card(self, card_number: str) -> t.Dict:
        raise NotImplementedError('delete_card not implemented')

    @abstractmethod
    def get_ibans(self) -> t.Dict:
        raise NotImplementedError('get_ibans not implemented')

    @abstractmethod
    def add_iban(self, iban: str) -> t.Dict:
        raise NotImplementedError('add_iban not implemented')

    @abstractmethod
    def delete_iban(self, iban: str) -> t.Dict:
        raise NotImplementedError('delete_iban not implemented')

    @abstractmethod
    def get_wallets(self, asset: str) -> t.Dict:
        raise NotImplementedError('get_wallets not implemented')

    @abstractmethod
    def get_balances(self, asset: str = None) -> t.Dict:
        raise NotImplementedError('get_balances not implemented')

    @abstractmethod
    def get_available_balance(self, asset: str) -> float:
        raise NotImplementedError('get_available_balance not implemented')

    @abstractmethod
    def get_fees(self, symbol: str = None) -> t.Dict:
        raise NotImplementedError('get_fees not implemented')

    @abstractmethod
    def create_order(
            self, symbol: str, side: str, type: str, quantity: float, price: float = None, client_id: str = None
    ) -> t.Dict:
        raise NotImplementedError('create_order not implemented')

    @abstractmethod
    def order_market(self, symbol: str, side: str, quantity: float, client_id: str = None) -> t.Dict:
        raise NotImplementedError('order_market not implemented')

    @abstractmethod
    def order_limit(self, symbol: str, side: str, quantity: float, price: float, client_id: str = None) -> t.Dict:
        raise NotImplementedError('order_limit not implemented')

    @abstractmethod
    def order_market_buy(self, symbol: str, quantity: float, client_id: str = None) -> t.Dict:
        raise NotImplementedError('order_market_buy not implemented')

    @abstractmethod
    def order_market_sell(self, symbol: str, quantity: float, client_id: str = None) -> t.Dict:
        raise NotImplementedError('order_market_sell not implemented')

    @abstractmethod
    def order_limit_buy(self, symbol: str, quantity: float, price: float, client_id: str = None) -> t.Dict:
        raise NotImplementedError('order_limit_buy not implemented')

    @abstractmethod
    def order_limit_sell(self, symbol: str, quantity: float, price: float, client_id: str = None) -> t.Dict:
        raise NotImplementedError('order_limit_sell not implemented')

    @abstractmethod
    def cancel_order(self, order_id: str) -> t.Dict:
        raise NotImplementedError('cancel_order not implemented')

    @abstractmethod
    def get_open_orders(self, symbol: str = None, side: str = None) -> t.Dict:
        raise NotImplementedError('get_open_orders not implemented')

    @abstractmethod
    def get_user_recent_trades(self, symbol: str = None, side: str = None, active: bool = None) -> t.Dict:
        raise NotImplementedError('get_user_recent_trades not implemented')

    @abstractmethod
    def get_order_status(self, order_id: str) -> t.Dict:
        raise NotImplementedError('get_order_status not implemented')

    @abstractmethod
    def withdraw(
            self, coin: str, network: str, amount: float,
            address: str, client_unique_id: str, memo: t.Optional[str] = None
    ) -> t.Dict:
        raise NotImplementedError('withdraw not implemented')

    @abstractmethod
    def close_connection(self):
        raise NotImplementedError('close_connection not implemented')
