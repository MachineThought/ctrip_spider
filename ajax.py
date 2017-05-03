import requests

def ajax():
    url = "http://vacations.ctrip.com/bookingnext/CalendarV2/CalendarInfo?ProductID=17185842&StartCity=2&SalesCity=2&MinPrice=1870&EffectDate=2015-12-15&ExpireDate=2017-06-30&ClientSource=Online&uid=&TourGroupProductIds=%5B17185842%5D&startDate=2017-4-30&endDate=2017-6-10&_=1493802478358"
    content = requests.get(url).content
    print(content)

ajax()