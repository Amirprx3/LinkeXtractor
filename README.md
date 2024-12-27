# Link Extractor Tool

![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.x-green)
![Selenium](https://img.shields.io/badge/dependency-Selenium-orange)

## Overview

The **Link Extractor Tool** is a Python-based web scraping utility that extracts all links (relative and absolute) from a webpage and its associated JavaScript files. It is designed for developers and researchers who need to analyze links or URLs embedded in websites.

## Features

- Extracts links from:
  - Webpage HTML
  - External JavaScript files
- Supports multiple browsers (Firefox, Chrome, Edge)
- Efficient multithreading for downloading and processing script files
- Saves results in a text file named after the website domain
- Simple and intuitive CLI interface

## Requirements

- Python 3.7 or higher
- Selenium
- Requests
- A compatible WebDriver for your browser:
  - [Geckodriver](https://github.com/mozilla/geckodriver) for Firefox
  - [Chromedriver](https://chromedriver.chromium.org/) for Chrome
  - [Edgedriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/) for Edge

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Amirprx3/LinkeXtractor.git
    cd LinkeXtractor
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Download the WebDriver for your preferred browser and add it to your system's PATH.

## Usage

1. Run the script:
    ```bash
    python LinkeXtractor.py
    ```

2. Select a browser:
    - firefox
    - chrome
    - edge

3. Enter one or more website URLs to process. Type `exit` when done.

4. Extracted links will be saved in a text file named after the website's domain. For example:
    - Input: `https://example.com`
    - Output: `example.com.txt`

## Example

**Input:**
```
Enter the browser to use (firefox, chrome, edge): firefox
Enter the website URL (or type 'exit' to quit): https://example.com 
Enter the website URL (or type 'exit' to quit): exit
```


**Output:**
- `example.com.txt`:



## Customization

- **Change Link Regex**: Modify the `regex` variable in `collect_links` to customize the type of links extracted.
- **Set Max Threads**: Adjust `max_workers` in the `ThreadPoolExecutor` for optimal performance based on your system.

## Known Issues

- Websites with complex JavaScript-based navigation (e.g., SPAs) may not load all links.
- Some links might not be accessible due to restrictions like CORS policies or CAPTCHA.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

Developed by [Amirprx3](https://github.com/Amirprx3).
