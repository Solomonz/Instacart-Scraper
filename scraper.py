#! /usr/bin/env python

from sys import argv
from bs4 import BeautifulSoup


def convert_price_to_integer_cents(price):
    return int(price[1:-3] + price[-2:])


def convert_integer_cents_to_price(cents):
    price = str(cents)
    return price[:-2] + '.' + price[-2:]



def get_item_name(item):
    return item.find(class_='item-name').contents[0].strip()


def get_item_price(item):
    price = item.find(class_='item-price').find_all(class_='total')[-1].text.strip()
    return convert_price_to_integer_cents(price)

def main():
    receipt_html_file_path = argv[1]
    # receipt_html_file_path = 'C:/Users/solom/Downloads/receipt.html'
    with open(receipt_html_file_path, 'r') as receipt_html_file:
        receipt_html = '\n'.join(receipt_html_file)
    
    soup = BeautifulSoup(receipt_html, 'html.parser')
    delivered_items = soup.find_all('div', class_='item-delivered')
    items = list(map(lambda item: (get_item_name(item), get_item_price(item)), delivered_items))
    expected_subtotal = soup.find(string='Items Subtotal').parent.parent.find(class_='amount').text.strip()
    expected_subtotal = convert_price_to_integer_cents(expected_subtotal)
    observed_subtotal = sum(map(lambda item: item[1], items))
    if not (expected_subtotal == observed_subtotal):
        print(f'ERROR: observed subtotal of {observed_subtotal} does not match expected subtotal of {expected_subtotal}.')
    
    for item in items:
        print(f'{item[0]};{convert_integer_cents_to_price(item[1])}')




if __name__ == "__main__":
    main()