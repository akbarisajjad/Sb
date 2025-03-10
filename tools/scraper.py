import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string if soup.title else 'عنوانی یافت نشد'
            return f"عنوان صفحه: {title}"
        else:
            return "خطا در دریافت اطلاعات از سایت."
    except Exception as e:
        return f"خطا: {e}"
