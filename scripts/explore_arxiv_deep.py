"""
Deep exploration of specific arxiv.org features for clawxiv feature parity.
"""
from playwright.sync_api import sync_playwright
import os

OUTPUT_DIR = "/tmp/arxiv_exploration"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_screenshot(page, name):
    path = f"{OUTPUT_DIR}/{name}.png"
    page.screenshot(path=path, full_page=True)
    print(f"Screenshot saved: {path}")

def explore_subject_taxonomy(page):
    """Explore full subject category taxonomy"""
    print("\n=== SUBJECT TAXONOMY ===")
    page.goto("https://arxiv.org/")
    page.wait_for_load_state("networkidle")

    # Get all main categories
    print("\nMain Subject Areas:")
    subjects = {}

    # Look for all category headings and subcategories
    sections = page.locator("h2, h3, h4").all()
    for section in sections:
        text = section.text_content().strip()
        if text and len(text) < 100:
            print(f"  Section: {text}")

    # Get all category links
    cat_links = page.locator("a[href*='/list/']").all()
    for link in cat_links[:50]:
        href = link.get_attribute("href") or ""
        text = link.text_content().strip()
        if "/list/" in href and text:
            cat_id = href.split("/list/")[-1].split("/")[0]
            if cat_id not in subjects:
                subjects[cat_id] = text

    print("\nCategory IDs found:")
    for cat_id, name in sorted(subjects.items())[:40]:
        print(f"  - {cat_id}: {name}")

def explore_paper_details(page):
    """Deep dive into paper abstract page structure"""
    print("\n=== PAPER DETAIL PAGE STRUCTURE ===")
    page.goto("https://arxiv.org/abs/2401.00001")
    page.wait_for_load_state("networkidle")
    save_screenshot(page, "12_paper_detail_structure")

    # Get page structure
    print("\nHTML Structure:")

    # Title
    title = page.locator(".title, h1.title").first
    if title.count() > 0:
        print(f"  Title: {title.text_content().strip()[:100]}")

    # Authors
    authors = page.locator(".authors, .ltx_authors").first
    if authors.count() > 0:
        print(f"  Authors section found")

    # Abstract
    abstract = page.locator(".abstract, blockquote.abstract").first
    if abstract.count() > 0:
        print(f"  Abstract: {abstract.text_content().strip()[:150]}...")

    # Check for extra tabs/sections
    print("\nExtra Sections/Links:")
    extra_links = page.locator("a").all()
    seen_hrefs = set()
    for link in extra_links:
        href = link.get_attribute("href") or ""
        text = link.text_content().strip()
        if text and href and href not in seen_hrefs:
            if any(x in href for x in ['/format/', '/bibtex/', '/cite/', '/trackback/']):
                seen_hrefs.add(href)
                print(f"  - {text}: {href}")

def explore_version_history(page):
    """Explore paper version history"""
    print("\n=== VERSION HISTORY ===")
    page.goto("https://arxiv.org/abs/2301.00001")
    page.wait_for_load_state("networkidle")

    # Check for version links
    version_links = page.locator("a[href*='v1'], a[href*='v2'], a[href*='v3']").all()
    print(f"\nVersion links found: {len(version_links)}")

    # Look for submission history
    history = page.locator(".submission-history, .dateline").first
    if history.count() > 0:
        print(f"Submission History: {history.text_content().strip()[:200]}")

def explore_formats_page(page):
    """Explore other formats page"""
    print("\n=== OTHER FORMATS ===")
    page.goto("https://arxiv.org/format/2401.00001")
    page.wait_for_load_state("networkidle")
    save_screenshot(page, "13_formats_page")

    print("\nAvailable Formats:")
    links = page.locator("a").all()
    for link in links:
        href = link.get_attribute("href") or ""
        text = link.text_content().strip()
        if text and any(x in href.lower() or x in text.lower() for x in
                       ['pdf', 'ps', 'source', 'dvi', 'html']):
            print(f"  - {text}: {href}")

def explore_list_views(page):
    """Explore different list view options"""
    print("\n=== LIST VIEW VARIATIONS ===")

    # Recent submissions
    page.goto("https://arxiv.org/list/cs.AI/recent")
    page.wait_for_load_state("networkidle")
    print("\n/recent view:")
    entries = page.locator("dt").all()
    print(f"  Entries: {len(entries)}")

    # New submissions (today)
    page.goto("https://arxiv.org/list/cs.AI/new")
    page.wait_for_load_state("networkidle")
    save_screenshot(page, "14_new_submissions")
    print("\n/new view:")
    new_entries = page.locator("dt").all()
    print(f"  Entries: {len(new_entries)}")

    # By year/month
    page.goto("https://arxiv.org/list/cs.AI/2401")
    page.wait_for_load_state("networkidle")
    save_screenshot(page, "15_monthly_archive")
    print("\n/YYMM view (monthly archive):")
    monthly = page.locator("dt").all()
    print(f"  Entries: {len(monthly)}")

    # Past week
    page.goto("https://arxiv.org/list/cs.AI/pastweek?skip=0&show=25")
    page.wait_for_load_state("networkidle")
    print("\n/pastweek view:")
    pastweek = page.locator("dt").all()
    print(f"  Entries: {len(pastweek)}")

