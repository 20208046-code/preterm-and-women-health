"""
Records a demo video of every feature of the Preterm & Women Health app.
Drives the real running app (frontend :3000 + Flask backend :5000) with
Playwright and records the whole walkthrough to a .webm video.
"""
import os
from playwright.sync_api import sync_playwright

BASE = "http://localhost:3000"
IMG = "/Users/hazem/Desktop/Pretem-and-Women-Health_Hazem 1/Data/test/malignant/538_HC_Annotation.png"
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs", "video")
os.makedirs(OUT_DIR, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(
        viewport={"width": 1280, "height": 800},
        record_video_dir=OUT_DIR,
        record_video_size={"width": 1280, "height": 800},
    )
    page = context.new_page()

    def pause(ms=1500):
        page.wait_for_timeout(ms)

    # --- 1. Home page ---
    page.goto(BASE, wait_until="networkidle")
    pause(2500)
    page.mouse.wheel(0, 350)          # reveal the feature cards
    pause(2500)
    page.mouse.wheel(0, -350)
    pause(800)

    # --- 2. Preterm Risk Assessment (real SVM prediction) ---
    page.goto(BASE + "/preterm", wait_until="networkidle")
    pause(1500)
    page.select_option('select[name="model"]', 'svm'); pause(400)
    page.select_option('select[name="age_group"]', '30 to 34 yrs'); pause(400)
    page.select_option('select[name="reported_race_ethnicity"]', 'Black, non-Hispanic'); pause(400)
    page.select_option('select[name="previous_births"]', 'Two'); pause(400)
    page.select_option('select[name="tobacco_use_during_pregnancy"]', 'No'); pause(400)
    page.select_option('select[name="adequate_prenatal_care"]', 'Adequate'); pause(700)
    page.click('form button[type="submit"]')
    page.wait_for_selector('text=Prediction Result', timeout=20000)
    page.locator('text=Prediction Result').scroll_into_view_if_needed()
    pause(3500)                        # hold on the result

    # --- 3. Fetal / Breast Ultrasound Classification (real CNN prediction) ---
    page.goto(BASE + "/ultrasound", wait_until="networkidle")
    pause(1500)
    page.set_input_files('input[type="file"]', IMG)
    pause(1200)
    page.click('button:has-text("Upload & Predict")')
    page.wait_for_selector('text=Class:', timeout=40000)
    page.locator('text=Prediction Result').scroll_into_view_if_needed()
    pause(3800)                        # hold on the result

    # --- 4. The informational pages ---
    for path in ["/symptoms", "/complications", "/ovulation"]:
        page.goto(BASE + path, wait_until="networkidle")
        pause(2500)

    page.goto(BASE, wait_until="networkidle")
    pause(1500)

    video_path = page.video.path()
    context.close()   # finalizes the video file
    browser.close()

print("VIDEO_SAVED:", video_path)
