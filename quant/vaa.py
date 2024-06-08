from datetime import datetime

import pandas as pd
import yfinance as yf

# 자산 목록
assets_aggressive = ['SPY', 'EFA', 'EEM', 'AGG', 'QQQ', 'TQQQ']
assets_safe = ['LQD', 'IEF', 'SHY']

# 데이터 다운로드
start_date = '2010-01-01'
end_date = datetime.today().strftime('%Y-%m-%d')
data = yf.download(assets_aggressive + assets_safe, start=start_date, end=end_date)['Adj Close']

# 특정 날짜 입력 받기
input_date_str = input("Enter the date (YYYY-MM-DD): ")
input_date = datetime.strptime(input_date_str, '%Y-%m-%d')


# 특정 날짜를 기준으로 수익률 계산 함수
def calculate_returns(data, end_date, months):
    start_date = end_date - pd.DateOffset(months=months)
    start_price = data.loc[start_date.strftime('%Y-%m-%d'):].iloc[0]
    end_price = data.loc[end_date.strftime('%Y-%m-%d'):].iloc[0]
    return (end_price - start_price) / start_price * 100


# 모멘텀 스코어 계산 함수
def calculate_momentum_score(data, date):
    returns_1m = calculate_returns(data, date, 1)
    returns_3m = calculate_returns(data, date, 3)
    returns_6m = calculate_returns(data, date, 6)
    returns_12m = calculate_returns(data, date, 12)

    momentum_score = (12 * returns_1m) + (4 * returns_3m) + (2 * returns_6m) + returns_12m
    return momentum_score


# 모멘텀 스코어 계산
momentum_scores_aggressive = calculate_momentum_score(data[assets_aggressive], input_date)
momentum_scores_safe = calculate_momentum_score(data[assets_safe], input_date)

# 모멘텀 스코어 출력
print("Momentum Scores (Aggressive Assets):")
print(momentum_scores_aggressive)
print("\nMomentum Scores (Safe Assets):")
print(momentum_scores_safe)

# 최종 포트폴리오 결정
if (momentum_scores_aggressive > 0).all():
    selected_asset = momentum_scores_aggressive.idxmax()
    selected_score = momentum_scores_aggressive.max()
else:
    selected_asset = momentum_scores_safe.idxmax()
    selected_score = momentum_scores_safe.max()

# 포트폴리오 결과 출력
print("\nSelected Asset for Portfolio:")
print(f"Asset: {selected_asset}, Momentum Score: {selected_score}")

# 포트폴리오 결과 저장
portfolio = pd.DataFrame(index=[input_date], columns=['Asset', 'Momentum_Score'])
portfolio.index.name = 'Date'
portfolio.loc[input_date] = [selected_asset, selected_score]

filename = f"vaa_aggressive_portfolio_{input_date.strftime('%Y-%m-%d')}.csv"
portfolio.to_csv(filename)
