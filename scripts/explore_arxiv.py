"""
Explore arxiv.org to document features for clawxiv feature parity.
"""
from playwright.sync_api import sync_playwright
import os

OUTPUT_DIR = "/tmp/arxiv_exploration"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_screenshot(page, name):
    path = f"{OUTPUT_DIR}/{name}.png"
    page.screenshot(path=path, full_page=True)
    print(f"Screenshot saved: {path}")

def explore_homepage(page):
    """Explore the arxiv.org homepage"""
    print("\n=== HOMEPAGE EXPLORATION ===")
    page.goto("https://arxiv.org/")
    page.wait_for_load_state("networkidle")
    save_screenshot(page, "01_homepage")

    # Get main navigation links
    print("\nMain Navigation Links:")
    nav_links = page.locator("nav a, header a, .nav a").all()
    for link in nav_links[:20]:
        text = link.text_content().strip()
        href = link.get_attribute("href")
        if text and href:
            print(f"  - {text}: {href}")

    # Get subject categories
    print("\nSubject Categories on Homepage:")
    categories = page.locator("a[href*='/list/']").all()
    seen = set()
    for cat in categories[:30]:
        text = cat.text_content().strip()
        href = cat.get_attribute("href")
        if text and href and text not in seen:
            seen.add(text)
            print(f"  - {text}: {href}")

def explore_search(page):
    """Explore the search functionality"""
    print("\n=== SEARCH FUNCTIONALITY ===")
    page.goto("https://arxiv.org/search/")
    page.wait_for_load_state("networkidle")
    save_screenshot(page, "02_search_page")

    # Document search form fields
    print("\nSearch Form Elements:")
    inputs = page.locator("input, select, textarea").all()
    for inp in inputs:
        name = inp.get_attribute("name") or inp.get_attribute("id")
        input_type = inp.get_attribute("type") or inp.evaluate("el => el.tagName")
        placeholder = inp.get_attribute("placeholder") or ""
        if name:
            print(f"  - {name} ({input_type}): {placeholder}")

    # Check for advanced search
    page.goto("https://arxiv.org/search/advanced")
    page.wait_for_load_state("networkidle")
    save_screenshot(page, "03_advanced_search")

    print("\nAdvanced Search Fields:")
    form_groups = page.locator(".form-group, .search-field, label").all()
    for group in form_groups[:20]:
        text = group.text_content().strip()[:50]
        if text:
            print(f"  - {text}")

def explore_paper_listing(page):
    """Explore a paper listing page"""
    print("\n=== PAPER LISTING (cs.AI) ===")
    page.goto("https://arxiv.org/list/cs.AI/recent")
    page.wait_for_load_state("networkidle")
    save_screenshot(page, "04_paper_listing")

    # Document listing structure
    print("\nListing Page Elements:")

    # Check for pagination
    pagination = page.locator("a[href*='skip='], .pagination, .paging").all()
    print(f"  - Pagination links: {len(pagination)}")

    # Paper entries
    entries = page.locator("dt, .list-title, .arxiv-result").all()
    print(f"  - Paper entries visible: {len(entries)}")

    # Get structure of a paper entry
    first_entry = page.locator(".meta, .list-title").first
    if first_entry:
        print(f"\nFirst Entry Structure:")
        print(f"  {first_entry.text_content()[:200]}...")

def explore_abstract_page(page):
    """Explore a paper abstract page"""
    print("\n=== ABSTRACT PAGE ===")
    # Get a recent paper ID from listing
    page.goto("https://arxiv.org/list/cs.AI/recent")
    page.wait_for_load_state("networkidle")

    # Find first paper link
    paper_link = page.locator("a[href*='/abs/']").first
    if paper_link:
        href = paper_link.get_attribute("href")
        paper_id = href.split("/abs/")[-1] if "/abs/" in href else "2401.00001"
    else:
        paper_id = "2401.00001"

    page.goto(f"https://arxiv.org/abs/{paper_id}")
    page.wait_for_load_state("networkidle")
    save_screenshot(page, "05_abstract_page")

    print(f"\nAbstract Page for: {paper_id}")

    # Document page sections
    print("\nPage Sections:")
    sections = ["title", "authors", "abstract", "comments", "subjects", "cite", "download"]
    for section in sections:
        elem = page.locator(f".{section}, #{section}, [class*='{section}']").first
        if elem.count() > 0:
            print(f"  - {section}: Found")

    # Download links
    print("\nDownload Links:")
    download_links = page.locator("a[href*='/pdf/'], a[href*='/ps/'], a[href*='/src/']").all()
    for link in download_links[:10]:
        text = link.text_content().strip()
        href = link.get_attribute("href")
        print(f"  - {text}: {href}")

    # Metadata elements
    print("\nMetadata Elements:")
    meta = page.locator(".metatable td, .tablecell, .submission-history").all()
    for m in meta[:10]:
        text = m.text_content().strip()[:60]
        if text:
            print(f"  - {text}")

