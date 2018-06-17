from pprint import pprint
import requests
import urllib3


def get_token():
    with open('token.txt') as f:
        return f.read()


def get_common_friends_list(token, uids):
    target_uids = ','.join(map(str, uids[1:]))
    source_uid = str(uids[0])

    params = {'access_token': token,
              'source_uid': source_uid,
              'target_uids': target_uids,
              'v': '5.78'}
    response = requests.get('https://api.vk.com/method/friends.getMutual',
                            params,
                            verify=False)
    friends_list = []
    for common_friend_info in response.json()['response']:
        friends_list.append(set(common_friend_info['common_friends']))
    friends_set = friends_list[0]
    for friends in friends_list[1:]:
        friends_set &= friends
    return list(friends_set)


def get_common_friends_list_detailed(token, uids):
    friends_list = get_common_friends_list(token, uids)
    prefix = 'https://vk.com/'
    uids = ','.join(map(str, friends_list))

    params = {'access_token': token,
              'user_ids': uids,
              'fields': 'domain',
              'v': '5.78'}
    response = requests.get('https://api.vk.com/method/users.get',
                            params,
                            verify=False)
    common_friends = response.json()['response']
    for el in common_friends:
        el['page'] = prefix + el['domain']
    return common_friends


if __name__ == '__main__':
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # иначе антивирус Касперского мешает
    TOKEN = get_token()
    uids = [7677533, 114266546, 24529523]
    common_friends = get_common_friends_list_detailed(TOKEN, uids)
    pprint(common_friends)
