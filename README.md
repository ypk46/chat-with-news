# Chat with News

## Overview

**Chat with News** is an application that fetches news articles from RSS feeds and generates summaries using a Large Language Model (LLM). The app also embeds the entire article content, allowing users to interact with the news using natural language.

## Features

- Fetch news articles from various RSS feeds.
- Generate concise summaries of news articles using an LLM.
- Embed full article content for interactive "chatting" with the news.
- Use natural language to ask questions and get information from news articles.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ypk46/chat-with-news.git
   ```
2. Navigate to the project directory:
   ```bash
   cd chat-with-news
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

The application has a CLI tool with a couple commands to handle the news fetching and embeddings. It relies on `pgai` extension along with `pgVectorizer` to automatically embed the news that get inserted.

1. Add a RSS feed:
   ```bash
   python -m app feed add
   ```
2. List all RSS feeds:
   ```bash
   python -m app feed list
   ```
3. Fetch news and create summaries:
   ```bash
   python -m app feed fetch
   ```
4. Generate embeddings using `pgVectorizer`:
   ```bash
   python -m app vectorize
   ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
