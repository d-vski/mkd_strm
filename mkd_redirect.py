import requests
from bs4 import BeautifulSoup
import json
from flask import Flask, redirect, request, Response

def get_m3u8_link(url_path):
    url = url_path
    selector_path = "#my-stage-ctn > div > script:nth-child(11)"

    r = requests.get(url)

    # Example log statements:
    print("Starting get_m3u8_link() function...")
    print(f"Received parameter value: {url}")

    r.content
    r.status_code

    soup = BeautifulSoup(r.content, "html.parser")

    script_element = soup.select_one(selector_path)

    if script_element:
        script_content = script_element.string
        start_index = script_content.find("[[{")
        if start_index != -1:
            end_index = script_content.find("}]]", start_index) + 3
            if end_index != -1:
                json_data = script_content[start_index:end_index]
                json_object = json.loads(json_data)[0]
            else:
                print("End index not found.")
        else:
            print("Start index not found.")
    else:
        print("Script element not found.")

    mrt_sat_1_xmpeg = json_object[0]['src']
    mrt_sat_1_rtmp = json_object[1]['src']

    print(mrt_sat_1_xmpeg + "\n" + mrt_sat_1_rtmp + "\n")

    return mrt_sat_1_xmpeg

def get_m3u8_link_stanici(url_path):
    headers = {
        "User-Agent": "curl/7.68.0",
        "Accept": "*/*",
    }
    r = requests.get(url_path, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")
    video_element = soup.select_one("video")

    if video_element:
        source_value = video_element.get('src')
        if source_value:
            print(source_value)
            return source_value
        else:
            print("No 'src' attribute found in the <video> element.")
    else:
        error_message = "Video element not found. " + r.text
        print(error_message)

    return None  


app = Flask(__name__)

@app.route('/')
def redirect_to_new_m3u8():
    # Get the 'param_name' parameter from the URL, if it exists
    url_path = request.args.get('param_name')

    if url_path:
        if url_path.startswith("https://tvstanici.net/"):
            new_m3u8_url = get_m3u8_link_stanici(url_path)
        elif url_path.startswith("https://play.mrt.com.mk/live/"):
            new_m3u8_url = get_m3u8_link(url_path)
        else:
            return "URL path not recognized.", 400  # Return a 400 Bad Request if the URL is not recognized

        # Redirect to the new m3u8 URL
        return redirect(new_m3u8_url, code=302)
    else:
        # If no parameter is provided, read and return the contents of channels.m3u
        try:
            with open('channels.m3u', 'r') as file:
                channels_content = file.read()
            return Response(channels_content, mimetype='text/plain')
        except FileNotFoundError:
            return "channels.m3u file not found.", 404  # Return a 404 Not Found if the file does not exist

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
