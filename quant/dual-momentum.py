from typing import List

import yfinance as yf
import pandas as pd


def calculate_momentum(ticker) -> float:
    # 오늘 날짜
    end_date = pd.Timestamp.today()

    # 12개월 전 날짜
    start_date = end_date - pd.DateOffset(months=12)

    # 데이터 다운로드
    data = yf.download(ticker, start=start_date, end=end_date)

    # 12개월 전 가격과 현재 가격
    price_12_months_ago = data['Adj Close'].iloc[0]
    current_price = data['Adj Close'].iloc[-1]

    # 12개월 수익률 계산
    return_12_months = (current_price - price_12_months_ago) / price_12_months_ago * 100

    return return_12_months


class AssetMomentum:
    def __init__(self, asset: str, momentum: float):
        self.asset = asset
        self.momentum = momentum


def dual_momentum(strategy_assets: List[str], base_asset_momentum: AssetMomentum) -> AssetMomentum:
    result: AssetMomentum = base_asset_momentum
    for strategy_asset in strategy_assets:
        momentum = calculate_momentum(strategy_asset)
        print(f"{strategy_asset} momentum: {momentum:.2f}%")
        if momentum > result.momentum:
            result = AssetMomentum(strategy_asset, momentum)

    return result


def calculate_total():
    base_asset_momentum = AssetMomentum('BIL', calculate_momentum('BIL'))
    print(f"Base asset: {base_asset_momentum.asset}, Momentum: {base_asset_momentum.momentum:.2f}%")

    # part1: 주식 - SPY vs EFA
    part1 = dual_momentum(['SPY', 'EFA'], base_asset_momentum)
    print(f"Best asset: {part1.asset}, Momentum: {part1.momentum:.2f}%\n")

    # part2: 채권 - LQD vs HYG
    part2 = dual_momentum(['LQD', 'HYG'], base_asset_momentum)
    print(f"Best asset: {part2.asset}, Momentum: {part2.momentum:.2f}%\n")

    # part3: 부동산 - VNQ vs REM
    part3 = dual_momentum(['VNQ', 'REM'], base_asset_momentum)
    print(f"Best asset: {part3.asset}, Momentum: {part3.momentum:.2f}%\n")

    # part4: 불경기 - TLT vs GLD
    part4 = dual_momentum(['TLT', 'GLD'], base_asset_momentum)
    print(f"Best asset: {part4.asset}, Momentum: {part4.momentum:.2f}%\n")


if __name__ == '__main__':
    calculate_total()
