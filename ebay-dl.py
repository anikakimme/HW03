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
    
# this if statement says only run the code below when the python file is run "normally"
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Download information from ebay and convert to JSON.')
    parser.add_argument('search_term')
    parser.add_argument('--num_pages', default=10)
    parser.add_argument('--csv', action = 'store_true')
    args = parser.parse_args()
    print('args.search_term=', args.search_term)

    items = [] # list of all items found in all ebay webpages

    # loop over the ebay webpages
    for page_number in range(1,int(args.num_pages) +1):
        url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=' 
        url += args.search_term 
        url += '&_sacat=0&_pgn='
        url+= str(page_number)
        url+='&rt=nc'
        print('url=', url)
    
        r = requests.get(url)
        status = r.status_code # 200 means success
        print('status=', status)

        html = r.text

        # process the html
        soup = BeautifulSoup(html, 'html.parser')
        
        # loop over the items in the page
        tags_items = soup.select('.s-item')
        for tag_item in tags_items:

            # name of the item
            tags_name =tag_item.select('.s-item__title')
            name = None
            for tag in tags_name:
                name = tag.text
            #print('name=', name)
            
            # add price here 
            price = None
            tags_price = tag_item.select('.s-item__price')
            for tag in tags_price:
                price = parse_price(tag.text)
            #print('price=',price)

            # status of item
            tags_status = tag_item.select('.SECONDARY_INFO')
            status = None
            for tag in tags_status:
                status = tag.text
            #print('status=', status)

            
            # add shipping here
            shipping = 0
            tags_shipping = tag_item.select('.s-item__shipping')
            for tag in tags_shipping:
                shipping = parse_shipping(tag.text)
            #print('shipping=',shipping)
            
        
            # whether the item has free returns
            freereturns = False
            tags_freereturns = tag_item.select('.s-item__free-returns')
            for tag in tags_freereturns:
                freereturns = True 
            #print('freereturns=',freereturns)
            
            # how many items were sold
            #.s-item__additionalItemHotness (is this necessary???????????????)
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

    # write the json to a file 
    
    if args.csv == 'csv': # use a for loop to write this 
        filename = args.search_term+ '.csv'
        outputFile = open(filename, 'w', newline='')
        outputWriter = csv.writer(outputFile)
        #outputFile = outputWriter.writerow(['name', 'free_returns', 'items_sold', 'status', 'shipping', 'price'])
        #for variable in item:
            #outputWriter.writerow([name, freereturns, items_sold, status, shipping, price])
        #outputFile.close()
    else:
        filename = args.search_term+ '.json'
        with open(filename, 'w', encoding='ascii') as f:
            f.write(json.dumps(items))