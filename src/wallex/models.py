import typing as t
from pydantic import BaseModel, Field, root_validator
from datetime import datetime


class ResultInfo(BaseModel):
    page: int
    per_page: int
    count: int
    total_count: int


class _Response(BaseModel):
    result: t.Dict[str, BaseModel]
    message: str
    success: bool


class MarketStats(_Response):
    class Result(BaseModel):
        class Symbols(BaseModel):
            class Stats(BaseModel):
                class Direction(BaseModel):
                    SELL: int
                    BUY: int

                bidPrice: float
                askPrice: float
                twentyFourHourChannel: t.Union[str, float] = Field(None, alias='24h_ch')
                sevenDayChannel: t.Union[str, float] = Field(None, alias='7d_ch')
                twentyFourHourVolume: t.Union[str, float] = Field(None, alias='24h_volume')
                sevenDayVolume: t.Union[str, float] = Field(None, alias='7d_volume')
                twentyFourHourQuoteVolume: t.Union[str, float] = Field(None, alias='24h_quoteVolume')
                twentyFourHourHighPrice: t.Union[str, float] = Field(None, alias='24h_highPrice')
                twentyFourHourLowPrice: t.Union[str, float] = Field(None, alias='24h_lowPrice')
                lastPrice: t.Union[float, str]
                lastQty: t.Union[float, str]
                lastTradeSide: str
                bidVolume: float
                askVolume: float
                bidCount: int
                askCount: int
                direction: Direction

            symbol: str
            baseAsset: str
            baseAssetPrecision: int
            quoteAsset: str
            quotePrecision: int
            faName: str
            faBaseAsset: str
            faQuoteAsset: str
            stepSize: int
            tickSize: int
            minQty: float
            minNotional: float
            stats: Stats
            createdAt: datetime

        symbols: t.Dict[str, Symbols]

    result: Result


class Currencies(_Response):
    class Result(BaseModel):
        class TransactionFee(BaseModel):
            percent: float
            max_fee: float

        class Network(BaseModel):
            id: int
            name: str
            message: t.Optional[str]
            type: str
            deposit_availability: str
            withdrawal_availability: str
            deposit_unavailability_reason: t.Optional[str]
            withdrawal_unavailability_reason: t.Optional[str]
            min_confirmation: int
            transaction_fee: float
            min_withdrawal_value: float
            min_deposit_value: float

        key: str
        name: str
        name_en: str
        type: str
        base: bool
        precision: int
        message: t.Optional[str]
        deposit_availability: str
        withdrawal_availability: str
        updated_at: t.Optional[datetime]
        transaction_fee: t.Optional[TransactionFee]
        min_withdrawal_value: t.Optional[float]
        network: t.Optional[t.List[Network]]

    result: t.Dict[str, Result]
    provider: str
    result_info: ResultInfo


class CurrenciesStats(_Response):
    class Result(BaseModel):
        key: str
        name: str
        name_en: str
        rank: t.Optional[int]
        dominance: t.Optional[float]
        volume_24h: t.Optional[float]
        market_cap: t.Optional[float]
        ath: t.Optional[float]
        ath_change_percentage: t.Optional[float]
        ath_date: t.Optional[datetime]
        price: t.Optional[float]
        daily_high_price: t.Optional[float]
        daily_low_price: t.Optional[float]
        weekly_high_price: t.Optional[float]
        weekly_low_price: t.Optional[float]
        percent_change_1h: t.Optional[float]
        percent_change_24h: t.Optional[float]
        percent_change_7d: t.Optional[float]
        percent_change_14d: t.Optional[float]
        percent_change_30d: t.Optional[float]
        percent_change_60d: t.Optional[float]
        percent_change_200d: t.Optional[float]
        percent_change_1y: t.Optional[float]
        price_change_24h: t.Optional[float]
        price_change_7d: t.Optional[float]
        price_change_14d: t.Optional[float]
        price_change_30d: t.Optional[float]
        price_change_60d: t.Optional[float]
        price_change_200d: t.Optional[float]
        price_change_1y: t.Optional[float]
        max_supply: t.Optional[float]
        total_supply: t.Optional[float]
        circulating_supply: t.Optional[float]
        created_at: t.Optional[datetime]
        updated_at: t.Optional[datetime]

    result: t.List[Result]
    provider: str
    result_info: ResultInfo


