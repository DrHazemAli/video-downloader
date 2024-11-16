# YouTube and Social Media Video Downloader

This Python application provides an easy-to-use GUI for downloading videos and audio from popular platforms such as YouTube, Instagram, TikTok, and Facebook. The downloader allows you to select video quality, extract audio as MP3 or WAV, and download thumbnails.

## Features

- **Video Download**: Download videos from YouTube, Instagram, TikTok, and Facebook.
- **Audio Download**: Extract audio from YouTube videos in MP3 or WAV format.
- **Audio Conversion**: Convert MP3 files to WAV format.
- **Thumbnail Download**: Download thumbnails of YouTube videos.
- **Video Quality Selection**: Choose from multiple video quality options (e.g., highest, 720p, 480p, etc.).
- **Progress Tracking**: Displays a progress bar to track the download progress.

## Prerequisites

- **Python 3.x**: Make sure you have Python installed on your system.
- **Libraries**: The following libraries are required to run this application. You can install them using `pip`:
  
  ```sh
  pip install pytube instaloader yt-dlp requests pydub
  ```
  - `tkinter`: Used for GUI components (pre-installed with Python on most systems).
  - `pytube`: Used for downloading YouTube videos and audio.
  - `instaloader`: Used for downloading Instagram content.
  - `yt-dlp`: Used for downloading videos from platforms like TikTok and Facebook.
  - `requests`: Used for handling HTTP requests (e.g., downloading thumbnails).
  - `pydub`: Required for audio conversion (MP3 to WAV).
  - **ffmpeg**: Required for `pydub` to convert MP3 to WAV. Install via package manager or from [FFmpeg's official website](https://ffmpeg.org/download.html).

## How to Run

1. **Clone the Repository**: Clone this repository to your local machine or download the source code.

   ```sh
   git clone https://github.com/DrHazemAli/video-downloader.git
   cd video-downloader
   ```

2. **Install Dependencies**: Ensure you have all the required Python packages installed using `pip` as mentioned above.

3. **Run the Application**: Run the script using the command:

   ```sh
   python app.py
   ```

4. **Usage**:
   - Enter the URL of the video you want to download.
   - Select your desired options (e.g., Video, Audio, Thumbnail).
   - Choose the video quality from the dropdown.
   - Click the `Download` button to start the download.

## GUI Components

- **URL Entry Field**: Input the URL of the video you want to download.
- **Options**:
  - `Video`: Download the video.
  - `Audio (MP3/WAV)`: Extract and download audio from YouTube videos.
  - `Convert Audio to WAV`: Convert downloaded MP3 audio files to WAV format.
  - `Thumbnail`: Download the thumbnail image of the YouTube video.
  - `Video + Audio`: Download both video and audio tracks.
- **Quality Selection**: Dropdown menu to select video quality (highest, 720p, 480p, etc.).
- **Download Button**: Start the download process.
- **Progress Bar**: Track the progress of the download.
- **Status Label**: Display the status of the download.

## Error Handling

- **Invalid URL**: Displays an error message if the entered URL is not supported.
- **Unavailable Video**: Handles scenarios where a YouTube video is unavailable.
- **Network Issues**: Provides error feedback if there is an issue with the internet connection.
- **General Errors**: Any unexpected error during download will be displayed as an error message.

## Notes

- **Audio Conversion**: Audio conversion to WAV requires the `pydub` library and FFmpeg. Make sure FFmpeg is installed and accessible via your system's PATH.
- **Instagram and TikTok Downloads**: Instagram profile URLs can be downloaded, while TikTok and Facebook videos are handled using `yt-dlp`.

## Dependencies Installation

Make sure to install the dependencies listed in the `requirements.txt` file or manually install them as follows:

```sh
pip install pytube instaloader yt-dlp requests pydub
```

For FFmpeg installation, refer to the [official guide](https://ffmpeg.org/download.html).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is intended for personal use only. Please ensure that you comply with the terms of service of any platform you are downloading content from.

## Acknowledgements

- **pytube** for YouTube video/audio download functionality.
- **instaloader** for Instagram content download.
- **yt-dlp** for extended social media support (TikTok, Facebook, etc.).
- **pydub** for audio conversion capabilities.

## Contribution

Feel free to fork the repository, make improvements, and submit pull requests. All contributions are welcome!

## Repository

This project is hosted on GitHub: [DrHazemAli/video-downloader](https://github.com/DrHazemAli/video-downloader).

