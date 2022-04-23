import pandas as pd
from bs4 import BeautifulSoup
import os, time, random, json, re


##################################
# Extract experiences
##################################

def extract_experiences(experience_tags):
    # r_expression = r'(?<=-\>)[0-9a-zA-Z ·-]+'
    r_expression = r"(?<=-\>)[0-9,;.\w\s&·-]+"
    experience_list = []

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
                        "job_duration": job_type.split('·')[1].strip() if '·' in job_type else job_type
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
                        "job_title": job_title,
                        "company": company.split('·')[0].strip() if '·' in company else company,
                        "job_type": company.split('·')[1].strip() if '·' in company else None,
                        "job_duration": duration.split('·')[-1].strip()
                    }
                )
        except Exception as e:
            pass
            # print(e)

    return experience_list


##################################
# Extract other achievements
##################################

def extract_achievements(head_section, category):
    r_expression = r"(?<=-\>)[0-9,;.\w\s&·-]+"
    achievement_list = []

    # if category == "education" or category == "certification":
    achievement_tags = head_section.find_all("a", class_="optional-action-target-wrapper display-flex flex-column full-width")
    achievement_tags += head_section.find_all("div", class_="display-flex flex-column full-width")
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
                    "institute": institute
                }
            )
        else:
            # linkedin made this
            achievement_list.append(
                {
                    "title": institute,
                    "institute": title
                }
            )

    return achievement_list


##################################
# Main
##################################

if __name__ == "__main__":
    profile_data = {}

    for profile in os.listdir("../scraped_data/"):
        profile_data[profile] = {}

        profile_url = f"../scraped_data/{profile}"
        # profile_url = f"../scraped_data/profile_100.html"

        with open(profile_url, 'r', encoding="utf-8") as f:
            soup = BeautifulSoup(f, features="lxml")


        # Extract basic info
        profile_card = soup.find_all("section", {"class": "artdeco-card ember-view pv-top-card"})[0]

        profile_data[profile]["name"] = profile_card.find("div", class_="pv-text-details__left-panel").div.h1.string.strip()
        profile_data[profile]["location"] = profile_card.find("div", class_="pb2 pv-text-details__left-panel").span.string.strip()
        profile_data[profile]["designation"] = profile_card.find("div", class_="text-body-medium break-words").string.strip()


        # Extract experience and other achievements
        sections = soup.find_all("section", {"class": "artdeco-card ember-view break-words pb3 mt4"})

        for section in sections:
            # Extract experiences
            if section.div["id"] == "experience":
                # print("found experience")
                experiences = section.find_all("a", {"data-field": "experience_company_logo"})
                if len(experiences):
                    profile_data[profile]["experiences"] = extract_experiences(experiences)

            # Extract educations
            if section.div["id"] == "education":
                # print("found education")
                profile_data[profile]["educations"] = extract_achievements(section, "education")

            if section.div["id"] == "licenses_and_certifications":
                # print("found certifications")
                profile_data[profile]["certifications"] = extract_achievements(section, "certification")

            elif section.div["id"] == "courses":
                # print("found courses")
                profile_data[profile]["courses"] = extract_achievements(section, "courses")

        # break


    with open("profile_data.json", "w", encoding="utf-8") as f:
        print(f"writing {len(profile_data)} profiles to disk")
        f.write(json.dumps(profile_data))
    # print(json.dumps(profile_data))
