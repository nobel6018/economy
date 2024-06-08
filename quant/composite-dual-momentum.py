from datetime import datetime

import pandas as pd
import yfinance as yf

# 자산 목록o
assets = {
    'Part1': ['SPY', 'EFA'],
    'Part2': ['LQD', 'HYG'],
    'Part3': ['VNQ', 'REM'],
    'Part4': ['TLT', 'GLD'],
}
cash_equiv = 'BIL'

# 데이터 다운로드
start_date = '2010-01-01'
end_date = datetime.today().strftime('%Y-%m-%d')
all_assets = [item for sublist in assets.values() for item in sublist] + [cash_equiv]
data = yf.download(all_assets, start=start_date, end=end_date)['Adj Close']

# 특정 날짜 입력 받기
input_date_str = input("Enter the date (YYYY-MM-DD): ")
input_date = datetime.strptime(input_date_str, '%Y-%m-%d')


# 최근 12개월 수익률 계산 함수
def calculate_12m_return(df, date):
    past_date = date - pd.DateOffset(months=12)
    past_price = df.loc[past_date.strftime('%Y-%m-%d'):].iloc[0]
    current_price = df.loc[date.strftime('%Y-%m-%d'):].iloc[0]
    return (current_price - past_price) / past_price


# 포트폴리오 할당 결정
portfolio = {}
returns_summary = {}

for part, etfs in assets.items():
    returns = {etf: calculate_12m_return(data[etf], input_date) for etf in etfs}
    cash_return = calculate_12m_return(data[cash_equiv], input_date)

    selected_etf = max(returns, key=returns.get)
    if returns[selected_etf] < cash_return:
        selected_etf = cash_equiv

    portfolio[part] = selected_etf
    returns_summary[part] = returns
    returns_summary[part][cash_equiv] = cash_return

# 결과 출력
print(f"Date: {input_date_str}")
print("Portfolio Allocation:")
for part, etf in portfolio.items():
    print(f"{part}: {etf}")

print("\n12-Month Returns for Each Asset:")
for part, returns in returns_summary.items():
    print(f"\n{part}:")
    for etf, return_ in returns.items():
        print(f"{etf}: {return_:.2%}")

# 결과를 데이터프레임으로 저장
portfolio_df = pd.DataFrame(portfolio.items(), columns=['Part', 'Asset'])
portfolio_df['Date'] = input_date
portfolio_df = portfolio_df[['Date', 'Part', 'Asset']]

# 입력 날짜를 파일명에 반영하여 CSV 파일 저장
filename = f"composite_dual_momentum_{input_date.strftime('%Y-%m-%d')}.csv"
portfolio_df.to_csv(filename, index=False)

print(f"\nPortfolio results saved to '{filename}'")