class Orderbook(_Response):
    class Result(BaseModel):
        class Order(BaseModel):
            price: float
            quantity: float
            sum: float

        ask: t.List[Order]
        bid: t.List[Order]

    result: Result


class RecentTrades(_Response):
    class Result(BaseModel):
        class Trade(BaseModel):
            symbol: str
            quantity: float
            price: float
            sum: float
            isBuyOrder: bool
            timestamp: datetime

        latestTrades: t.List[Trade]

    result: Result

#
# class OHLC(_Response):
#     raise NotImplementedError

    # class Result(BaseModel):
    #     class OHLC(BaseModel):
    #         open: t.List[float] = Field(None, alias='o')
    #         high: t.List[float] = Field(None, alias='h')
    #         low: t.List[float] = Field(None, alias='l')
    #         close: t.List[float] = Field(None, alias='c')
    #         volume: t.List[float] = Field(None, alias='v')
    #         timestamp: t.List[datetime] = Field(None, alias='t')
    #
    #     ohlc: t.List[OHLC]
    #
    # result: Result


setting_sample = {
    'result': {
        'tracking_id': 244283,
        'first_name': 'امیرمهدی',
        'last_name': 'عرفانی زاده',
        'national_code': '0024****103',
        'face_image': None,
        'birthday': '2001-07-31T00:00:00Z',
        'address': {
            'city': '',
            'country': '',
            'location': 'شهرآرا، کوچه 38، پلاک 21, واحد 3',
            'province': '',
            'postal_code': '',
            'house_number': ''
        },
        'phone_number': {
            'area_code': '021',
            'main_number': '88265241'
        },
        'mobile_number': '0939****814',
        'verification': 'VERIFIED',
        'email': 'am**********@g****.com',
        'invite_code': 'BnAvR',
        'avatar': None,
        'commission': 25,
        'settings': {
            'theme': 'light',
            'mode': 'pro',
            'order_submit_confirm': False,
            'order_delete_confirm': True,
            'default_mode': True,
            'favorite_markets': [],
            'choose_trading_type': True,
            'coin_deposit': True,
            'coin_withdraw': True,
            'money_deposit': True,
            'money_withdraw': True,
            'logins': True,
            'trade': True,
            'api_key_expiration': True,
            '0': 'manual_deposit',
            'notification': {
                'email': {
                    'is_enable': True,
                    'actions': {
                        'coin_deposit': {'is_enable': True, 'label': 'واریز کوین'},
                        'coin_withdraw': {'is_enable': True, 'label': 'برداشت کوین'},
                        'money_deposit': {'is_enable': True, 'label': 'واریز تومان'},
                        'money_withdraw': {'is_enable': True, 'label': 'برداشت تومان'},
                        'logins': {'is_enable': True, 'label': 'فعالیتها'},
                        'api_key_expiration': {'is_enable': True, 'label': 'labels.profile_settings.api_key_expiration'},
                        'manual_deposit': {'is_enable': True, 'label': 'labels.profile_settings.manual_deposit'}
                    },
                    'label': 'ایمیل'
                },
                'announcement': {
                    'is_enable': True,
                    'actions': {
                        'coin_deposit': {'is_enable': True, 'label': 'واریز کوین'},
                        'coin_withdraw': {'is_enable': True, 'label': 'برداشت کوین'},
                        'money_deposit': {'is_enable': True, 'label': 'واریز تومان'},
                        'money_withdraw': {'is_enable': True, 'label': 'برداشت تومان'},
                        'logins': {'is_enable': True, 'label': 'فعالیتها'},
                        'trade': {'is_enable': True, 'label': 'معامله'},
                        'api_key_expiration': {'is_enable': True, 'label': 'labels.profile_settings.api_key_expiration'},
                        'manual_deposit': {'is_enable': True, 'label': 'labels.profile_settings.manual_deposit'},
                        'price_alert': {'is_enable': True, 'label': 'labels.profile_settings.price_alert'}},
                    'label': 'اطلاعیه داخل سایت(اپلیکیشن)'
                },
                'push': {
                    'is_enable': True,
                    'actions': {
                        'coin_deposit': {'is_enable': True, 'label': 'واریز کوین'},
                        'coin_withdraw': {'is_enable': True, 'label': 'برداشت کوین'},
                        'money_deposit': {'is_enable': True, 'label': 'واریز تومان'},
                        'money_withdraw': {'is_enable': True, 'label': 'برداشت تومان'},
                        'logins': {'is_enable': True, 'label': 'فعالیتها'},
                        'trade': {'is_enable': True, 'label': 'معامله'},
                        'api_key_expiration': {'is_enable': True, 'label': 'labels.profile_settings.api_key_expiration'},
                        'manual_deposit': {'is_enable': True,'label': 'labels.profile_settings.manual_deposit'},
                        'price_alert': {'is_enable': True,'label': 'labels.profile_settings.price_alert'}
                    },
                    'label': 'Push Notification'
                }
            }
        },
        'status': {
            'first_name': 'ACCEPTED',
            'last_name': 'ACCEPTED',
            'national_code': 'ACCEPTED',
            'national_card_image': 'ACCEPTED',
            'face_image': 'UNFILLED',
            'face_video': 'UNFILLED',
            'birthday': 'ACCEPTED',
            'address': 'ACCEPTED',
            'phone_number': 'ACCEPTED',
            'mobile_number': 'ACCEPTED',
            'email': 'ACCEPTED'
        },
        'kyc_info': {
            'details': {
                'mobile_activation': True,
                'personal_info': True,
                'financial_info': True,
                'phone_number': True,
                'national_card': True,
                'face_recognition': True,
                'admin_approval': True
            },
            'level': 2
        },
        'meta': {
            'disabled_features': [
                'BOT_USER_CRYPTO_WITHDRAWAL_EXTRA_VERIFICATION_STEP',
                'quick trade',
                'QUICK_TRADE',
                'REWARDS_HUB'
            ]
        }
    },
    'message': 'The operation was successful',
    'success': True
}


