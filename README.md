# Sidious

![Build](https://github.com/austinhrdt/sidious/workflows/Build/badge.svg)

## Description

Darth Sidious discord bot. To add it to your discord server, refer [this link](https://discordapp.com/oauth2/authorize?client_id=673260587710545928&scope=bot&permissions=19926016).

![Sheev](media/sidious.JPG)

## Usage

Admins may send `!execute 66` into a text channel (any text channel) and the bot will then disconnect all active users from all voice channels. That's it.

## Toolkit

This bot was built using [discord.py](https://github.com/Rapptz/discord.py). It is containerized and deployed on AWS Fargate via GitHub Actions workflow, based on [this blogpost](https://aws.amazon.com/blogs/opensource/github-actions-aws-fargate/)
