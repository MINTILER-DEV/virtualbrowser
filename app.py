from flask import Flask, request, send_file
import subprocess
import os
import random

app = Flask(__name__)

def get_random_proxy():
    # Read the proxies from http.txt
    with open('http.txt', 'r') as file:
        proxies = file.read().splitlines()
    
    # Return a random proxy
    return random.choice(proxies)

@app.route('/download')
def download():
    # Get the video URL from the query parameters
    video_url = request.args.get('url')
    if not video_url:
        return 'URL is required', 400

    # Set the output file path
    output_file = 'video.mp4'

    # Get a random proxy
    proxy = get_random_proxy()
    # print(f"Using proxy: http://{proxy}")  # Log the proxy being used

    try:
        # Download the video using yt-dlp with a random proxy
        subprocess.run([
            'yt-dlp',
            #'--proxy', f"http://{proxy}",  # Use the random proxy
            '-o', output_file,
            video_url
        ], check=True)

        # Send the video file as a response
        return send_file(output_file, as_attachment=True)
    except subprocess.CalledProcessError as e:
        return f'Error: {str(e)}', 500
    finally:
        # Clean up the file after sending
        if os.path.exists(output_file):
            os.remove(output_file)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)