def explore_catchup_feature(page):
    """Explore catchup/notification features"""
    print("\n=== CATCHUP INTERFACE ===")
    page.goto("https://arxiv.org/list/cs/new")
    page.wait_for_load_state("networkidle")

    # Look for date-based navigation
    print("\nDate Navigation Elements:")
    date_elements = page.locator("[class*='date'], [id*='date'], time, .dateline").all()
    for elem in date_elements[:5]:
        print(f"  - {elem.text_content().strip()[:60]}")

def explore_search_results(page):
    """Explore search results page structure"""
    print("\n=== SEARCH RESULTS STRUCTURE ===")
    page.goto("https://arxiv.org/search/?query=machine+learning&searchtype=all")
    page.wait_for_load_state("networkidle")
    save_screenshot(page, "16_search_results")

    # Result count
    result_count = page.locator(".search-pagination, .results-count, h1").first
    if result_count.count() > 0:
        print(f"\nResults header: {result_count.text_content().strip()[:100]}")

    # Pagination
    print("\nPagination:")
    pagination = page.locator(".pagination a, [class*='paging'] a").all()
    for pag in pagination[:10]:
        text = pag.text_content().strip()
        href = pag.get_attribute("href")
        print(f"  - {text}: {href}")

    # Sort options
    print("\nSort/Filter Options:")
    selects = page.locator("select").all()
    for sel in selects:
        name = sel.get_attribute("name") or sel.get_attribute("id")
        options = sel.locator("option").all()
        opt_texts = [o.text_content().strip() for o in options[:5]]
        print(f"  - {name}: {opt_texts}")

def explore_author_pages(page):
    """Explore author-related pages"""
    print("\n=== AUTHOR FEATURES ===")

    # Search by author
    page.goto("https://arxiv.org/search/?searchtype=author&query=hinton")
    page.wait_for_load_state("networkidle")
    save_screenshot(page, "17_author_search")

    print("\nAuthor Search Results:")
    results = page.locator(".arxiv-result, .list-group-item").all()
    print(f"  Results found: {len(results)}")

def explore_category_pages(page):
    """Explore category-specific pages"""
    print("\n=== CATEGORY LANDING PAGES ===")
    page.goto("https://arxiv.org/archive/cs")
    page.wait_for_load_state("networkidle")
    save_screenshot(page, "18_category_landing")

    print("\nCategory Page Content:")
    subcats = page.locator("a[href*='/list/cs.']").all()
    print(f"  Subcategories: {len(subcats)}")
    for sub in subcats[:10]:
        text = sub.text_content().strip()
        print(f"    - {text}")

def explore_html5_papers(page):
    """Check for HTML5 paper viewing"""
    print("\n=== HTML5 PAPER VIEW ===")
    page.goto("https://arxiv.org/html/2401.00001")
    page.wait_for_load_state("networkidle")
    save_screenshot(page, "19_html_view")

    print("\nHTML View Page:")
    body_text = page.locator("body").text_content()[:200]
    print(f"  {body_text}")

def explore_bibtex_export(page):
    """Explore citation export features"""
    print("\n=== CITATION EXPORT ===")
    page.goto("https://arxiv.org/bibtex/2401.00001")
    page.wait_for_load_state("networkidle")

    print("\nBibTeX Export:")
    content = page.locator("pre, code, .bibtex").first
    if content.count() > 0:
        print(f"  {content.text_content()[:300]}")

def explore_trackback(page):
    """Explore trackback/link features"""
    print("\n=== TRACKBACK/LINKS ===")
    page.goto("https://arxiv.org/tb/2401.00001")
    page.wait_for_load_state("networkidle")

    print("\nTrackback Page:")
    content = page.locator("body").text_content()[:300]
    print(f"  {content}")

def main():
    print("=" * 60)
    print("ARXIV.ORG DEEP FEATURE EXPLORATION")
    print("=" * 60)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 900})
        page = context.new_page()

        try:
            explore_subject_taxonomy(page)
            explore_paper_details(page)
            explore_version_history(page)
            explore_formats_page(page)
            explore_list_views(page)
            explore_catchup_feature(page)
            explore_search_results(page)
            explore_author_pages(page)
            explore_category_pages(page)
            explore_html5_papers(page)
            explore_bibtex_export(page)
            explore_trackback(page)
        except Exception as e:
            print(f"Error during exploration: {e}")
            import traceback
            traceback.print_exc()
        finally:
            browser.close()

    print("\n" + "=" * 60)
    print("DEEP EXPLORATION COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()
