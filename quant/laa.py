import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime

# 자산 목록
fixed_assets = ['IWD', 'GLD', 'IEF']
timing_assets = ['QQQ', 'SHY']  # 나스닥 100 지수(QQQ)와 미국 단기국채(SHY)

# 데이터 다운로드
start_date = '2010-01-01'
end_date = datetime.today().strftime('%Y-%m-%d')
data = yf.download(fixed_assets + timing_assets + ['^GSPC'], start=start_date, end=end_date)['Adj Close']

# 특정 날짜 입력 받기
input_date_str = input("Enter the date (YYYY-MM-DD): ")
input_date = datetime.strptime(input_date_str, '%Y-%m-%d')

# 이동평균 및 실업률 데이터 (가상의 실업률 데이터를 생성합니다)
# 실제 실업률 데이터는 경제 지표 API 등을 통해 가져와야 합니다.
unemployment_rate = pd.Series(np.random.rand(len(data)), index=data.index)  # 가상의 데이터
unemployment_rate_ma = unemployment_rate.rolling(window=12).mean()

# S&P 500 200일 이동평균
sp500_ma200 = data['^GSPC'].rolling(window=200).mean()

# 매수 전략 결정
if data['^GSPC'].loc[input_date] < sp500_ma200.loc[input_date] and unemployment_rate.loc[input_date] > \
        unemployment_rate_ma.loc[input_date]:
    selected_timing_asset = 'SHY'
else:
    selected_timing_asset = 'QQQ'

# 포트폴리오 할당
portfolio = {
    'IWD': 0.25,
    'GLD': 0.25,
    'IEF': 0.25,
    selected_timing_asset: 0.25
}

# 결과 출력
print(f"Date: {input_date_str}")
print("Portfolio Allocation:")
for asset, allocation in portfolio.items():
    print(f"{asset}: {allocation * 100:.2f}%")

# 결과를 데이터프레임으로 저장
portfolio_df = pd.DataFrame(portfolio.items(), columns=['Asset', 'Allocation'])
portfolio_df['Date'] = input_date
portfolio_df = portfolio_df[['Date', 'Asset', 'Allocation']]

# 입력 날짜를 파일명에 반영하여 CSV 파일 저장
filename = f"laa_portfolio_{input_date.strftime('%Y-%m-%d')}.csv"
portfolio_df.to_csv(filename, index=False)

print(f"\nPortfolio results saved to '{filename}'")
