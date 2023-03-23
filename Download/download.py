"""
Program to download and write files to disk

"""
import requests

def download(url):
    # Get the URL
    get_request = requests.get(url)
    file_name = url.split('/')
    # Name file as last element in list, so the file name
    with open(file_name[-1], "w") as out_file:
        out_file.write(get_request.content)

    print(get_request.content)

download('https://i.guim.co.uk/img/media/26392d05302e02f7bf4eb143bb84c8097d09144b/446_167_3683_2210/master/3683.jpg?width=620&quality=45&dpr=2&s=none')