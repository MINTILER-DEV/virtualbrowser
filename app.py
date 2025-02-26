from flask import Flask, request, send_file
import subprocess
import os

app = Flask(__name__)

@app.route('/download')
def download():
    # Get the video URL from the query parameters
    video_url = request.args.get('url')
    if not video_url:
        return 'URL is required', 400

    # Set the output file path
    output_file = 'video.mp4'

    try:
        # Download the video using yt-dlp
        subprocess.run(['yt-dlp', '-o', output_file, video_url], check=True)

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