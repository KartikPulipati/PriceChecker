import json
import requests
from django.shortcuts import render
import requests

def home(request):
    return render(request, 'check/home.html')

def results(request):

    keyword = request.GET.get('searchBox')

    # Walmart
    params = {
    'api_key': '${{ secrets.WAL_KEY }}',
    'type': 'search',
    'search_term': keyword,
    'sort_by': 'best_match'
    }
    api_result = requests.get('https://api.bluecartapi.com/request', params)
    data = api_result.json()
    title = data['search_results'][0]['product']['title'][:100]
    link = data['search_results'][0]['product']['link']
    # image = data['search_results'][0]['product']['images']["primary_image"]
    in_stock = data['search_results'][0]['inventory']['in_stock']
    price = data['search_results'][0]['offers']['primary']['price']


    params_amazon = {
        'api_key': '${{ secrets.AM_KEY }}',
        'type': 'search',
        'amazon_domain': 'amazon.com',
        'search_term': keyword,
        'sort_by': 'featured'
    }
    api_result_amazon = requests.get('https://api.rainforestapi.com/request', params_amazon)
    data_amazon = api_result_amazon.json()
    amazon_title = data_amazon['search_results'][0]['title'][:100]
    amazon_link = data_amazon['search_results'][0]['link']
    # amazon_image = data_amazon['search_results'][0]['image']
    amazon_price = data_amazon['search_results'][0]["price"]["raw"]


    #Target
    url = "https://target-com-store-product-reviews-locations-data.p.rapidapi.com/product/search"

    querystring = {"store_id": "3991", "keyword": keyword, "sponsored": "1", "limit": "1", "offset": "0"}

    headers = {
        'x-rapidapi-key': "${{ secrets.TAR_KEY }}",
        'x-rapidapi-host': "target-com-store-product-reviews-locations-data.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    data_target = response.json()
    title_target = data_target['products'][0]['title']
    url = 'https://www.target.com' + data_target['products'][0]['url']
    target_price = data_target['products'][0]['price']['formatted_current_price']

    print(response.text)
    return render(request, 'check/result.html', {'wal_title': title, 'wal_link': link, 'wal_in_stock': in_stock, 'wal_price': price,'amazon_title': amazon_title,'amazon_link':amazon_link,'amazon_price':amazon_price,'target_title':title_target, 'url':url, 'target_price': target_price,})
