from ..models import Course, CustomUser, UserWatchedCourse
from django.db.models import F
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
from django.core.mail import send_mass_mail
from django.conf import settings
import urllib3


def scrape_timetable():
    driver = webdriver.Chrome()
    driver.get("https://oracle-www.dartmouth.edu/dart/groucho/timetable.main")
    driver.find_element(By.NAME, "searchtype").click()
    driver.find_element(By.ID, "term1").click()
    driver.find_element(By.ID, "allsubjects").click()
    driver.find_element(By.XPATH, "//*[@id='content']/table[3]/tbody/tr[8]/td[1]/input").click()
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    data = soup.find_all("div", "data-table")
    table = pd.read_html(str(data), flavor='html5lib')[0]
    driver.quit()

    courses_qset = []

    for index, row in table.iterrows():

        course = Course()
        course.crn = row['CRN']
        course.subject = row['Subj']
        course.course_number = row['Num']
        course.section = row['Sec']
        course.title = row['Title']
        course.period = row['Period Code']
        course.instructor = row['Instructor']
        course.world_culture = row['WC']
        course.distributive = row['Dist']

        if not pd.isnull(row['Lim']):
            course.enrollment_limit = row['Lim']

        if not pd.isnull(row['Enrl']):
            course.num_enrolled = row['Enrl']

        course.requires_ip = not pd.isnull(row['Status'])
        course.is_nr_eligible = not pd.isnull(row['NR Eligible or CT/NC'])

        courses_qset.append(course)

    Course.objects.bulk_create(
        courses_qset,
        update_conflicts=True,
        unique_fields=['crn'],
        update_fields=['num_enrolled', 'enrollment_limit', 'requires_ip']
    )

    #send_notifications()


def get_users_to_email():
    open_courses = Course.objects.filter(num_enrolled__lt=F('enrollment_limit'))
    users_to_email = UserWatchedCourse.objects.filter(course__in=open_courses)
    return users_to_email


def send_notifications():
    user_watched_courses = get_users_to_email()

    emails = []
    for user_course_pair in user_watched_courses:
        user = user_course_pair.user
        course = user_course_pair.course
        num_spots = course.enrollment_limit - course.num_enrolled
        course_number = course.truncate_course_number()

        subject = f"New spot open in {course.subject} {course_number}"

        if num_spots == 1:
            message = f"There is currently {course.enrollment_limit - course.num_enrolled} " \
                      f"spot open in {course.subject} {course_number}: {course.title}. " \
                      f"Sign up now!\n\n CRN: {course.crn}"
        else:
            message = f"There are currently {course.enrollment_limit - course.num_enrolled} " \
                      f"spots open in {course.subject} {course_number}: {course.title}. " \
                      f"Sign up now!\n\n CRN: {course.crn}"

        email = (subject, message, settings.EMAIL_HOST_USER, [user.email])
        emails.append(email)

    send_mass_mail(tuple(emails), fail_silently=False)







