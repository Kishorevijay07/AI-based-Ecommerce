

    # Implement web scraping logic here
import requests
from bs4 import BeautifulSoup
import json

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

def fetch_page(url):
    """Fetch HTML content of a page"""
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    return resp.text

def parse_amazon(html):
    """Parse Amazon product page and extract details"""
    soup = BeautifulSoup(html, "html.parser")

    # Title
    title = soup.select_one("#productTitle")
    title = title.get_text(strip=True) if title else None

    # Price
    price = None
    for sel in ("#priceblock_ourprice", "#priceblock_dealprice", "#corePrice_feature_div .a-offscreen"):
        el = soup.select_one(sel)
        if el:
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

def web_scraper_service(url: str):
    """Main function to fetch Amazon product and return JSON"""
    html = fetch_page(url)
    data = parse_amazon(html)

    # Fetch related links data
    related_dict = {}
    for link in data["related_links"]:
        html_related = fetch_page(link)
        temp_data = parse_amazon(html_related)
        related_dict[link] = temp_data["related_links"][:5]

    data["related_products_expanded"] = related_dict

    return json.dumps(data, indent=2, ensure_ascii=False)




url = "https://www.amazon.in/Samsung-Galaxy-Smartphone-Titanium-Storage/dp/B0CS5XW6TN/ref=sr_1_1?_encoding=UTF8&content-id=amzn1.sym.15692926-7af5-4978-a095-8e6f1f81f807&dib=eyJ2IjoiMSJ9.h5D_SB61tNg4XGcuTwO61vJuOJuTAAUl9npQvDxHg_1ZA6Y-oVQCOp5RcBmFIoc-6lFlvBADiexjR_Czl7wHcVlghVyDwqK4dfFmK5PF7sv-EHxTfHHfmjPDap3g24PBfTyGyzfY72TRoh-lIewqjHARjlc1ddiP85dP87c-3U6tfw0Iky1KxHsCbSdL0QaWATtICUPU1QAu8qyYPGQY5JfNVcbtKmPOkpxSsc7EEeCH3hgGn51r_Fej7qZ149bPkCt40A_UsJm94tUeOJLr7vZtQPZI9CpJzETf3P5NYP0.q_SiM0L0922-RMChDYHvpJNGz2-XQbQfNzJ3g6DlQb4&dib_tag=se&pd_rd_r=0188c998-4fa2-4e76-a384-c12150a57c2f&pd_rd_w=A4ILp&pd_rd_wg=nMCwb&qid=1758691093&refinements=p_123%3A46655&rnid=1389432031&s=electronics&sr=1-1"
html = fetch_page(url)
data = parse_amazon(html)
res=[]
print(data["related_links"])
d={}
for i in range(len(data["related_links"])):
    html = fetch_page(data["related_links"][i])
    temp_data = parse_amazon(html)
    for j in temp_data["related_links"]:
        res.append(j)
    print("len",len(res))
    d[data["related_links"][i]]=res
    print("Dictionary : ",d)
    res=[]
print(json.dumps(data, indent=2, ensure_ascii=False))
print()