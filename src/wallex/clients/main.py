import typing as t
import requests
import aiohttp
import asyncio

from ..enums import Resolution
from .base import BaseClient, AbstractClient
from ..exceptions import RequestException, APIException


__all__ = [
    'Client',
    'AsyncClient'
]


class Client(BaseClient, AbstractClient):
    def __init__(
            self, api_key: t.Optional[str] = None, requests_params: t.Optional[t.Dict[str, t.Any]] = None,
    ):

        super().__init__(api_key, requests_params)

    def _init_session(self) -> requests.Session:

        headers = self._get_headers()

        session = requests.session()
        session.headers.update(headers)
        return session

    def _request(self, method, uri: str, signed: bool, **kwargs):

        kwargs = self._get_request_kwargs(method, signed, **kwargs)

        self.response = getattr(self.session, method)(uri, **kwargs)
        return self._handle_response(self.response)

    @staticmethod
    def _handle_response(response: requests.Response):
        if not (200 <= response.status_code < 300):
            raise APIException(response, response.status_code, response.text)
        try:
            return response.json()
        except ValueError:
            raise RequestException('Invalid Response: %s' % response.text)

    def _request_api(
            self, method, path: str, signed: bool = False, version=BaseClient.PUBLIC_API_VERSION, **kwargs
    ):
        uri = self._create_api_uri(path, version)
        return self._request(method, uri, signed, **kwargs)

    def _get(self, path, signed=False, version=BaseClient.PUBLIC_API_VERSION, **kwargs) -> t.Dict:
        return self._request_api('get', path, signed, version, **kwargs)

    def _post(self, path, signed=False, version=BaseClient.PUBLIC_API_VERSION, **kwargs) -> t.Dict:
        return self._request_api('post', path, signed, version, **kwargs)

    def _put(self, path, signed=False, version=BaseClient.PUBLIC_API_VERSION, **kwargs) -> t.Dict:
        return self._request_api('put', path, signed, version, **kwargs)

    def _delete(self, path, signed=False, version=BaseClient.PUBLIC_API_VERSION, **kwargs) -> t.Dict:
        return self._request_api('delete', path, signed, version, **kwargs)

    def get_market_stats(self, symbol: str = None) -> t.Dict:
        result = self._get('markets')

        if symbol is not None:
            data = self._pick(result.get('result').get('symbols'), symbol)
            result['result'] = data

        return result

    def get_currencies(self, currency: str = None) -> t.Dict:
        result = self._get('currencies')

        if currency is not None:
            data = self._pick(result.get('result'), currency)
            result['result'] = data

        return result

    def get_currencies_stats(self, currency=None) -> t.Dict:
        result = self._get('currencies/stats')

        if currency is not None:
            data = self._pick(result.get('result'), 'key', currency)
            result['result'] = data

        return result

    def get_orderbook(self, symbol: str) -> t.Dict:
        return self._get('depth', params={'symbol': symbol})

    def get_recent_trades(self, symbol: str = 'None', **kwargs) -> t.Dict:
        return self._get('trades', params={'symbol': symbol}, **kwargs)

    def get_ohlc_data(
            self, symbol: str = None, resolution: Resolution = None, from_date: int = None, to_date: int = None
    ) -> t.Dict:
        return self._get('udf/history', params={
            'symbol': symbol,
            'resolution': resolution.value if resolution is not None else None,
            'from': from_date,
            'to': to_date
        })

    def get_profile(self) -> t.Dict:
        return self._get('account/profile', signed=True)

    def get_cards(self) -> t.Dict:
        return self._get('account/card-numbers', signed=True)

    def add_card(self, card_number: str) -> t.Dict:
        return self._post('account/card-numbers', signed=True, json={'card_number': card_number})

    def delete_card(self, card_number: str) -> t.Dict:
        return self._delete(f'account/card-numbers/{card_number}', signed=True)

    def get_ibans(self) -> t.Dict:
        return self._get('account/ibans', signed=True)

    def add_iban(self, iban: str) -> t.Dict:
        return self._post('account/ibans', signed=True, json={'iban': iban})

    def delete_iban(self, iban: str) -> t.Dict:
        return self._delete(f'account/ibans/{iban}', signed=True)

    def get_wallets(self, asset: str) -> t.Dict:
        return self._get(f'account/wallets/{asset}', signed=True)

    def get_balances(self, asset: str = None) -> t.Dict:
        result = self._get(f'account/balances', signed=True)

        if asset is not None:
            data = self._pick(result.get('result').get('balances'), asset)
            result['result']['balances'] = data

        return result

    def get_available_balance(self, asset: str) -> float:
        result = self.get_balances(asset)
        result = result.get('result').get('balances').get(asset.upper())
        return float(result.get('value')) - float(result.get('locked'))

    def get_fees(self, symbol: str = None) -> t.Dict:
        result = self._get('account/fee', signed=True)

        if symbol is not None:
            data = self._pick(result.get('result'), symbol)
            result['result'] = data

        return result

    def create_order(
            self, symbol: str, side: str, type: str, quantity: float, price: float = None, client_id: str = None
    ) -> t.Dict:
        return self._post('account/orders', signed=True, json=self._get_kwargs(locals(), del_nones=True))

    def order_market(self, symbol: str, side: str, quantity: float, client_id: str = None) -> t.Dict:
        return self.create_order(symbol, side, self.ORDER_TYPE_MARKET, quantity, client_id)

    def order_limit(self, symbol: str, side: str, quantity: float, price: float, client_id: str = None) -> t.Dict:
        return self.create_order(symbol, side, self.ORDER_TYPE_LIMIT, quantity, client_id)

    def order_market_buy(self, symbol: str, quantity: float, client_id: str = None) -> t.Dict:
        return self.order_market(symbol, self.SIDE_BUY, quantity, client_id)

    def order_market_sell(self, symbol: str, quantity: float, client_id: str = None) -> t.Dict:
        return self.order_market(symbol, self.SIDE_SELL, quantity, client_id)

    def order_limit_buy(self, symbol: str, quantity: float, price: float, client_id: str = None) -> t.Dict:
        return self.order_limit(symbol, self.SIDE_BUY, quantity, price, client_id)

    def order_limit_sell(self, symbol: str, quantity: float, price: float, client_id: str = None) -> t.Dict:
        return self.order_limit(symbol, self.SIDE_SELL, quantity, price, client_id)

    def cancel_order(self, order_id: str) -> t.Dict:
        return self._delete(f'account/orders', signed=True, json={'clientOrderId': order_id})

    def get_open_orders(self, symbol: str = None, side: str = None) -> t.Dict:
        result = self._get('account/openOrders', signed=True)

        if symbol is not None:
            data = self._pick(result.get('result').get('orders'), "symbol", symbol)
            result['result'] = data

        if side is not None:
            data = self._pick(result.get('result').get('orders'), "side", side)
            result['result'] = data

        return result

    def get_user_recent_trades(self, symbol: str = None, side: str = None, active: bool = None) -> t.Dict:
        return self._get('account/trades', signed=True, params={
            'symbol': symbol,
            'side': side,
            'active': active
        })

    def get_order_status(self, order_id: str) -> t.Dict:
        return self._get(f'account/orders/{order_id}', signed=True)

    def withdraw(
            self, coin: str, network: str, amount: float,
            address: str, client_unique_id: str, memo: t.Optional[str] = None
    ) -> t.Dict:
        return self._post('account/crypto-withdrawal', signed=True, json=self._get_kwargs(locals(), del_nones=True))

    def close_connection(self):
        if self.session:
            self.session.close()

    def __del__(self):
        self.close_connection()


