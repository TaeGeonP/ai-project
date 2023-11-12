import csv
import time
import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode
import requests
import pandas as pd

# 주문서 데이터를 생성하는 가상 함수 (실제 데이터에 대한 대체)
def generate_order_book_data():
    while(1):
        
        book = {}
        response = requests.get ('https://api.upbit.com/public/orderbook/BTC_KRW/?count=5')
        book = response.json()


        data = book['data']

        bids = (pd.DataFrame(data['bids'])).apply(pd.to_numeric,errors='ignore')
        bids.sort_values('price', ascending=False, inplace=True)
        bids = bids.reset_index(); del bids['index']
        bids['type'] = 0
    
        asks = (pd.DataFrame(data['asks'])).apply(pd.to_numeric,errors='ignore')
        asks.sort_values('price', ascending=True, inplace=True)
        asks['type'] = 1 

        print (bids)
        print ("\n")
        print (asks)

        time.sleep(4.9)
        

        df = bids.append(asks)
    
        timestamp = datetime.datetime.now()
        req_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')

        df['quantity'] = df['quantity'].round(decimals=4)
        df['timestamp'] = req_timestamp
    
        #print (df)
        #print ("\n")
    
        df.to_csv("./2022-05-18-upbit-orderbook.csv", index=False, header=False, mode = 'a')
 

# CSV 파일에 데이터를 기록하는 함수
def write_order_book_to_csv(file_path, data):
    with open(file_path, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        
        # 파일이 비어있으면 헤더를 쓴다.
        if file.tell() == 0:
            writer.writeheader()
        
        writer.writerow(data)

# 주문서 데이터를 1초마다 CSV 파일로 저장
def record_order_book():
    while True:
        order_data = generate_order_book_data()
        write_order_book_to_csv('order_book.csv', order_data)
        time.sleep(1)

if __name__ == "__main__":
    record_order_book()
