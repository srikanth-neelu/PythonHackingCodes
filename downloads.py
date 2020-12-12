import requests

def download(url):
    get_response=requests.get(url)
    # print(get_response)
    # print(get_response.content)
    filename=url.split("/")[-1]
    with open(filename,"wb") as out_file:
        out_file.write(get_response.content)


download("https://image.shutterstock.com/image-photo/image-front-sports-car-scene-260nw-566330083.jpg")
