import time
import requests
import pandas as pd
import datetime

# CSV 파일 이름
file_name = "2023-11-12-bithumb-btc-orderbook.csv"

while True:
    # 주문서 데이터 요청
    response = requests.get('https://api.bithumb.com/public/orderbook/BTC_KRW/?count=5')
    book_data = response.json()['data']

    # bids와 asks 데이터를 DataFrame으로 변환
    bids = pd.DataFrame(book_data['bids']).apply(pd.to_numeric, errors='ignore')
    bids.sort_values('price', ascending=False, inplace=True)
    bids.reset_index(drop=True, inplace=True)
    bids['type'] = 0

    asks = pd.DataFrame(book_data['asks']).apply(pd.to_numeric, errors='ignore')
    asks.sort_values('price', ascending=True, inplace=True)
    asks['type'] = 1

    # bids와 asks를 합치고 필요한 열을 추가
    df = bids.append(asks)
    df['quantity'] = df['quantity'].round(decimals=4)

    # 현재 시간을 timestamp로 추가
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    df['timestamp'] = timestamp

    # CSV 파일로 저장 (기존 파일에 이어서 추가)
    df.to_csv(file_name, index=False, header=False, mode='a')

    # 1초 대기
    time.sleep(1)

