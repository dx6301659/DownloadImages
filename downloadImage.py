import requests
from bs4 import BeautifulSoup
import os

def get_html_content(url):
    response = requests.get(url)
    # response.rAIse_for_status()
    return response.text

def extract_image_urls(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    img_tags = soup.find_all('img')
    urls = [img['src'] for img in img_tags if 'src' in img.attrs]
    return urls

def format_and_filter_urls(base_url, urls):
    formatted_urls = []
    for url in urls:
        # if url.startswith('//'):
        #     url = 'http:' + url
        # elif url.startswith('/'):
        #     url = base_url + url

        if not url.startswith('http'):
            continue

        if url.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')):
            formatted_urls.append(url)

    return formatted_urls

def download_images(urls, path='./images'):
    if not os.path.exists(path):
        os.makedirs(path)

    for url in urls:
        print(f"Downloading {url} images to '{path}'")
        filename = url.split('/')[-1]
        # # with requests.get(url, stream=True) as r:
        # with requests.get(url) as r:
        #     with open(os.path.join(path, filename), 'wb') as f:
        #         # shutil.copyfileobj(r.raw, f)
        #         f.write(r.content)
        with requests.get(url) as r:
            with open(os.path.join(path, filename), 'wb') as f:
                f.write(r.content)
                f.flush()

def main(url, path='./images'):
    html_content = get_html_content(url)
    urls = extract_image_urls(html_content)
    formatted_urls = format_and_filter_urls(url, urls)
    download_images(formatted_urls, path)
    print(f"Downloaded {len(formatted_urls)} images to '{path}'")

main('https://www.pexels.com/zh-cn/', 'D:/Pic')