class Profile(_Response):
    class Result(BaseModel):
        class Address(BaseModel):
            city: str
            country: str
            location: str
            province: str
            postal_code: str
            house_number: str

        class PhoneNumber(BaseModel):
            area_code: str
            main_number: str

        class Settings(BaseModel):
            class Notification(BaseModel):
                class Email(BaseModel):
                    class Actions(BaseModel):
                        class Action(BaseModel):
                            is_enable: bool
                            label: str

                        coin_deposit: Action
                        coin_withdraw: Action
                        money_deposit: Action
                        money_withdraw: Action
                        logins: Action
                        api_key_expiration: Action
                        manual_deposit: Action

                    is_enable: bool
                    actions: Actions
                    label: str

                class AnnouncementAndPush(BaseModel):
                    class Action(BaseModel):
                        is_enable: bool
                        label: str

                    coin_deposit: Action
                    coin_withdraw: Action
                    money_deposit: Action
                    money_withdraw: Action
                    logins: Action
                    trade: Action
                    api_key_expiration: Action
                    manual_deposit: Action
                    price_alert: Action

                    is_enable: bool
                    actions: Action
                    label: str

                email: Email
                announcement: AnnouncementAndPush
                push: AnnouncementAndPush

            theme: str
            mode: str
            order_submit_confirm: bool
            order_delete_confirm: bool
            default_mode: bool
            favorite_markets: t.List[str]
            choose_trading_type: bool
            coin_deposit: bool
            coin_withdraw: bool
            money_deposit: bool
            money_withdraw: bool
            logins: bool
            trade: bool
            api_key_expiration: bool
            zero: str = Field(None, alias='0')
            notification: Notification

        tracking_id: int
        first_name: str
        last_name: str
        national_code: str
        face_image: t.Optional[str]
        birthday: datetime
        address: Address
        phone_number: PhoneNumber
        mobile_number: str
        verification: str
        email: str
        invite_code: t.Optional[str]
        avatar: t.Optional[str]
        commission: int
        settings: Settings

    result: Result


