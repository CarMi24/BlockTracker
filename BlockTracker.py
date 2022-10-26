import requests
import json


#Initiate global variables of genesis and latest blocks data
gen_response = requests.get(f'https://blockchain.info/block-height/1?format=json')
genesis_timestamp = gen_response.json()['blocks'][0]['time']
response = requests.get('https://blockchain.info/latestblock')
latest_block = response.json()['height']


#Gets a wanted timestamp from user
def get_timestamp():
    timestamp = int(input("Please set TS: \n"))
    return timestamp

#Returns the timestamp of a block in index @height
def get_block_timestamp(height):
    while True:
        
        response = requests.get(f'https://blockchain.info/block-height/{height}?format=json')
        if (response.status_code == 200):
            break
    obj = response.json()
    timestamp = obj['blocks'][0]['time']
    return timestamp

#Approximates a better initiate range for search based on average block creation
#If approximation fails, sets the range for (genesis,latest)
def init_range_of_search(timestamp):
    low = int((timestamp - genesis_timestamp)/(10.5*60))
    high = int((timestamp - genesis_timestamp)/(9.5*60))
    if(get_block_timestamp(low) > timestamp):
        low = 1
    if(get_block_timestamp(high) < timestamp):
        high = latest_block
    print(f'starting search in range of blocks: ({low},{high})')
    return (low,high)


#Searches for N given a timestamp.
#O(log n) , as n = number of blocks
def search_time_height(timestamp):
    
    low,high =init_range_of_search(timestamp)
    high = min(high, latest_block)
    mid = (high+low)//2
    counter = 0
    while(high >= low):
        mid = (high+low)//2
        #print(f"mid is: {mid}")
        current_ts = get_block_timestamp(mid)
        counter += 1
        if(current_ts >= timestamp):
            high = mid - 1
        else:
            low = mid + 1
        
    print(f'num of API calls: {counter}')
    N = mid if current_ts < timestamp else mid-1
    return N


def home_challenge_1():
    timestamp = get_timestamp()
    print(f'N is: {search_time_height(timestamp)}')

home_challenge_1()

            