from __future__ import unicode_literals
import argparse
import os
import yt_dlp
from openai import OpenAI
import json

chunk_prompt = """
You are a helpful AI assistant who is tasked with helping the user group a video transcript
into segments based on the topics discussed. The user will provide you a transcript in VTT format
and you need to read it, group it into segments and provide the start, end and title for each segment.
You must return the data in JSON format as follows:


{
    "segments": [
        {
            "start": "00:00:00",
            "end": "00:01:00",
            "title": "OpenAI's new chat model GPT-4o"
        },
        {
            "start": "00:01:00",
            "end": "00:02:00",
            "title": "Why Wendys is the best place to eat"
        },
        ...
    ]
}
"""

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

def download_to_mp3(video_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(video_url)
        info = ydl.sanitize_info(result)
        filename = info['requested_downloads'][0]['filepath']

    return filename

def create_transcript_from_mp3(mp3_file):
    print(f"Transcribing {mp3_file}")
    output_filename = mp3_file + ".vtt"
    if os.path.exists(output_filename):
        print(f"Transcript already exists at {output_filename} - skipping transcription")
        return output_filename
    mp3 = open(mp3_file, "rb")
    client = OpenAI()
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=mp3,
        response_format="vtt"
    )
    mp3.close()
    with open(output_filename, "w") as f:
        f.write(transcription)
    return output_filename

def create_youtube_segments(vtt_file):
    print(f"Creating segments for {vtt_file}")
    segments_file = vtt_file + ".txt"
    if os.path.exists(segments_file):
        print(f"Segments already exist at {segments_file} - skipping segment creation")
        return segments_file
    client = OpenAI()
    with open(vtt_file, "r") as f:
        lines = f.readlines()
    # chunk lines into chunked_lines of upto 200 lines each
    chunked_lines = [lines[i:i+200] for i in range(0, len(lines), 200)]
    # for each chunked_lines, create segments by making a call to openai chat model gpt-4o
    segments = []
    for chunk in chunked_lines:
        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={ "type": "json_object" },
            messages = [
                {
                    "role": "system",
                    "content": chunk_prompt
                },
                {
                    "role": "user",
                    "content": "".join(chunk)
                }
            ]
        )
        segments.append(response.choices[0].message.content)

    consolidated_data = {"segments": []}
    for json_str in segments:
        data = json.loads(json_str)
        if "segments" in data:
            consolidated_data["segments"].extend(data["segments"])

    with open(segments_file, "w") as f:
        f.write(json.dumps(consolidated_data, indent=4))
    return segments_file

def main(video_url):
    filename = download_to_mp3(video_url)
    transcript = create_transcript_from_mp3(filename)
    grouped_transcript = create_youtube_segments(transcript)
    print(f"Chunked transcript saved as : {grouped_transcript}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get timestamp transcript & timecodes from YouTube video")
    parser.add_argument("url", help="URL of the YouTube video")
    args = parser.parse_args()
    main(args.url)
