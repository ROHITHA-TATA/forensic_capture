# ForensicCapture - Social Media Evidence Tool

A comprehensive desktop application for automated extraction and documentation of social media evidence for investigative and forensic purposes.

## Features

- **Multi-Platform Support**: Reddit, Mastodon, Facebook, Instagram, and more
- **Public Profile Extraction**: Extract data without requiring authentication
- **Hashtag/Subreddit Analysis**: Capture posts from specific hashtags or subreddit communities
- **Optimized Screenshot Capture**: Strategic screenshot capture system (1-2 profile + 4 post screenshots)
- **PDF Report Generation**: Comprehensive PDF reports with metadata and evidence
- **Batch Processing**: Handle multiple extractions efficiently
- **User-friendly GUI**: Intuitive interface with progress tracking
- **Local Processing**: All data processed and stored locally for security

## Requirements

- **Python 3.8 or higher**
- **Google Chrome browser** (latest version recommended)
- **Windows 10 or higher**
- **Internet connection** for web scraping
- **4GB RAM minimum** (8GB recommended for large extractions)

## Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/ForensicCapture.git
cd ForensicCapture
```

### Step 2: Set Up Python Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
.\venv\Scripts\activate

# On Linux/Mac:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Verify ChromeDriver
The application includes ChromeDriver in the `drivers/` folder. If you encounter issues:
- Ensure Chrome browser is installed and updated
- Check that ChromeDriver version matches your Chrome version

## Getting Started - First Time Users

### Quick Start Guide

1. **Launch the Application**:
```bash
python windows-app/main.py
```

2. **Select Platform**: Choose from Reddit, Mastodon, Facebook, or Instagram

3. **Choose Extraction Type**:
   - **Public Profile**: Extract user profile and posts
   - **Hashtag/Subreddit**: Extract posts from specific communities

4. **Configure Options**:
   - ✅ **Save as PDF Report**: Enable for comprehensive PDF documentation
   - Enter target username, hashtag, or subreddit name
   - Select instance (for Mastodon)

5. **Start Extraction**: Click "Extract Data" and monitor progress

6. **Review Results**: Find generated reports in `windows-app/reports/` directory

## Usage Examples

### Reddit Extraction
```bash
# Example: Extract public profile
Username: some_reddit_user
Platform: Reddit
Type: Public Profile
✅ Save as PDF Report
```

### Mastodon Extraction
```bash
# Example: Extract hashtag posts
Hashtag: climate
Instance: mastodon.social
Platform: Mastodon
✅ Save as PDF Report
```

## Output Structure

After extraction, you'll find organized files in:

```
windows-app/
├── screenshots/
│   ├── reddit/          # Reddit screenshots
│   ├── mastodon/        # Mastodon screenshots
│   └── [platform]/      # Other platform screenshots
├── data/
│   ├── reddit/          # JSON metadata files
│   ├── mastodon/        # JSON metadata files
│   └── [platform]/      # Other platform metadata
├── reports/
│   └── [timestamp]_report.pdf  # Generated PDF reports
└── logs/
    └── [platform]_[timestamp].log  # Extraction logs
```

## PDF Report Features

When "Save as PDF Report" is enabled, the application generates comprehensive reports containing:

- **Cover page** with extraction metadata
- **Screenshots** (optimized 4-screenshot strategy per target)
- **Data summary** and extraction details
- **Timestamp** and authenticity information
- **Organized layout** for professional documentation

## Advanced Features

### Screenshot Optimization
- **Strategic Capture**: 1-2 profile screenshots + 4 post screenshots maximum
- **Overlap Prevention**: 80% scroll increments to capture unique content
- **Efficient Processing**: Reduced redundancy for faster extractions

### Platform-Specific Capabilities

**Reddit**:
- Public profiles and subreddit extraction
- Post content and metadata capture
- Community analysis

**Mastodon**:
- Decentralized instance support
- Hashtag trending analysis
- Public timeline extraction

**Facebook & Instagram**:
- Public profile data extraction
- Post and story capture
- Metadata preservation

## Security Notes

- Credentials are stored only in memory during the session
- All data is processed locally
- Screenshots and reports are saved locally

## Legal Disclaimer

This tool is intended for use by authorized personnel only. Users are responsible for ensuring compliance with:
- Applicable laws and regulations
- Platform terms of service
- Privacy laws and data protection regulations

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


