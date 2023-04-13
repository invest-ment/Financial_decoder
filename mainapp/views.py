from django.http.response import HttpResponse
from django.shortcuts import render
from yahoo_fin.stock_info import *
import time
import queue
import yfinance as yf
from threading import Thread
from asgiref.sync import sync_to_async
# Create your views here.
def stockPicker(request):
    stock_picker = tickers_nifty50()
    print(stock_picker)
    return render(request, 'mainapp/stockpicker.html', {'stockpicker':stock_picker})

'''def checkAuthenticated(request):
    if not request.user.is_authenticated:
        return False
    else:
        return True'''
def stockTracker(request):
    '''is_loginned = await checkAuthenticated(request)
    if not is_loginned:
        return HttpResponse("Login First")'''
    stockpicker = request.GET.getlist('stockpicker')
    stockshare=str(stockpicker)[1:-1]
    
    print(stockpicker)
    data = {}
    available_stocks = tickers_nifty50()
    for i in stockpicker:
        if i in available_stocks:
            pass
        else:
            return HttpResponse("Error")
    
    n_threads = len(stockpicker)
    thread_list = []
    que = queue.Queue()
    start = time.time()
    #for i in stockpicker:
    #    result = get_quote_table(i)
    #    data.update({i: result})
    '''for i in range(n_threads):
        thread = Thread(target = lambda q, arg1: q.put({stockpicker[i]: get_quote_table(arg1)}), args = (que, stockpicker[i]))
        #print(thread)
        thread_list.append(thread)
        thread_list[i].start()

    for thread in thread_list:
        thread.join()
    
    while not que.empty():
        result = que.get()
        data.update(result)
        #print(result)'''
    for i in stockpicker:
        ticker = yf.Ticker(i)
        stock_data = {
    "open": ticker.info.get("regularMarketOpen"),
    "high": ticker.info.get("regularMarketDayHigh"),
    "low": ticker.info.get("regularMarketDayLow"),
    "close": ticker.info.get("regularMarketPrice"),
    "volume": ticker.info.get("regularMarketVolume"),
    "market_cap": ticker.info.get("marketCap"),
    "forward_PE": ticker.info.get("forwardPE")
}
        que.put({i: stock_data})
    end = time.time()
    time_taken =  end - start
    print(time_taken)
    while not que.empty():
        result = que.get()
        data.update(result)
    print(data)
    return render(request, 'mainapp/stocktracker.html', {'data': data, 'room_name': 'track','selectedstock':stockshare})
