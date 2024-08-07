# YouTube to Blog Generator

## Overview

The **YouTube to Blog Generator** is a Python and Django application that converts YouTube videos into blog articles. Users can submit a YouTube link, and the application will:

1. Download the video's audio using `yt-dlp`.
2. Extract the transcript from the audio with AssemblyAI.
3. Generate a blog post from the transcript using the OpenAI API.
4. Display the generated blog article to the user.

User authentication is included to manage access.

## Features

- **YouTube Video to Audio:** Download audio from YouTube videos.
- **Transcript Extraction:** Convert audio to text.
- **Blog Generation:** Create blog articles from transcripts.
- **User Authentication:** Register and log in to access the features.

## Technologies Used

- **Python:** Programming language
- **Django:** Web framework
- **yt-dlp:** YouTube video downloader
- **AssemblyAI:** Speech-to-text service
- **OpenAI:** Natural language processing

## Installation

### Prerequisites

- Python 3.x
- `yt-dlp`
- AssemblyAI API key
- OpenAI API key

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Manuka-Rathnayake/BlogGenAi.git
   cd BlogGenAi
2. **Create a Virtual Environment**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
3. **Install Dependencies**
   ```
   pip install -r requirements.txt

4. **Configure Environment Variables**

   Create a .env file in the root directory of the project and add the following:
   ```
   ASSEMBLYAI_API_KEY=your_assemblyai_api_key
   OPENAI_API_KEY=your_openai_api_key
5. **Apply Migrations**
   ```
   python manage.py migrate

6. **Start the Development Server**
   ```
   python manage.py runserver

