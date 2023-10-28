import pandas as pd
from bs4 import BeautifulSoup
import os, time, random, json, re


r_expression = r"(?<=-\>)[\/’`',;.&%\d\w\s·-]+"

##################################
# Extract experiences
##################################

def extract_experiences(experience_tags):
    # r_expression = r'(?<=-\>)[0-9a-zA-Z ·-]+'
    experience_list = []

    order = 1
    for exp_tag in experience_tags:
        experience_div = exp_tag.parent.parent
        experience_div = [*experience_div.children][3]

        try:
            if experience_div.div.a is not None:
                # Multiple job position within same company
                multi_job = experience_div.find_all("div", class_="display-flex align-items-center") #.span.span
                company = multi_job[0].span.span
                job_title = multi_job[1].span.span
                job_type = experience_div.find("span", class_="t-14 t-normal").span

                job_title = re.search(r_expression, str(job_title)).group(0)
                company = re.search(r_expression, str(company)).group(0)
                job_type = re.search(r_expression, str(job_type)).group(0)
                job_type = job_type.split('·')[0] if '·' in job_type else job_type

                # experience_list.append((job_title, company, *[c.strip() for c in job_type.split('·')][::-1]))
                experience_list.append(
                    {
                        "job_title": job_title,
                        "company": company,
                        "job_type": job_type.split('·')[0].strip() if '·' in job_type else None,
                        "job_duration": job_type.split('·')[1].strip() if '·' in job_type else job_type,
                        "order": order
                    }
                )
        except Exception as e:
            pass
            # print(e)
        try:
            if experience_div.div.div.div is not None:
                job_title = experience_div.find("div", class_="display-flex align-items-center").span.span
                company = experience_div.find("span", class_="t-14 t-normal").span
                duration = experience_div.find("span", class_="t-14 t-normal t-black--light").span

                job_title = re.search(r_expression, str(job_title)).group(0)
                company = re.search(r_expression, str(company)).group(0)
                duration = re.search(r_expression, str(duration)).group(0)

                # experience_list.append((job_title, *[c.strip() for c in company.split('·')][::-1], duration.split('·')[-1].strip()))
                experience_list.append(
                    {
                        "job_title": job_title.strip(),
                        "company": company.split('·')[0].strip() if '·' in company else company,
                        "job_type": company.split('·')[1].strip() if '·' in company else None,
                        "job_duration": duration.split('·')[-1].strip(),
                        "order": order
                    }
                )
        except Exception as e:
            pass
            # print(e)
        order += 1

    return experience_list


##################################
# Extract other achievements
##################################

def extract_achievements(head_section, category):
    achievement_list = []

    # if category == "education" or category == "certification":
    achievement_tags = head_section.find_all("a", class_="optional-action-target-wrapper display-flex flex-column full-width")
    achievement_tags += head_section.find_all("div", class_="display-flex flex-column full-width")
    order = 1
    for tag in achievement_tags:
        institute = tag.div.span.span
        title = tag.find("span", class_="t-14 t-normal")
        title = title.span if title else None

        title = re.search(r_expression, str(title))
        title = title.group(0) if title else None
        institute = re.search(r_expression, str(institute))
        institute = institute.group(0) if institute else None

        if category == "education":
            achievement_list.append(
                {
                    "title": title,
                    "institute": institute,
                    "order": order
                }
            )
        else:
            # linkedin made this
            achievement_list.append(
                {
                    "title": institute,
                    "institute": title,
                    "order": order
                }
            )
        order += 1

    return achievement_list


##################################
# Main
##################################

if __name__ == "__main__":
    profile_data = {}
    df_profile = pd.DataFrame()
    df_experience = pd.DataFrame()
    df_education = pd.DataFrame()
    df_certification = pd.DataFrame()
    df_courses = pd.DataFrame()

    for profile in os.listdir("../profile_html/"):
        profile_url = f"../profile_html/{profile}"
        # profile_url = f"../profile_html/profile_100.html"

        with open(profile_url, 'r', encoding="utf-8") as f:
            soup = BeautifulSoup(f, features="lxml")


        # Extract basic info
        profile_card = soup.find_all("section", {"class": "artdeco-card ember-view pv-top-card"})[0]

        # name = profile_card.find("div", class_="pv-text-details__left-panel").div.h1.string.strip()
        # location = profile_card.find("div", class_="pb2 pv-text-details__left-panel").span.string.strip()
        designation = profile_card.find("div", class_="text-body-medium break-words").string.strip()

        # df = pd.DataFrame({"profile": profile, "name": name, "location": location, "designation": designation}, index=[0])
        df = pd.DataFrame({"profile": profile, "designation": designation}, index=[0])
        df_profile = pd.concat([df_profile, df], ignore_index=True, axis=0)


        # Extract experience and other achievements
        # sections = soup.find_all("section", {"class": "artdeco-card ember-view break-words pb3 mt4"})
        sections = soup.find_all("section", {"data-view-name":"profile-card"})

        for section in sections:
            # Extract experiences
            # if section.div["id"] == "experience":
            #     # print("found experience")
            #     experiences = section.find_all("ul", {"class": "pvs-list"})
            #     if len(experiences):
            #         experiences_json = extract_experiences(experiences)
            #         df = pd.DataFrame(data=experiences_json)
            #         df['profile'] = profile
            #         df_experience = pd.concat([df_experience, df], ignore_index=True, axis=0)

            # Extract educations
            if section.div["id"] == "education":
                # print("found education")
                educations_json = extract_achievements(section, "education")
                df = pd.DataFrame(data=educations_json)
                df['profile'] = profile
                df_education = pd.concat([df_education, df], ignore_index=True, axis=0)

            if section.div["id"] == "licenses_and_certifications":
                # print("found certifications")
                certifications_json = extract_achievements(section, "certification")
                df = pd.DataFrame(data=certifications_json)
                df['profile'] = profile
                df_certification = pd.concat([df_certification, df], ignore_index=True, axis=0)

            elif section.div["id"] == "courses":
                # print("found courses")
                courses_json = extract_achievements(section, "courses")
                df = pd.DataFrame(data=courses_json)
                df['profile'] = profile
                df_courses = pd.concat([df_courses, df], ignore_index=True, axis=0)

        # break
    print("Writing dataframes to csv")
    df_profile.to_csv("../raw_data/profile.csv", index=False)
    df_experience.to_csv("../raw_data/experience.csv", index=False)
    df_education.to_csv("../raw_data/education.csv", index=False)
    df_certification.to_csv("../raw_data/certification.csv", index=False)
    df_courses.to_csv("../raw_data/courses.csv", index=False)
