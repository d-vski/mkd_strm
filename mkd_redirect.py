import requests
from bs4 import BeautifulSoup
import json
from flask import Flask, redirect

def get_m3u8_link(url_path):
    url = url_path

    r = requests.get(url)

    print("Download about to start")

    r.content
    r.status_code

    soup = BeautifulSoup(r.content, "html.parser")

    # Define the CSS selector path to find the script element
    selector_path = "#my-stage-ctn > div > script:nth-child(11)"

    # Use BeautifulSoup's select() method to find the script element
    script_element = soup.select_one(selector_path)

    # Check if the script element exists before proceeding
    if script_element:
        # Extract the script content
        script_content = script_element.string

        # Extract the JSON portion from the script content
        start_index = script_content.find("[[{")  # Find the start of the JSON array

        # Check if the start index is found before proceeding
        if start_index != -1:
            end_index = script_content.find("}]]", start_index) + 3  # Find the end of the JSON array

            # Check if the end index is found before proceeding
            if end_index != -1:
                json_data = script_content[start_index:end_index]

                # Load the JSON data using json.loads()
                json_object = json.loads(json_data)[0]

                # Now you can work with the extracted JSON object
            else:
                print("End index not found.")
        else:
            print("Start index not found.")
    else:
        print("Script element not found.")

    json_object

    mrt_sat_1_xmpeg = json_object[0]['src']
    mrt_sat_1_rtmp = json_object[1]['src']

    print(mrt_sat_1_xmpeg + "\n" + mrt_sat_1_rtmp + "\n")

    return mrt_sat_1_xmpeg


app = Flask(__name__)

@app.route('/')

def redirect_to_new_m3u8():
    # Get the 'param_name' parameter from the URL, if it exists
    url_path = request.args.get('param_name')

    # Call your function with the parameter value

    # Call your function to get the new m3u8 URL with the auth token
    new_m3u8_url = get_m3u8_link(url_path)

    # Redirect to the new m3u8 URL
    return redirect(new_m3u8_url, code=302)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
