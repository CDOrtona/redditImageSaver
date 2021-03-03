import requests
import json
import os


def main():
    subreddit = input("enter the subreddit name: ")
    index = input("enter how many images to retrieve")
    display_option = input("enter the display option")
    url = "https://www.reddit.com/r/" + subreddit.lower() + "/" + display_option.lower() + ".json?limit=" + index
    session = requests.session()
    response = session.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    binary = response.content
    json_format = json.loads(binary)
    info_list = []
    my_set = {'author', 'url', 'title', 'id'}
    for x in range(int(index)):
        if my_set.issubset(json_format['data']['children'][x]['data'].keys()):
            info_list.clear()
            info_list.append(json_format['data']['children'][x]['data']['title'])
            info_list.append(json_format['data']['children'][x]['data']['author'])
            info_list.append(json_format['data']['children'][x]['data']['id'])
            # if there's not post_hint then it's a txt
            # post_int can indicate a video, image or link
            if 'post_hint' in json_format['data']['children'][x]['data']:
                post_hint = json_format['data']['children'][x]['data']['post_hint']
                # image case
                print(f'Type of post: {post_hint}')
                if post_hint.__eq__('image'):
                    response = session.get(json_format['data']['children'][x]['data']['url'],
                                           headers={'User_Agent': 'Mozilla/5.0'})
                    img = response.content
                    save(subreddit, info_list, img)
            else:
                print('Media ignored as it\'s not an image')
        else:
            print("unexpected error")
            main()


# info --> [title, author, id]
def save(subreddit, info, file):
    # title = info[0]
    author = info[1]
    file_id = info[2]
    base_path = os.getcwd()
    dir_path = base_path + '/' + subreddit
    if os.path.isdir(dir_path):
        pass
    else:
        os.mkdir(dir_path)
    # this checks if the folder with the name of the author exists or not
    if not os.path.isdir(dir_path + '/' + author):
        # this creates the folder with author's name when if condition is true
        os.mkdir(dir_path + '/' + author)
        # this checks if an image with the same title is already in the folder
        if not os.path.isfile(dir_path + '/' + author + '/' + file_id + '.jpg'):
            with open(dir_path + '/' + author + '/' + file_id + '.jpg', 'wb') as f:
                f.write(file)
        else:
            # ignore the writing of the file if it's present in the folder already
            print('file already in folder, skipped...')
            pass
    else:
        if not os.path.isfile(dir_path + '/' + author + '/' + file_id + '.jpg'):
            with open(dir_path + '/' + author + '/' + file_id + '.jpg', 'wb') as f:
                f.write(file)
        else:
            # ignore the writing of the file if it's present in the folder already
            print('file already in folder, skipped...')
            pass


if __name__ == "__main__":
    main()
else:
    exit()