class AsyncClient(BaseClient, AbstractClient):
    def __init__(
            self,
            api_key: t.Optional[str] = None,
            requests_params: t.Optional[t.Dict[str, t.Any]] = None,
            loop: t.Optional[asyncio.AbstractEventLoop] = None
    ):

        self.loop = loop or asyncio.get_event_loop()
        super().__init__(api_key, requests_params)

    @classmethod
    async def create(
            cls,
            api_key: t.Optional[str] = None,
            requests_params: t.Optional[t.Dict[str, t.Any]] = None,
            loop: t.Optional[asyncio.AbstractEventLoop] = None
    ) -> 'AsyncClient':

        return cls(api_key, requests_params, loop)

    def __aenter__(self):
        return self

    def __aexit__(self, exc_type, exc_val, exc_tb):
        self.close_connection()
        return False

    def _init_session(self) -> aiohttp.ClientSession:
        session = aiohttp.ClientSession(
            loop=self.loop,
            headers=self._get_headers()
        )
        return session

    async def _request(self, method, uri: str, signed: bool, **kwargs):

        kwargs = self._get_request_kwargs(method, signed, **kwargs)

        async with getattr(self.session, method)(uri, **kwargs) as response:
            self.response = response
            return await self._handle_response(response)

    @staticmethod
    async def _handle_response(response: aiohttp.ClientResponse):
        if not str(response.status).startswith('2'):
            raise APIException(response, response.status, await response.text())
        try:
            return await response.json()
        except ValueError:
            txt = await response.text()
            raise RequestException(f'Invalid Response: {txt}')

    async def _request_api(self, method, path, signed=False, version=BaseClient.PUBLIC_API_VERSION, **kwargs):
        uri = self._create_api_uri(path, version)
        return await self._request(method, uri, signed, **kwargs)

    async def _get(self, path, signed=False, version=BaseClient.PUBLIC_API_VERSION, **kwargs) -> t.Dict:
        return await self._request_api('get', path, signed, version, **kwargs)

    async def _post(self, path, signed=False, version=BaseClient.PUBLIC_API_VERSION, **kwargs) -> t.Dict:
        return await self._request_api('post', path, signed, version, **kwargs)

    async def _put(self, path, signed=False, version=BaseClient.PUBLIC_API_VERSION, **kwargs) -> t.Dict:
        return await self._request_api('put', path, signed, version, **kwargs)

    async def _delete(self, path, signed=False, version=BaseClient.PUBLIC_API_VERSION, **kwargs) -> t.Dict:
        return await self._request_api('delete', path, signed, version, **kwargs)

    async def get_market_stats(self, symbol: str = None) -> t.Dict:
        result = await self._get('markets')

        if symbol is not None:
            data = self._pick(result.get('result').get('symbols'), symbol)
            result['result'] = data

        return result

    async def get_currencies(self, currency: str = None) -> t.Dict:
        result = await self._get('currencies')

        if currency is not None:
            data = self._pick(result.get('result'), currency)
            result['result'] = data

        return result

    async def get_currencies_stats(self, currency=None) -> t.Dict:
        result = await self._get('currencies/stats')

        if currency is not None:
            data = self._pick(result.get('result'), 'key', currency)
            result['result'] = data

        return result

    async def get_orderbook(self, symbol: str) -> t.Dict:
        return await self._get('depth', params={'symbol': symbol})

    async def get_recent_trades(self, symbol: str = 'None', **kwargs) -> t.Dict:
        return await self._get('trades', params={'symbol': symbol}, **kwargs)

    async def get_ohlc_data(
            self, symbol: str = None, resolution: Resolution = None, from_date: int = None, to_date: int = None
    ) -> t.Dict:
        return await self._get('udf/history', params={
            'symbol': symbol,
            'resolution': resolution.value if resolution is not None else None,
            'from': from_date,
            'to': to_date
        })

    async def get_profile(self) -> t.Dict:
        return await self._get('account/profile', signed=True)

    async def get_cards(self) -> t.Dict:
        return await self._get('account/card-numbers', signed=True)

    async def add_card(self, card_number: str) -> t.Dict:
        return await self._post('account/card-numbers', signed=True, json={'card_number': card_number})

    async def delete_card(self, card_number: str) -> t.Dict:
        return await self._delete(f'account/card-numbers/{card_number}', signed=True)

    async def get_ibans(self) -> t.Dict:
        return await self._get('account/ibans', signed=True)

    async def add_iban(self, iban: str) -> t.Dict:
        return await self._post('account/ibans', signed=True, json={'iban': iban})

    async def delete_iban(self, iban: str) -> t.Dict:
        return await self._delete(f'account/ibans/{iban}', signed=True)

    async def get_wallets(self, asset: str) -> t.Dict:
        return await self._get(f'account/wallets/{asset}', signed=True)

    async def get_balances(self, asset: str = None) -> t.Dict:
        result = await self._get(f'account/balances', signed=True)

        if asset is not None:
            data = self._pick(result.get('result').get('balances'), asset)
            result['result']['balances'] = data

        return result

    async def get_available_balance(self, asset: str) -> float:
        result = await self.get_balances(asset)

        result = result.get('result').get('balances').get(asset.upper())

        return float(result.get('value')) - float(result.get('locked'))

    async def get_fees(self, symbol: str = None) -> t.Dict:
        result = await self._get('account/fee', signed=True)

        if symbol is not None:
            data = self._pick(result.get('result'), symbol)
            result['result'] = data

        return result

    async def create_order(
            self, symbol: str, side: str, type: str, quantity: float, price: float = None, client_id: str = None
    ) -> t.Dict:
        return await self._post('account/orders', signed=True, json=self._get_kwargs(locals()))

    async def order_market(self, symbol: str, side: str, quantity: float, client_id: str = None) -> t.Dict:
        return await self.create_order(symbol, side, self.ORDER_TYPE_MARKET, quantity, client_id)

    async def order_limit(self, symbol: str, side: str, quantity: float, price: float, client_id: str = None) -> t.Dict:
        return await self.create_order(symbol, side, self.ORDER_TYPE_LIMIT, quantity, client_id)

    async def order_market_buy(self, symbol: str, quantity: float, client_id: str = None) -> t.Dict:
        return await self.order_market(symbol, self.SIDE_BUY, quantity, client_id)

    async def order_market_sell(self, symbol: str, quantity: float, client_id: str = None) -> t.Dict:
        return await self.order_market(symbol, self.SIDE_SELL, quantity, client_id)

    async def order_limit_buy(self, symbol: str, quantity: float, price: float, client_id: str = None) -> t.Dict:
        return await self.order_limit(symbol, self.SIDE_BUY, quantity, price, client_id)

    async def order_limit_sell(self, symbol: str, quantity: float, price: float, client_id: str = None) -> t.Dict:
        return await self.order_limit(symbol, self.SIDE_SELL, quantity, price, client_id)

    async def cancel_order(self, order_id: str) -> t.Dict:
        return await self._delete(f'account/orders', signed=True, json={'clientOrderId': order_id})

    async def get_open_orders(self, symbol: str = None, side: str = None) -> t.Dict:
        result = await self._get('account/openOrders', signed=True)

        if symbol is not None:
            data = self._pick(result.get('result').get('orders'), "symbol", symbol)
            result['result'] = data

        if side is not None:
            data = self._pick(result.get('result').get('orders'), "side", side)
            result['result'] = data

        return result

    async def get_user_recent_trades(self, symbol: str = None, side: str = None, active: bool = None) -> t.Dict:
        return await self._get('account/trades', signed=True, params={
            'symbol': symbol,
            'side': side,
            'active': active
        })

    async def get_order_status(self, order_id: str) -> t.Dict:
        return await self._get(f'account/orders/{order_id}', signed=True)

    async def withdraw(
            self, coin: str, network: str, amount: float,
            address: str, client_unique_id: str, memo: t.Optional[str] = None
    ) -> t.Dict:
        return await self._post(
            'account/crypto-withdrawal', signed=True, json=self._get_kwargs(locals(), del_nones=True)
        )

    async def close_connection(self):
        if self.session:
            assert self.session
            await self.session.close()

    def __del__(self):
        asyncio.get_event_loop().create_task(self.close_connection())