def explore_pdf_page(page):
    """Explore PDF viewer/download"""
    print("\n=== PDF VIEWING ===")
    page.goto("https://arxiv.org/list/cs.AI/recent")
    page.wait_for_load_state("networkidle")

    pdf_link = page.locator("a[href*='/pdf/']").first
    if pdf_link:
        href = pdf_link.get_attribute("href")
        print(f"PDF Link format: {href}")
        # Note: Don't actually load PDF, just document the URL pattern
        print(f"  Pattern: /pdf/[paper_id]")

def explore_user_features(page):
    """Explore user account features"""
    print("\n=== USER/ACCOUNT FEATURES ===")
    page.goto("https://arxiv.org/user")
    page.wait_for_load_state("networkidle")
    save_screenshot(page, "06_user_page")

    print("\nUser Features Available:")
    links = page.locator("a").all()
    for link in links[:30]:
        text = link.text_content().strip()
        href = link.get_attribute("href") or ""
        if text and any(word in href.lower() or word in text.lower() for word in
                       ["login", "register", "account", "submit", "author", "profile"]):
            print(f"  - {text}: {href}")

def explore_submission(page):
    """Explore submission process"""
    print("\n=== SUBMISSION FEATURES ===")
    page.goto("https://arxiv.org/submit")
    page.wait_for_load_state("networkidle")
    save_screenshot(page, "07_submit_page")

    print("\nSubmission Page Content:")
    content = page.locator("main, .content, article").first
    if content.count() > 0:
        text = content.text_content()[:1000]
        print(f"  {text}")

def explore_catchup(page):
    """Explore the catchup/notification features"""
    print("\n=== CATCHUP/NEW SUBMISSIONS ===")
    page.goto("https://arxiv.org/list/cs.AI/new")
    page.wait_for_load_state("networkidle")
    save_screenshot(page, "08_new_submissions")

    print("\nNew Submissions Page:")
    # Check for date navigation
    date_nav = page.locator("a[href*='pastweek'], a[href*='current'], .date-nav").all()
    print(f"  Date navigation links: {len(date_nav)}")

def explore_api_info(page):
    """Check for API documentation"""
    print("\n=== API DOCUMENTATION ===")
    page.goto("https://arxiv.org/help/api")
    page.wait_for_load_state("networkidle")
    save_screenshot(page, "09_api_help")

    print("\nAPI Help Page:")
    links = page.locator("a[href*='api']").all()
    for link in links[:15]:
        text = link.text_content().strip()
        href = link.get_attribute("href")
        if text:
            print(f"  - {text}: {href}")

def explore_rss_feeds(page):
    """Check for RSS/Atom feeds"""
    print("\n=== RSS/ATOM FEEDS ===")
    page.goto("https://arxiv.org/help/rss")
    page.wait_for_load_state("networkidle")
    save_screenshot(page, "10_rss_help")

    print("\nRSS Feed Information:")
    content = page.locator("main, .content, article").first
    if content.count() > 0:
        text = content.text_content()[:500]
        print(f"  {text}")

def explore_stats(page):
    """Explore statistics pages"""
    print("\n=== STATISTICS ===")
    page.goto("https://arxiv.org/stats/monthly_submissions")
    page.wait_for_load_state("networkidle")
    save_screenshot(page, "11_stats")

    print("\nStats Page:")
    tables = page.locator("table").all()
    print(f"  Tables found: {len(tables)}")

def main():
    print("=" * 60)
    print("ARXIV.ORG FEATURE EXPLORATION FOR CLAWXIV PARITY")
    print("=" * 60)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 900})
        page = context.new_page()

        try:
            explore_homepage(page)
            explore_search(page)
            explore_paper_listing(page)
            explore_abstract_page(page)
            explore_pdf_page(page)
            explore_user_features(page)
            explore_submission(page)
            explore_catchup(page)
            explore_api_info(page)
            explore_rss_feeds(page)
            explore_stats(page)
        except Exception as e:
            print(f"Error during exploration: {e}")
            import traceback
            traceback.print_exc()
        finally:
            browser.close()

    print("\n" + "=" * 60)
    print(f"Screenshots saved to: {OUTPUT_DIR}")
    print("=" * 60)

if __name__ == "__main__":
    main()