class Wallets(_Response):
    class Result(BaseModel):
        class CoinType(BaseModel):
            key: str
            name: str
            name_en: str
            type: str
            deposit_availability: str = Field(None, enum=['ENABLE', 'DISABLE'])
            withdrawal_availability: str = Field(None, enum=['ENABLE', 'DISABLE'])
            deposit_unavailability_reason: t.Optional[str]
            withdrawal_unavailability_reason: t.Optional[str]

        class Wallet(BaseModel):
            class Network(BaseModel):
                id: int
                name: str
                message: t.Optional[str]
                type: str
                deposit_availability: str = Field(None, enum=['ENABLE', 'DISABLE'])
                withdrawal_availability: str = Field(None, enum=['ENABLE', 'DISABLE'])
                deposit_unavailability_reason: t.Optional[str]
                withdrawal_unavailability_reason: t.Optional[str]

            address: str
            memo: t.Optional[str]
            min_confirmation: int
            transaction_fee: float
            min_withdrawal_value: float
            min_deposit_value: float

        coin_type: CoinType
        wallets: t.Dict[str, Wallet]

    result: Result
    provider: str


class Balances(_Response):
    class Result(BaseModel):
        class Balance(BaseModel):
            asset: str
            faName: str
            fiat: bool
            value: float
            locked: float
            free: float = None

            @root_validator(pre=True)
            def _calculate_free_balance(cls, values):
                total = float(values.get('value'))
                locked = float(values.get('locked'))

                free = values.get('free')

                if free is None:
                    free = total - locked
                values['free'] = float(free)
                return values

        balances: t.Dict[str, Balance]

    result: Result


class Fees(_Response):
    class Result(BaseModel):
        makerFeeRate: t.Optional[float]
        takerFeeRate: t.Optional[float]
        recent_days_sum: t.Optional[float]

    result: t.Dict[str, Result]


class Order(BaseModel):
    class Result(BaseModel):
        class Fills(BaseModel):
            price: float
            quantity: float
            fee: float
            feeCoefficient: float
            feeAsset: str
            timestamp: datetime
            symbol: str
            sum: float
            makerFeeCoefficient: float
            takerFeeCoefficient: float
            isBuyer: bool

            side: str = None

            @root_validator(pre=True)
            def _find_side(cls, values):
                if values.get('isBuyer'):
                    values['side'] = 'buy'
                else:
                    values['side'] = 'sell'
                return values

        symbol: str = Field(None, alias='symbol')
        type: str = Field(None, alias='type')
        side: str = Field(None, alias='side')
        client_order_id: str = Field(None, alias='clientOrderId')
        transact_time: datetime = Field(None, alias='transactTime')
        price: float = Field(None, alias='price')
        orig_qty: float = Field(None, alias='origQty')
        executed_sum: float = Field(None, alias='executedSum')
        executed_qty: float = Field(None, alias='executedQty')
        executed_price: float = Field(None, alias='executedPrice')
        sum: float = Field(None, alias='sum')
        executed_percent: float = Field(None, alias='executedPercent')
        status: str = Field(None, alias='status')
        active: bool = Field(None, alias='active')
        fills: t.List[Fills] = Field(None, alias='fills')
        created_at: t.Optional[datetime] = Field(None, alias='created_at')

    result: Result
    # TODO add enum for status


class OpenOrders(_Response):
    class Result(BaseModel):
        orders: t.List[Order.Result]

    result: Result
