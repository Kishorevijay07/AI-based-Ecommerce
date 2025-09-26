import httpx
from bs4 import BeautifulSoup
import asyncio
import json

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}


async def fetch_page(url):
    """Fetch HTML content of a page (async safe)"""
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(url, headers=HEADERS)
        resp.raise_for_status()
        return resp.text


async def parse_amazon(html):
    """Parse Amazon product page and extract details"""
    soup = BeautifulSoup(html, "html.parser")

    # Title
    title_el = soup.select_one("#productTitle")
    title = title_el.get_text(strip=True) if title_el else None

    # Price
    price = None
    price_selectors = [
        "#priceblock_ourprice",
        "#priceblock_dealprice",
        "#corePrice_feature_div .a-offscreen",
        "span.a-price span.a-offscreen",
        "span[data-a-color='price'] span.a-offscreen",
        "span[data-a-color='base'] span.a-offscreen"
    ]
    for sel in price_selectors:
        el = soup.select_one(sel)
        if el and el.get_text(strip=True):
            price = el.get_text(strip=True)
            break

    # Rating & review count
    rating_el = (soup.select_one("i[data-hook='average-star-rating']") or
                 soup.select_one("span[data-hook='rating-out-of-text']") or
                 soup.select_one(".a-icon-alt"))
    rating = rating_el.get_text(strip=True) if rating_el else None

    review_count_el = soup.select_one("#acrCustomerReviewText")
    review_count = review_count_el.get_text(strip=True) if review_count_el else None

    # Reviews
    reviews = []
    for r in soup.select("div[data-hook='review']"):
        rtitle = r.select_one("a[data-hook='review-title']") or r.select_one("span[data-hook='review-title']")
        rbody = r.select_one("span[data-hook='review-body']")
        rrating = r.select_one("i[data-hook='review-star-rating']") or r.select_one("span.a-icon-alt")
        rdate = r.select_one("span[data-hook='review-date']")
        reviews.append({
            "title": rtitle.get_text(strip=True) if rtitle else None,
            "body": rbody.get_text(strip=True) if rbody else None,
            "rating": rrating.get_text(strip=True) if rrating else None,
            "date": rdate.get_text(strip=True) if rdate else None,
        })

    # About this item
    about_items = []
    for li in soup.select("ul.a-unordered-list.a-vertical.a-spacing-mini li span.a-list-item"):
        text = li.get_text(strip=True)
        if text:
            about_items.append(text)

    # Product Image
    img_el = soup.select_one("#landingImage") or soup.select_one("img[data-old-hires]") or soup.select_one("img.a-dynamic-image")
    image_url = img_el.get("src") if img_el else None

    # Product Details Table
    product_details = {}
    for row in soup.select("table.a-normal tr"):
        th = row.select_one("td span.a-text-bold")
        td = row.select_one("td.a-span9 span")
        if th and td:
            key = th.get_text(strip=True)
            val = td.get_text(strip=True)
            product_details[key] = val

    # Related Product Links
    related_links = []
    for div in soup.select("div[data-asin]"):
        asin = div.get("data-asin")
        if asin and len(asin) > 5:
            link = f"https://www.amazon.in/dp/{asin}"
            if link not in related_links:
                related_links.append(link)

    return {
        "title": title,
        "price": price,
        "rating": rating,
        "review_count": review_count,
        "reviews": reviews,
        "about_items": about_items,
        "image": image_url,
        "product_details": product_details,
        "related_links": related_links[:5]  # limit to first 5
    }

async def search_via_internet(url: str):
    html = await fetch_page(url)
    data = await parse_amazon(html)
    d = {}
    for link in data["related_links"]:
        try:
            html = await fetch_page(link)
            temp_data = await parse_amazon(html)
            d[link] = temp_data["related_links"]
        except Exception as e:
            d[link] = f"Error fetching: {e}"
    return {"main_product": data, "related_products": d}
