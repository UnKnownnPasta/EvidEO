"""Keyboard-only walkthrough of the web UI (M4 accessibility check). Needs the API on :8000.
Types a question, checks the parsed configuration, picks a district with arrow keys, runs it from the keyboard,
and checks that focus lands on the evidence card. Exits non-zero on failure.
Usage: python tools/ui_keyboard_check.py"""
import sys

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    page = p.chromium.launch().new_page(viewport={"width": 1280, "height": 900})
    page.goto("http://localhost:8000/", wait_until="networkidle")
    page.keyboard.press("Tab")  # first stop is the skip link
    assert page.evaluate("document.activeElement.className") == "skip"
    page.focus("#q")
    page.keyboard.type("Did the flood spread in Barpeta between 2024-06-05 and 2024-07-11?")
    page.keyboard.press("Control+Enter")  # step 1 -> step 2 (configuration)
    page.wait_for_selector("#stage-config:not(.hidden)")
    page.wait_for_function("document.querySelector('#understood-cfg').innerText.includes('Barpeta')")
    assert page.input_value("#intent") == "water_change" and page.is_visible("#d2")
    assert page.input_value("#d1") == "2024-06-05" and page.input_value("#d2") == "2024-07-11"
    page.focus("#place")  # the district combobox still works from the keyboard
    page.keyboard.type("Barpe")
    page.wait_for_selector("#place-list li")
    page.keyboard.press("ArrowDown")
    assert page.get_attribute("#place", "aria-activedescendant") == "opt-0"
    page.keyboard.press("Enter")
    assert "Barpeta" in page.inner_text("#place-picked")
    page.wait_for_function("!document.querySelector('#go').disabled")
    page.focus("#go")
    page.keyboard.press("Enter")  # step 2 -> step 3 (progress, then results)
    page.wait_for_selector("#card:not(.hidden)", timeout=240_000)
    page.wait_for_timeout(300)
    assert page.evaluate("document.activeElement.id") == "card", "focus should move to the card"
    print("understood:", page.inner_text("#understood-text"))
    print("card:", page.inner_text("#answer"))
    print("keyboard walkthrough OK")
    sys.exit(0)
