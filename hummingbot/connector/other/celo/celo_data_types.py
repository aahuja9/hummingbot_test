from decimal import Decimal
from typing import NamedTuple

from pydantic import Field, SecretStr

from hummingbot.client.config.config_data_types import BaseConnectorConfigMap, ClientFieldData


class CeloExchangeRate(NamedTuple):
    from_token: str
    from_amount: Decimal
    to_token: str
    to_amount: Decimal


class CeloBalance(NamedTuple):
    token: str
    total: Decimal
    locked: Decimal

    def available(self):
        return self.total - self.locked


class CeloArbTradeProfit(NamedTuple):
    is_celo_buy: bool  # Celo order side, buy if this is true, else sell.
    ctp_price: Decimal  # Counter party order price, the opposite side of Celo order, so sell if is_celo_buy is true.
    ctp_vwap: Decimal  # Counter party vwap price, used to calculate celo buy volume and profit
    celo_price: Decimal  # Celo order price.
    profit: Decimal  # profit in percentage

    def __repr__(self) -> str:
        return (
            f"Celo side: {'Buy' if self.is_celo_buy else 'Sell'}, Celo price: {self.celo_price:.3f}, "
            f"Counter party price: {self.ctp_price:.3f}, Profit: {self.profit:.2%}"
        )


class CeloOrder(NamedTuple):
    tx_hash: str
    is_buy: bool
    price: Decimal
    amount: Decimal
    timestamp: float

    def __repr__(self) -> str:
        return (
            f"Celo Order - tx_hash: {self.tx_hash}, side: {'buy' if self.is_buy else 'sell'}, "
            f"price: {self.price}, amount: {self.amount}."
        )


class CeloConfigMap(BaseConnectorConfigMap):
    """
    As Celo is treated as a special case everywhere else in the code,
    its canfigs cannot be stored and handled the conventional way either (i.e. using celo_utils.py).
    """
    connector: str = Field(default="celo", client_data=None)
    celo_address: str = Field(
        default=...,
        client_data=ClientFieldData(
            prompt=lambda cm: "Enter your Celo account address",
            is_connect_key=True,
            prompt_on_new=True,
        )
    )
    celo_password: SecretStr = Field(
        default=...,
        client_data=ClientFieldData(
            prompt=lambda cm: "Enter your Celo account password",
            is_secure=True,
            is_connect_key=True,
            prompt_on_new=True,
        )
    )

    class Config:
        title = "celo"


KEYS = CeloConfigMap.construct()
