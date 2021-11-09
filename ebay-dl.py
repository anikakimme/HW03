import argparse
import requests
from bs4 import BeautifulSoup
import json
import csv

def parse_itemssold(text):
    '''
    Takes as input a string and returns the number of items sold as specified in the string.

    >>> parse_itemssold('38 sold')
    38
    >>> parse_itemssold('14 watchers')
    0
    >>> parse_itemssold('Almost gone')
    0
    '''
    numbers = ''
    for char in text:
        if char in '1234567890':
            numbers += char
    if 'sold' in text:
        return int(numbers)
    else:
        return 0

def parse_shipping(text):
    '''
    Takes as input a string and returns the number of items sold as specified in the string.

    >>> parse_shipping('Free Shipping')
    0
    >>> parse_shipping('Free 3 day Shipping')
    0
    >>> parse_shipping('+$3.99 shipping')
    399
    '''
    value = ''
    for char in text:
        if char in '1234567890':
            value += char
    if '$' in text:
        return int(value)
    else:
        return 0

    
def parse_price(text):
    '''
    Takes as input a string and returns the number of items sold as specified in the string.

    >>> parse_price('See Price')
    0
    >>> parse_price('$22.99')
    2299
    >>> parse_price('$28.00 to $29.00')
    2800
    '''
    
    value = ''
    if '$' in text:
        text = text.split()
        for char in text[0]:
            if char in '1234567890':
                value += char
        return int(value)
    else:
        return 0
    
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Download information from ebay and convert to JSON.')
    parser.add_argument('search_term')
    parser.add_argument('--num_pages', default=10)
    parser.add_argument('--csv', action = 'store_true')
    args = parser.parse_args()
    print('args.search_term=', args.search_term)
    print('args.csv=', args.csv)

    items = [] 

    for page_number in range(1,int(args.num_pages) +1):
        url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=' 
        url += args.search_term 
        url += '&_sacat=0&_pgn='
        url+= str(page_number)
        url+='&rt=nc'
        print('url=', url)
    
        r = requests.get(url)
        status = r.status_code 
        print('status=', status)

        html = r.text

        soup = BeautifulSoup(html, 'html.parser')
        
        tags_items = soup.select('.s-item')
        for tag_item in tags_items:

            tags_name =tag_item.select('.s-item__title')
            name = None
            for tag in tags_name:
                name = tag.text
            #print('name=', name)
            
            price = None
            tags_price = tag_item.select('.s-item__price')
            for tag in tags_price:
                price = parse_price(tag.text)
            #print('price=',price)

            tags_status = tag_item.select('.SECONDARY_INFO')
            status = None
            for tag in tags_status:
                status = tag.text
            #print('status=', status)
            
            shipping = 0
            tags_shipping = tag_item.select('.s-item__shipping')
            for tag in tags_shipping:
                shipping = parse_shipping(tag.text)
            #print('shipping=',shipping)
        
            freereturns = False
            tags_freereturns = tag_item.select('.s-item__free-returns')
            for tag in tags_freereturns:
                freereturns = True 
            #print('freereturns=',freereturns)
            
            items_sold = None
            tags_itemssold = tag_item.select('.s-item__hotness')
            for tag in tags_itemssold:
                items_sold = parse_itemssold(tag.text)
            #print('items sold=',items_sold)
             
            
            item = {
                'name': name,
                'free_returns': freereturns,
                'items_sold': items_sold,
                'status': status,
                'shipping': shipping,
                'price' : price
            }
            items.append(item)

        #print('len(tag_items)=', len(tags_items))
        #print('len(items)=', len(items))  
    
    if args.csv == True: 
        filename = args.search_term+ '.csv'
        outputFile = open(filename, 'w', newline='')
        outputWriter = csv.writer(outputFile)
        outputFile = outputWriter.writerow(['name', 'free_returns', 'items_sold', 'status', 'shipping', 'price'])
        for item in items:
            name = item['name']
            freereturns = item['free_returns']
            items_sold = item['items_sold']
            status = item['status']
            shipping = item['shipping']
            price = item['price']
            outputWriter.writerow([name, freereturns, items_sold, status, shipping, price])
    else:
        filename = args.search_term+ '.json'
        with open(filename, 'w', encoding='ascii') as f:
            f.write(json.dumps(items))