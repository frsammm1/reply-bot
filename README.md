# Telegram Message Relay Bot

A simple Telegram bot that relays messages between users and the bot owner (Sam).

## Features

- 📨 Forwards all user messages to the owner with sender details
- 💬 Owner can reply by responding to forwarded messages
- 🎯 Supports text, photos, videos, documents, voice messages, and more
- 🔒 Private communication channel

## How It Works

1. **Users**: Send messages to the bot, which are forwarded to Sam
2. **Owner (Sam)**: Receives messages with sender info and replies by responding to them
3. **Bot**: Relays replies back to the original senders

## Environment Variables

Set these on Render:

- `BOT_TOKEN`: Your Telegram bot token
- `OWNER_ID`: Your Telegram user ID

## Deploy on Render

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set environment variables
4. Deploy!

## Setup

Bot token: `8542488824:AAEp6mN_yK9UMFmHcPnPUVTK-KwvZro-Rc8`
Owner ID: `8242974141`
