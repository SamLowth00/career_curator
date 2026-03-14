import os
import requests
import json
from bs4 import BeautifulSoup
from openai import OpenAI


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

SCRAPER_API_KEY = os.getenv("SCRAPER_API_KEY")
SCRAPER_API_DOMAINS = ("indeed.com")


def cleanAiResponse(raw):
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```")[1]
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]
        cleaned = cleaned.strip()
    return cleaned


def fetch_html(url):
    # use scraperapi if the url is from the list of domains to bypass cloudflare protection
    if any(domain in url for domain in SCRAPER_API_DOMAINS):
        scraper_url = f"http://api.scraperapi.com?api_key={SCRAPER_API_KEY}&url={url}"
        return requests.get(scraper_url).text
    return requests.get(url, headers=HEADERS).text


#works with greenhouse, linkedin, indeed (via ScraperAPI)
def parse_job(url):
    html = fetch_html(url)

    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator="\n", strip=True)
    # Truncate to avoid token limits
    text = text[:12000]

    prompt = f"""Extract the job details from the following webpage text and return a JSON object with these exact keys:
- title: the job title
- company: the company name
- description: the full job description
- salary: salary if mentioned, otherwise null

Return only valid JSON, no markdown, no explanation.

Webpage text:
{text}"""

    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0,
        response_format={"type": "json_object"},
        messages=[{"role": "user", "content": prompt}],
    )

    raw = response.choices[0].message.content or ""

    cleaned = cleanAiResponse(raw)

    if not cleaned:
        raise ValueError("AI returned empty response when parsing job.")

    try:
        result = json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(f"AI returned unparseable JSON when parsing job: {e}") from e

    return result




# using JobPosting
# def parse_job_structured(url):
#     """Original structured-data approach (JSON-LD / __NEXT_DATA__). Kept for reference."""
#     html = requests.get(url, headers=HEADERS).text
#     html_length = len(html)
#     print('📄 HTML length:', html_length)
#
#     soup = BeautifulSoup(html, "html.parser")
#
#     all_scripts = soup.find_all("script")
#     print('🔍 All script tags:')
#     for s in all_scripts:
#         attrs = dict(s.attrs)
#         snippet = (s.string or '')[:80].replace('\n', ' ')
#         print(f'  type={attrs.get("type")} id={attrs.get("id")} src={attrs.get("src")} | {snippet}')
#
#     scripts = soup.find_all("script", type="application/ld+json")
#
#     for script in scripts:
#         try:
#             data = json.loads(script.string)
#             # JSON-LD can be a list or wrapped in @graph
#             if isinstance(data, list):
#                 data = next((d for d in data if d.get("@type") == "JobPosting"), None)
#             elif isinstance(data, dict) and "@graph" in data:
#                 data = next((d for d in data["@graph"] if d.get("@type") == "JobPosting"), None)
#             if data and data.get("@type") == "JobPosting":
#                 return {
#                     "title": data.get("title"),
#                     "company": data.get("hiringOrganization", {}).get("name"),
#                     "location": data.get("jobLocation"),
#                     "salary": data.get("baseSalary"),
#                     "description": data.get("description")
#                 }
#         except:
#             print('error')
#             continue
#
#     # Fallback: Indeed embeds data in Next.js __NEXT_DATA__ script tag
#     next_data_tag = soup.find("script", id="__NEXT_DATA__")
#     if next_data_tag:
#         try:
#             next_data = json.loads(next_data_tag.string)
#             job_data = (
#                 next_data
#                 .get("props", {})
#                 .get("pageProps", {})
#                 .get("jobInfoWrapperModel", {})
#                 .get("jobInfoModel", {})
#             )
#             print('🔍 Indeed job_data keys:', list(job_data.keys()) if job_data else 'not found')
#             if job_data:
#                 return {
#                     "title": job_data.get("jobTitle"),
#                     "company": job_data.get("companyName"),
#                     "location": job_data.get("jobLocation"),
#                     "salary": None,
#                     "description": job_data.get("sanitizedJobDescription")
#                 }
#         except Exception as e:
#             print('❌ __NEXT_DATA__ parse error:', e)
#
#     return None
