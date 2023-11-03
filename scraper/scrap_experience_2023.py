import pandas as pd
from bs4 import BeautifulSoup
import os, time, random, json, re


r_expression = r"(?<=-\>)[\/’`',;.&%\d\w\s·-]+"

##################################
# Extract experiences
##################################

def extract_experiences(experiences_li):
    # r_expression = r'(?<=-\>)[0-9a-zA-Z ·-]+'
    experience_list = []

    order_level_1 = 1
    for exp in experiences_li:
        # experience_div = exp_tag.parent.parent
        # experience_div = [*experience_div.children][3]

        if len(exp.div.div.find_all('div', {'class':'display-flex flex-column full-width align-self-center'})) > 1:
            # Multiple job position within same company
            multi_job = exp.div.div.find_all("a")
            company = multi_job[1].find_all('span', {'aria-hidden':'true'})[0].text
            # company = re.search(r_expression, str(company)).group(0)
            order_level_2 = 1
            for job in multi_job[2:]:
                job_title = job.span
                job_type = exp.find("span", class_="t-14 t-normal").span

                job_title = re.search(r_expression, str(job_title)).group(0)
                job_type = re.search(r_expression, str(job_type)).group(0)
                job_type = job_type.split('·')[0] if '·' in job_type else job_type

                # experience_list.append((job_title, company, *[c.strip() for c in job_type.split('·')][::-1]))
                experience_list.append(
                    {
                        "job_title": job_title,
                        "company": company,
                        "job_type": job_type.split('·')[0].strip() if '·' in job_type else None,
                        "job_duration": job_type.split('·')[1].strip() if '·' in job_type else job_type,
                        "order": f"{order_level_1}.{order_level_2}"
                    }
                )
                # print(experience_list[-1])
                order_level_2 += 1
        else:
            job_details = exp.find_all('span', {'aria-hidden':'true'})
            job_title = job_details[0]
            company = job_details[1]
            duration = job_details[2]

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
                    "order": order_level_1
                }
            )
            # print(experience_list[-1])
        order_level_1 += 1

    return experience_list


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

        if "experience" not in profile_url:
            continue

        with open(profile_url, 'r', encoding="utf-8") as f:
            soup = BeautifulSoup(f, features="lxml")

        # Extract basic info
        # profile_card = soup.find_all("section", {"class": "artdeco-card ember-view pv-top-card"})[0]

        # # name = profile_card.find("div", class_="pv-text-details__left-panel").div.h1.string.strip()
        # # location = profile_card.find("div", class_="pb2 pv-text-details__left-panel").span.string.strip()
        # designation = profile_card.find("div", class_="text-body-medium break-words").string.strip()

        # # df = pd.DataFrame({"profile": profile, "name": name, "location": location, "designation": designation}, index=[0])
        # df = pd.DataFrame({"profile": profile, "designation": designation}, index=[0])
        # df_profile = pd.concat([df_profile, df], ignore_index=True, axis=0)


        # Extract experience and other achievements
        experiences = soup.find("ul", {"class":"pvs-list"})
        experiences = experiences.find_all("li", recursive=False)
        if len(experiences):
            for exp in experiences:
                experiences_json = extract_experiences(experiences)
                df = pd.DataFrame(data=experiences_json)
                df['profile'] = profile
                df_experience = pd.concat([df_experience, df], ignore_index=True, axis=0)

    df_experience.drop_duplicates(inplace=True)

    print("Writing dataframes to csv")
    # df_profile.to_csv("../raw_data/profile.csv", index=False)
    df_experience.to_csv("../raw_data/experience.csv", index=False)
    # df_education.to_csv("../raw_data/education.csv", index=False)
    # df_certification.to_csv("../raw_data/certification.csv", index=False)
    # df_courses.to_csv("../raw_data/courses.csv", index=False)
