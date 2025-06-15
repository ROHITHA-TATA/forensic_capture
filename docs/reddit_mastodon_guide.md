# Using Reddit and Mastodon in ForensicCapture

This guide explains how to use the newly added Reddit and Mastodon capabilities in ForensicCapture.

## Overview

Both Reddit and Mastodon platforms have been integrated to allow capturing public profiles and posts without requiring authentication. This is ideal for demonstrations and forensic evidence collection from public sources.

## Reddit Usage

Reddit is a popular social news aggregation platform with millions of users and thousands of communities (subreddits).

### Capturing Reddit User Profiles

1. Launch the ForensicCapture application
2. Select "Reddit" from the platform dropdown
3. Select "Public Profile" option (only public access is supported)
4. Enter a Reddit username (without the u/ prefix) in the "Profile ID/Username" field
   - For example: `spez`, `GovSchwarzenegger`, `AutoModerator`
5. Select "User Profile" or "User Posts" from the data type dropdown
6. Click "Extract Data"

### Capturing Reddit Subreddits

1. Launch the ForensicCapture application
2. Select "Reddit" from the platform dropdown
3. Select "Public Profile" option
4. Enter a subreddit name (without the r/ prefix) in the "Profile ID/Username" field
   - For example: `news`, `programming`, `science`
5. Select "Subreddit" from the data type dropdown
6. Click "Extract Data"

## Mastodon Usage

Mastodon is a decentralized, open-source social media platform that works similarly to Twitter.

### Capturing Mastodon User Profiles

1. Launch the ForensicCapture application
2. Select "Mastodon" from the platform dropdown
3. Select "Public Profile" option (only public access is supported)
4. Enter a Mastodon username in the "Profile ID/Username" field
   - For example: `Gargron`, `journa`, `EU_Commission`
   - Include the @ symbol if desired (e.g., `@Gargron` or just `Gargron`)
5. Select "User Profile" or "User Posts" from the data type dropdown
6. Click "Extract Data"

### Capturing Mastodon Hashtags

1. Launch the ForensicCapture application
2. Select "Mastodon" from the platform dropdown
3. Select "Public Profile" option
4. Enter a hashtag in the "Profile ID/Username" field
   - For example: `technology`, `art`, `photography`
   - Include the # symbol if desired (e.g., `#technology` or just `technology`)
5. Select "Hashtag" from the data type dropdown
6. Click "Extract Data"

## Tips for Successful Capture

1. **Popular Accounts**: Choose popular, active accounts for the best demonstration results
2. **Public Content**: Ensure you're only accessing publicly available content
3. **Processing Time**: Allow a few seconds for the browser to navigate and capture screenshots
4. **Results**: Screenshots are saved in the `screenshots/reddit` or `screenshots/mastodon` folders
5. **Metadata**: JSON metadata for each extraction is saved in the `data/reddit` or `data/mastodon` folders

## Example Reddit Usernames for Testing

- `spez` - Reddit co-founder and CEO
- `GovSchwarzenegger` - Arnold Schwarzenegger's official account
- `AutoModerator` - Reddit's official bot account
- `reddit` - Official Reddit account

## Example Reddit Subreddits for Testing

- `news` - News and current events
- `programming` - Programming discussions
- `science` - Scientific research and news
- `AskReddit` - Question and answer forum

## Example Mastodon Accounts for Testing

- `Gargron@mastodon.social` - Mastodon creator
- `EU_Commission@social.network.europa.eu` - European Commission
- `mozilla@mozilla.social` - Mozilla Foundation

## Example Mastodon Hashtags for Testing

- `technology`
- `art`
- `photography`
- `science`
