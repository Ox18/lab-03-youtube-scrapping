import requests

url_youtube = "https://www.youtube.com/results?search_query=datos"

response = requests.get(url_youtube)

## save in HTML
with open("youtube.html", "w") as file:
    file.write(response.text)

## extract <script nonce="PxF2efLUBVaVA-B9JWSG3w">
    #   var ytInitialData = {
    #     responseContext: {
# the content of the script tag only content from ytInitialData with regex

import re
import json

pattern = r"var ytInitialData = ({.*?});"

match = re.search(pattern, response.text)

if match:
    data = match.group(1)
    ### save in json
    with open("youtube.json", "w") as file:
        file.write(data)

    ## get data.content.twoColumnSearchResultsRenderer.primaryContents.sectionListRenderer.contents
    data = json.loads(data)

    contents = data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"]

    ## save in json contents
    with open("youtube_contents.json", "w") as file:
        json.dump(contents, file, indent=4)

    items_list = []

    ## recorre contents
    for content in contents:
        ## get data

        if "videoRenderer" not in content:
            continue

        data = content["videoRenderer"]
        ## save in json
        title = data["title"]["runs"][0]["text"]
        image_url = data["thumbnail"]["thumbnails"][-1]["url"]
        video_url = "https://www.youtube.com/watch?v=" + data["videoId"]
        channel_name = data["ownerText"]["runs"][0]["text"]
        channel_name_id = data["ownerText"]["runs"][0]["navigationEndpoint"]["browseEndpoint"]["browseId"]
        vistas = data["viewCountText"]["simpleText"]
        tiempo = data["lengthText"]["simpleText"]


        items_list.append({
            "title": title,
            "image_url": image_url,
            "video_url": video_url,
            "channel_name": channel_name,
            "channel_name_id": channel_name_id,
            "vistas": vistas,
            "tiempo": tiempo
        })
        
    ## save in json items_list
    with open("youtube_items.json", "w") as file:
        json.dump(items_list, file, indent=4)




