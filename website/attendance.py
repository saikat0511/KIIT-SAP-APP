from .login import login
from .ids import years, sessions
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


def restore_original_table_layout(frame):
    frame.get_by_text('Attendance Details').click(button='right')
    frame.get_by_text('User Settings').click()
    if frame.get_by_text('Restore Original Order').is_visible():
        frame.get_by_text('Restore Original Order').click()
    return frame


def unhide_image(frame):
    frame.locator('Attendance Details').click(button='right')
    frame.get_by_text('User Settings').click()
    if frame.get_by_text('Restore Original Order').is_visible():
        frame.get_by_text('Restore Original Order').click()
    return frame


def get_attendance(username, password, year, session):
    year_id = years[year]
    session_id = sessions[session]

    with sync_playwright() as p:
        browser = p.chromium.launch() #headless=False
        context = browser.new_context()
        context.set_default_timeout(50000)
        page = login(context, username, password)
        if page == -1:
            return -1

        try:
            desktopInnerPage = page.frame_locator('#ivuFrm_page0ivu3')
            desktopInnerPage.locator('a[title = "Student Self Service"]').click()
            desktopInnerPage.locator('a[title = "Student Attendance Details"]').click()

            isolatedWorkArea = desktopInnerPage.frame_locator('#isolatedWorkArea')

            # restore original settings before scraping to get correct column order
            # isolatedWorkArea.get_by_text('Select Year & Session').click(button='right')
            # isolatedWorkArea.get_by_text('User Settings').click()
            # isolatedWorkArea.get_by_text('More...').click()
            # URLSPW = page.frame_locator('#URLSPW-0')
            # URLSPW.get_by_text('Reset User Settings for Running Application').click()
            isolatedWorkArea = restore_original_table_layout(isolatedWorkArea)
            page.wait_for_timeout(100)
            
            isolatedWorkArea.locator('#WD52').click()
            isolatedWorkArea.locator(year_id).click() #select 2022-2023
            isolatedWorkArea.locator('#WD6E').click()
            isolatedWorkArea.locator(session_id).click() # select spring
            isolatedWorkArea.locator('#WD7B').click() # submit

        except PlaywrightTimeoutError:
            return -1

        page.wait_for_load_state('networkidle')
        #page.wait_for_timeout(1000)

        #WD7E
        subjectRowLocator = isolatedWorkArea.locator('#WD7E-contentTBody').locator('tr[rt = "1"]')
        subject_name = subjectRowLocator.locator('td[cc = "1"]')
        present_count = subjectRowLocator.locator('td[cc = "2"]')
        absent_count = subjectRowLocator.locator('td[cc = "3"]')
        day_count = subjectRowLocator.locator('td[cc = "5"]')
        present_percent = subjectRowLocator.locator('td[cc = "6"]')
        faculty_name = subjectRowLocator.locator('td[cc = "8"]')
        
        attendance = {
            'Subject': [],
            'No. of Present': [],
            'No. of Absent': [],
            'No. of Days': [],
            'Total Percentage': [],
            'Faculty Name': []
        }

        totalSubjects = subject_name.count()
        for subject in range(totalSubjects):
            attendance['Subject'].append(subject_name.nth(subject).all_inner_texts()[0])
            attendance['No. of Present'].append(present_count.nth(subject).all_inner_texts()[0])
            attendance['No. of Absent'].append(absent_count.nth(subject).all_inner_texts()[0])
            attendance['No. of Days'].append(day_count.nth(subject).all_inner_texts()[0])
            attendance['Total Percentage'].append(present_percent.nth(subject).all_inner_texts()[0])
            attendance['Faculty Name'].append(faculty_name.nth(subject).all_inner_texts()[0])

        #attendance = pd.DataFrame(attendance).to_csv(index=False) # returns empty csv if connection issues
        return attendance
