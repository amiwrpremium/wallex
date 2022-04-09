from inspect import currentframe as cf
import typing as t

import requests


from .exceptions import *
from ._package_data import __version__, __author__


class Wallex:
    """
    Wallex API wrapper.
    """

    MARKET_ORDER = 'market'
    LIMIT_ORDER = 'limit'
    STOP_LIMIT_ORDER = 'stop_limit'
    STOP_MARKET_ORDER = 'stop_market'

    BUY_ORDER = 'buy'
    SELL_ORDER = 'sell'

    def __init__(self, token: t.Optional[str] = None, requests_params: t.Optional[t.Dict] = None):
        self.__base_url = "https://api.wallex.ir/v1/"
        self.__requests_params = requests_params
        self.__token = token

        self.__headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

        if self.__token:
            self.__headers['Authorization'] = 'Bearer ' + self.__token

        if self.__requests_params:
            if 'headers' in self.__requests_params.keys():
                self.__headers.update(self.__requests_params.get('headers'))

        return

    @staticmethod
    def __get_func_args(all_locals: t.Dict, remove_keys: t.Optional[t.List[str]] = None) -> t.Dict:
        """
        Get function arguments.

        :param all_locals: All locals
        :type all_locals: dict

        :return: Function arguments
        :rtype: dict
        """

        if remove_keys is None:
            remove_keys = ['self']

        if 'self' not in remove_keys:
            remove_keys.append('self')

        for i in remove_keys:
            try:
                all_locals.pop(i)
            except KeyError:
                pass

        return all_locals

    def __make_headers(self, func_name: str, auth: t.Optional[bool] = True) -> t.Dict:
        """
        Make headers.

        :param func_name: Function name
        :type func_name: str

        :param auth: Authorization (optional)
        :type auth: bool

        :return: Headers
        :rtype: dict
        """

        f_args = self.__get_func_args(locals())
        headers = self.__headers.copy()

        if auth is True:
            if self.__token is None:
                raise TokenException(
                    func_name,
                    'access_token is None',
                    f_args=f_args
                )
            headers.update({
                'Authorization': f'Bearer {self.__token}'
            })

        return headers

    @staticmethod
    def __validate_response(f_name: str, response: requests.Response) -> bool:
        r_json = response.json()
        _ = r_json.get('success') is True or str(r_json.get('success')).lower() == 'true'

        if _ is False:
            raise InvalidResponse(
                f_name,
                'invalid response',
                response=response
            )

        return _

    def _process_response(
            self,
            func_name: str,
            response: requests.Response,
            additional: t.Optional[t.Dict] = None,
    ) -> t.Dict:
        """
        Check response for exceptions.

        :param response: Response
        :type response: requests.Response

        :param func_name: Function name
        :type func_name: str

        :raises: WallexExceptions

        :return: None
        :rtype: None
        """

        if additional is not None:
            additional.update(self.__get_func_args(locals()))

        if 200 <= response.status_code < 300:
            try:
                r_json: t.Dict = response.json()
            except Exception as e:
                raise JSONDecodingError(
                    func_name=func_name,
                    message='Could not decode JSON',
                    response=response,
                )

        else:
            raise StatusCodeError(
                func_name,
                f'invalid status code',
                response=response,
                additional=additional
            )

        self.__validate_response(func_name, response)

        return r_json

    def _request(
            self, func_name: str, method: str, url: str, auth: t.Optional[bool] = False,
            params: t.Optional[t.Dict] = None, data: t.Optional[t.Dict] = None, json_data: t.Optional[t.Dict] = None,
    ) -> requests.Response:
        """
        Make a request to the Bitpin API.

        :param method: HTTP method
        :type method: str

        :param url: URL
        :type url: str

        :param auth: Whether to use authentication (optional)
        :type auth: bool

        :param params: Query parameters (optional)
        :type params: dict

        :param data: Request body (optional)
        :type data: dict

        :param json_data: Request body (optional)
        :type json_data: dict

        :param func_name: Function name
        :type func_name: str

        :return: Response
        :rtype: requests.Response
        """

        f_args = self.__get_func_args(locals())
        headers = self.__make_headers(func_name, auth)

        try:
            response = requests.request(
                method,
                self.__base_url + url,
                headers=headers,
                params=params,
                json=json_data,
                data=data
            )

            return response
        except Exception as e:
            raise RequestsExceptions(
                func_name,
                e,
                f_args=f_args
            )

    def set_token(self, token: str) -> str:
        """
        Set token

        :param token: Token
        :type token: str

        :return: Token
        :rtype: str
        """

        self.__token = token
        return self.__token

    def markets_stats(self, symbol: t.Optional[str] = None) -> t.Dict:
        """
        Get markets stat.

        :return: Markets stat
        :rtype: dict
        """

        f_name = cf().f_code.co_name

        try:
            response = self._request(
                f_name,
                'GET',
                'markets'
            )
        except Exception as e:
            raise RequestsExceptions(f_name, e)

        resp = self._process_response(f_name, response)

        if symbol is not None:
            _ = resp.get('result').get('symbols').get(symbol.upper())
            if _ is None:
                raise InvalidInputs(
                    f_name,
                    f'Invalid symbol, Symbol Not Found',
                    symbol=symbol,
                )
            return _

        return resp

    def orderbook(self, symbol: str) -> t.Dict[str, t.List[t.Dict[str, t.Any]]]:
        """
        Get orderbook.

        :param symbol: Symbol
        :type symbol: str

        :return: Orderbook
        :rtype: dict
        """

        f_name = cf().f_code.co_name

        try:
            response = self._request(
                f_name,
                'GET',
                f'depth?symbol={symbol.upper()}'
            )
        except Exception as e:
            raise RequestsExceptions(f_name, e)

        return self._process_response(f_name, response)

    def balances(self, asset: t.Optional[str] = None) -> t.Dict:
        """
        Get balances.

        :param asset: Asset (optional)
        :type asset: str

        :return: Balances
        :rtype: dict
        """

        f_name = cf().f_code.co_name

        try:
            response = self._request(
                f_name,
                'GET',
                'account/balances',
                auth=True
            )
        except Exception as e:
            raise RequestsExceptions(f_name, e)

        resp = self._process_response(f_name, response)

        if asset is not None:
            return resp.get('result').get('balances').get(asset.upper())

        return resp

    def available_balance(self, asset: str) -> float:
        """
        Get available balances.

        :return: Available balances
        :rtype: dict
        """

        f_name = cf().f_code.co_name

        try:
            balances = self.balances(asset)
            return float(balances.get('value')) - float(balances.get('locked'))

        except Exception as e:
            raise WallexExceptions(f_name, e)

    def create_order(
            self,
            symbol: str,
            side: str,
            quantity: t.Union[float, int],
            price: t.Union[float, int],
            order_type: str,
            stop_price: t.Optional[t.Union[float, int]] = None,
            client_order_id: t.Optional[str] = None
    ) -> t.Dict:
        """
        Create order.

        :param symbol: Symbol
        :type symbol: str

        :param side: Side
        :type side: str

        :param quantity: Amount
        :type quantity: str

        :param price: Price
        :type price: str

        :param order_type: Order type
        :type order_type: str

        :param stop_price: Stop price (optional)
        :type stop_price: str

        :param client_order_id: Client order ID (optional)
        :type client_order_id: str

        :return: Order
        :rtype: dict
        """

        f_name = cf().f_code.co_name

        data = {
            "price": str(price),
            "quantity": str(quantity),
            "side": side.lower(),
            "symbol": symbol.upper(),
            "type": order_type.lower(),
        }

        if client_order_id is not None:
            data.update({'client_id': client_order_id})

        if order_type.lower() == self.STOP_LIMIT_ORDER or order_type.lower() == self.STOP_MARKET_ORDER:
            if stop_price is None:
                raise InvalidInputs(
                    f_name,
                    f'Stop price is required for {order_type} order',
                    order_type=order_type,
                    stop_price=stop_price
                )
            data.update({'stop_price': str(stop_price)})

        try:
            response = self._request(
                f_name,
                'POST',
                'account/orders',
                auth=True,
                json_data=data
            )
        except Exception as e:
            raise RequestsExceptions(f_name, e)

        return self._process_response(f_name, response)

    def cancel_order(self, order_id: str) -> t.Dict:
        """
        Cancel order.

        :param order_id: Order ID
        :type order_id: str

        :return: Order
        :rtype: dict
        """

        f_name = cf().f_code.co_name

        data = {
            "clientOrderId": order_id
        }

        try:
            response = self._request(
                f_name,
                'DELETE',
                f'account/orders',
                auth=True,
                json_data=data
            )
        except Exception as e:
            raise RequestsExceptions(f_name, e)

        return self._process_response(f_name, response)

    def open_orders(self, symbol: t.Optional[str] = None, side: t.Optional[str] = None) -> t.Dict:
        """
        Get open orders.

        :param symbol: Symbol (optional)
        :type symbol: str

        :param side: Side (optional)
        :type side: str

        :return: Open orders
        :rtype: dict
        """

        f_name = cf().f_code.co_name

        params = {}

        url = f'account/openOrders'
        if symbol is not None:
            url += f'?symbol={symbol.upper()}'

        try:
            response = self._request(
                f_name,
                'GET',
                url,
                auth=True,
                params=params
            )
        except Exception as e:
            raise RequestsExceptions(f_name, e)

        resp = self._process_response(f_name, response)

        if side is not None:
            all_orders = resp.get('result').get('orders')
            for order in all_orders:
                if order.get('side').lower() != side.lower():
                    all_orders.remove(order)

        return resp

    def user_recent_trades(self, symbol: t.Optional[str] = None,
                           side: t.Optional[str] = None, active: t.Optional[bool] = None) -> t.Dict:
        """
        Get user recent trades.

        :param symbol: Symbol (optional)
        :type symbol: str

        :param side: Side (optional)
        :type side: str

        :param active: Active (optional)
        :type active: bool

        :return: User recent trades
        :rtype: dict
        """

        f_name = cf().f_code.co_name

        params = {}

        if symbol:
            params.update({'symbol': symbol.upper()})
        if side:
            params.update({'side': side.lower()})
        if active:
            params.update({'active': active})

        try:
            response = self._request(
                f_name,
                'GET',
                'account/trades',
                auth=True,
                params=params
            )
        except Exception as e:
            raise RequestsExceptions(f_name, e)

        return self._process_response(f_name, response)

    def order_status(self, order_id: str) -> t.Dict:
        """
        Get order status.

        :param order_id: Order ID
        :type order_id: str

        :return: Order status
        :rtype: dict
        """

        f_name = cf().f_code.co_name

        try:
            response = self._request(
                f_name,
                'GET',
                f'account/orders/{order_id}',
                auth=True,
            )
        except Exception as e:
            raise RequestsExceptions(f_name, e)

        return self._process_response(f_name, response)

    def withdraw(self, coin: str, network: str, amount: t.Union[int, float],
                 address: str, client_unique_id: str, memo: t.Optional[str] = None):
        """
        Withdraw.

        :param coin: Coin
        :type coin: str

        :param client_unique_id: Client unique ID
        :type client_unique_id: str

        :param network: Network
        :type network: str

        :param amount: Amount
        :type amount: str

        :param address: Address
        :type address: str

        :param memo: Memo (optional)
        :type memo: str

        :return: Withdraw
        :rtype: dict
        """

        f_name = cf().f_code.co_name

        data = {
            "coin": coin.upper(),
            "client_unique_id": str(client_unique_id),
            "network": network,
            "value": str(amount),
            "wallet_address": address,
        }
        if memo:
            data.update({'memo': memo})

        try:
            response = self._request(
                f_name,
                'POST',
                'account/crypto-withdrawal',
                auth=True,
                json_data=data
            )
        except Exception as e:
            raise RequestsExceptions(f_name, e)

        return self._process_response(f_name, response)

    def __str__(self):
        return f'Wallex API Client, By {__author__}, Version {__version__}'

    def __repr__(self):
        return f'Wallex API Client, By {__author__}, Version {__version__}'
