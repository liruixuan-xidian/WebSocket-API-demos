# -*- coding: utf-8 -*-
#author: 半熟的韭菜
from websocket import create_connection
from pymongo import MongoClient
import gzip
import time

if __name__ == '__main__':
    while(1):
        try:
            #ws = create_connection("wss://api.huobipro.com/ws")
            ws = create_connection("wss://api.hadax.com/ws")
            break
        except:
            print('connect ws error,retry...')
            time.sleep(5)

    # 订阅 KLine 数据
    tradeStr="""{"sub": "market.seelebtc.kline.1min","id": "id10"}"""

    # 请求 KLine 数据
    #tradeStr="""{"req": "market..kline.1min","id": "id10", "from": 1513391453, "to": 1513392453}"""

    #订阅 Market Depth 数据
    tradeStr="""{"sub": "market.seelebtc.depth.step5", "id": "id10"}"""

    #请求 Market Depth 数据
    # tradeStr="""{"req": "market.ethusdt.depth.step5", "id": "id10"}"""

    #订阅 Trade Detail 数据
    tradeStr="""{"sub": "market.seelebtc.trade.detail", "id": "id10"}"""

    #请求 Trade Detail 数据
    # tradeStr="""{"req": "market.ethusdt.trade.detail", "id": "id10"}"""

    #请求 Market Detail 数据
    # tradeStr="""{"req": "market.ethusdt.detail", "id": "id12"}"""
    #client = MongoClient('mongodb://ds137611.mlab.com:37611/huobi')
    client = MongoClient('mongodb://localhost:27017/')
    
    db = client.example
    ws.send(tradeStr)
    while(1):
        compressData=ws.recv()
        result=gzip.decompress(compressData).decode('utf-8')
        if result[:7] == '{"ping"':
            ts=result[8:21]
            pong='{"pong":'+ts+'}'
            ws.send(pong)
            ws.send(tradeStr)
        else:
            result = eval(result)
            if 'tick' in result.keys() and 'data' in result['tick'].keys():
                data = result['tick']['data'][0]
                print(data)
                data['id'] = str(data['id'])
                db.auto.insert(data)

    
