#!/usr/bin/env python

# import csv
# import fuzzywuzzy.fuzz as fuzz
# import Levenshtein
import json
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Float, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from sqlalchemy.dialects.sqlite import JSON

# Load the data from JSON
# with open('./../../../../archives/cleaned_companies_data.json', 'r') as file:
#     data = json.load(file)

# Create the database
engine = create_engine('sqlite:///database.db', echo=False)
Base = declarative_base()


class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    positions = relationship('OldPosition', back_populates='company')


class OldPosition(Base):
    __tablename__ = 'old_positions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    company = relationship('Company', back_populates='positions')


class Major(Base):
    __tablename__ = 'majors'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)


class CoopCycle(Base):
    __tablename__ = 'coop_cycles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)


class OldCoopSalary(Base):
    __tablename__ = 'old_coop_salaries'

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    position_id = Column(Integer, ForeignKey('positions.id'), nullable=False)
    cycle_id = Column(Integer, ForeignKey('coop_cycles.id'), nullable=False)
    salary_per_hour = Column(Float, nullable=False)
    hours_per_week = Column(Integer, nullable=False)
    experience = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)


class CoopSalary(Base):
    __tablename__ = 'coop_salaries'

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_position_id = Column(
        Integer,
        ForeignKey('companies_positions.id'),
        nullable=False
    )
    cycle_id = Column(
        Integer,
        ForeignKey('coop_cycles.id'),
        nullable=False
    )
    salary_per_hour = Column(Float, nullable=False)
    hours_per_week = Column(Integer, nullable=False)
    experience = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)


class UniquePosition(Base):
    __tablename__ = 'unique_positions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False, unique=True)
    position_ids = Column(JSON, nullable=False)


class Position(Base):
    __tablename__ = 'positions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)


class CompaniesPositions(Base):
    __tablename__ = 'companies_positions'
    __table_args__ = (
        UniqueConstraint(
            'company_id',
            'position_id',
            name='_company_position_uc'
        ),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    position_id = Column(Integer, ForeignKey('positions.id'), nullable=False)


def create_company_salary(session):
    ocs = session.query(OldCoopSalary).all()

    for oc in ocs:
        unique_positions = session.query(UniquePosition).all()

        full = {}
        for up in unique_positions:
            for oid in up.position_ids:
                full[oid] = up.id

        cp = session.query(CompaniesPositions).filter_by(
            company_id=oc.company_id,
            position_id=full[oc.position_id]
        ).first()

        session.add(
            CoopSalary(
                company_position_id=cp.id,
                salary_per_hour=oc.salary_per_hour,
                cycle_id=oc.cycle_id,
                hours_per_week=oc.hours_per_week,
                experience=oc.experience,
                year=oc.year
            )
        )


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

create_company_salary(session)

session.commit()
session.close()

# def create_positions_from_unique(session):
#     print("pass")
#     unique_positions = session.query(UniquePosition).all()
#     for up in unique_positions:
#         new_position = Position(id=up.id, title=up.title)
#         session.add(new_position)


# def create_companies_positions(session):
#     unique_positions = session.query(UniquePosition).all()
#     old_positions = session.query(OldPosition).all()
#     # print(old_positions[0].id)
#
#     full = {}
#     for up in unique_positions:
#         for oid in up.position_ids:
#             full[oid] = up.id
#     #
#     for op in old_positions:
#         uid = full[op.id]
#         new_companies_positions = CompaniesPositions(
#             company_id=op.company_id,
#             position_id=uid
#         )
#         session.add(new_companies_positions)
#         session.commit()

# create_positions_from_unique(session)
# create_companies_positions(session)


# def normalize_title(title):
#     # Strip white spaces and remove 'coop' if present at the end
#     title = title.strip()
#     title = re.sub(r'\s*co.?op.?$', '', title,
#                    flags=re.IGNORECASE).strip()
#     title = re.sub(r'\s*intern.?$', '', title, flags=re.IGNORECASE).strip()
#     return title
#
#
# def create_unique_positions(session):
#     positions = session.query(Position).all()
#     title_to_ids = {}
#
#     for position in positions:
#         normalized_title = normalize_title(position.title)
#         if normalized_title not in title_to_ids:
#             title_to_ids[normalized_title] = []
#         title_to_ids[normalized_title].append(position.id)
#
#     for title, ids in title_to_ids.items():
#         new_unique_position = UniquePosition(title=title, position_ids=ids)
#         session.add(new_unique_position)
#
#     session.commit()

# create_unique_positions(session)

# Create the tables

# # Populate the majors table
# majors_list = [
#     "Accounting", "Air Force ROTC", "Animation & Visual Effects", "Architectural Engineering",
#     "Architectural Studies", "Architecture", "Army ROTC", "Art History", "Behavioral Economics, Business and Organizations",
#     "Behavioral Health Counseling", "Biological Sciences", "Biomedical Engineering", "Business", "Business Administration",
#     "Business Analytics", "Business Economics", "Business Undeclared", "Business and Engineering", "Chemical Engineering",
#     "Chemistry", "Chemistry-Biochemistry Concentration", "Civil Engineering", "Communication", "Computer Engineering",
#     "Computer Science", "Computing and Security Technology", "Construction Management", "Criminology and Justice Studies",
#     "Culinary Arts & Science", "Custom-Designed Major", "Dance", "Dance - Part-time Professional", "Data Science",
#     "Design and Merchandising", "Digital Media and Virtual Production", "Economic Analysis", "Economics", "Economics and Business",
#     "Economics and Data Science", "Economics and Mathematics", "Economics and Public Health", "Education: Non-Certification",
#     "Electrical Engineering", "Elementary Education", "Engineering", "Engineering Technology", "Engineering Undeclared",
#     "English, Literary Studies Concentration", "English, Secondary Education Concentration", "English, Writing Concentration",
#     "Entertainment and Arts Management", "Entrepreneurship & Innovation 3-year Option", "Entrepreneurship and Innovation",
#     "Environmental Engineering", "Environmental Science", "Environmental Studies and Sustainability", "Esport Business",
#     "Exercise Science", "Fashion Design", "Film & Television", "Finance", "First Year Exploratory Studies",
#     "Game Design & Production", "General Business", "General Humanities and Social Sciences", "General Studies", "Geoscience",
#     "Global Public Health", "Global Studies", "Graphic Design", "Health Data Analytics", "Health Sciences",
#     "Health Services Administration", "History", "Hospitality Management", "Human Development and Counseling", "Information Systems",
#     "Interior Design", "International Business", "International Business Co-Major", "Law", "Learning Sciences, Experience Design, and Technology",
#     "Legal Studies", "Management Information Systems", "Marketing", "Materials Science and Engineering", "Mathematical Statistics",
#     "Mathematics", "Mechanical Engineering & Mechanics", "Music Industry", "Navy ROTC", "Neuroscience", "Nursing",
#     "Nursing: RN-MSN Bridge Program", "Nutrition and Foods", "Operations and Supply Chain Management", "Organizational Management",
#     "Philosophy", "Philosophy, Politics and Economics", "Photography", "Physics", "Political Science", "Product Design", "Psychology",
#     "Public Health", "ROTC", "Real Estate Management and Development", "Science", "Screenwriting and Playwriting", "Sociology",
#     "Software Engineering", "Special Education", "Sport Business", "Sustainability and Innovation", "Teacher Education",
#     "Technology Innovation Management", "User Experience and Interaction Design", "Westphal Studies Program"
# ]
#
# for major in majors_list:
#     session.add(Major(name=major))
#
# # Populate the coop_cycle table
# coop_cycles_list = [
#     "Fall/Winter", "Winter/Spring", "Spring/Summer", "Summer/Fall"
# ]
#
# for cycle in coop_cycles_list:
#     session.add(CoopCycle(name=cycle))
#
# session.commit()

# Process CSV data using csv reader and populate coop_salaries table

# file_path = "./salary_pos.csv"
# with open(file_path, 'r') as file:
#     csv_reader = csv.DictReader(file)
#     for row in csv_reader:
#         company_name = row['Company']
#         position_title = row['Position']
#         c_id = row['c_id']
#         p_id = row['p_id']
#         salary_per_hour = float(row['Salary'])
#         hours_per_week = int(row['Hours'])
#         coop_year_name = row['Cycle']
#         experience = int(row['Experience'])
#         _year = int(row['Year'])
#
#         company = None
#         if c_id:
#             company = session.query(Company).filter_by(id=c_id).first()
#         else:
#             company = session.query(Company).filter_by(
#                 name=company_name).first()
#
#         if not company:
#             company = Company(name=company_name)
#             session.add(company)
#             session.commit()
#
#         position = None
#         if p_id:
#             position = session.query(Position).filter_by(
#                 id=p_id,
#                 company_id=company.id
#             ).first()
#         else:
#             position = session.query(Position).filter_by(
#                 title=position_title,
#                 company_id=company.id
#             ).first()
#
#         if not position:
#             position = Position(title=position_title, company_id=company.id)
#             session.add(position)
#             session.commit()
#
#         coop_cycle = session.query(CoopCycle).filter_by(
#             name=coop_year_name
#         ).first()
#
#         coop_salary = CoopSalary(
#             company_id=company.id,
#             position_id=position.id,
#             cycle_id=coop_cycle.id,
#             salary_per_hour=salary_per_hour,
#             hours_per_week=hours_per_week,
#             experience=experience,
#             year=_year
#         )
#
#         session.add(coop_salary)
#
# session.commit()
# session.close()

# for company_name, positions in data.items():
#     company = Company(name=company_name)
#     session.add(company)
#     session.flush()  # Ensure the company ID is generated
#
#     for position_title in positions:
#         position = Position(title=position_title, company_id=company.id)
#         session.add(position)

# Function to retrieve positions by company name
# def get_positions_by_company(company_name):
#     company = session.query(Company).filter_by(name=company_name).first()
#     if company:
#         return [position.title for position in company.positions]
#     else:
#         return []
#
#
# # Example usage
# company_name = "Rising Sun Presents"
# positions = get_positions_by_company(company_name)
# print(f"Positions at {company_name}: {positions}")
#
# # Close the session
# session.close()

# Commit the session
# session.commit()

# Close the session
# session.close()

# Function to retrieve and print companies with similar spellings
# def print_companies_and_similar_ids(company_list, threshold=80):
#     companies_in_db = session.query(Company).all()
#     for target_company in company_list:
#         for company in companies_in_db:
#             match_score = fuzz.partial_ratio(
#                 company.name.lower(), target_company.lower())
#             distance = Levenshtein.distance(
#                 company.name.lower(), target_company.lower())
#             if distance <= 5 or match_score >= 80:
#                 if target_company[0] == company.name[0]:
#                     print(f"Company: {target_company}")
#                     print(f"    Database Company: {
#                           company.name} | id: {company.id}")
#         input()
#         print("-----"*10)

# List of companies to search for
# companies_to_search = [
#     "Google", "Amazon Robotics", "Monarch Systems", "SIG", "Nintendo Platform Technology Development",
#     "Amazon", "Apollo Global Management", "Vanguard", "AVEVA", "SAP", "Comcast", "Monroe Energy",
#     "Oracle", "Apple", "Woodward McCoach", "JPMorgan Chase and Co", "Pratt & Whitney", "Medidata Solutions",
#     "Comcast Corporation", "Merck", "Blackrock", "Glenmeade", "Lockheed Martin", "Financial Research Associates",
#     "College Ave Student Loans", "Security Risk Advisors", "Davison Kempner", "Susquehanna International Group",
#     "TherapyNotes", "EMoney", "AstraZeneca", "Berkley Technology Services", "Exelon", "Century Thereapeutics",
#     "Raytheon", "Delve", "Secant Group", "Sparks Therapeutics", "Baltimore Gas and Electric", "Cigna",
#     "City of Philadelphia", "Accurate Tool Company", "WebstaurantStore", "Rhoads", "Holman", "Hologic",
#     "Leidos", "GSK", "OPEX", "Takachar", "Columbus Technologies", "VOX Funding", "Remington and Vernick Engineers",
#     "Hargrove Life Sciences", "Neuroflow", "Pfizer", "Wawa", "PJM Interconnection", "Mulhern and Kulp",
#     "Two Six Technologies", "Penn Mutual Life Insurance", "Johnson and Johnson", "Clark Associates/WebstaurantStore",
#     "National Board of Medical Examiners", "Aramark", "PECO Exelon", "Ametek PDS", "Curtiss-Wright", "Kiewit",
#     "Dorman", "STV", "FS Investments", "Moberg Analytics", "PECO", "Kulicke and Soffa", "Incyte", "Constellation",
#     "Teleflex", "Venerable", "West Pharmaceuticals", "EwingCole", "PSEG", "CHOP", "West Pharmaceutical Services",
#     "University of Pennsylvania", "Thermo Systems", "Fox Rothschild", "Simpletire", "Wharton School of Business",
#     "Pennoni", "Fluitron", "Colorcon", "Qfix/CQ Medical", "Estee Lauder Inc.", "Drexel Office of Institutional Advancement",
#     "MIAX", "Dometic", "ZeroEyes", "The Siegfried Group,", "Crayola", "Tokio Marine North America Services",
#     "Theory", "Adesis", "GeoStructures", "Springboard Collabrative", "Philadelphia Water Department", "Design Science",
#     "Drexel University (SOE)", "NAWCAD Lakehurst", "Blackstar Projects", "German Jumpstart", "northern children",
#     "AdMed, Inc.", "Brandywine Workshop and Archives", "Becton Dickinson Singapore - International Co-op",
#     "Music Play Patrol", "Nayko Naturals"
# ]
# print_companies_and_similar_ids(companies_to_search)

# Close the session
# session.close()

# print_companies_and_similar_ids(companies_to_search)

# Close the session
# session.close()
# _and_similar_ids(companies_to_search)

# Close the session
# session.close()

# print_companies_and_similar_ids(companies_to_search)

# Close the session
# session.close()
# _and_similar_ids(companies_to_search)

# Close the session
# session.close()

# print_companies_and_similar_ids(companies_to_search)

# Close the session
# session.close()
# _and_similar_ids(companies_to_search)

# Close the session
# session.close()

# print_companies_and_similar_ids(companies_to_search)

# Close the session
# session.close()
# _and_similar_ids(companies_to_search)

# Close the session
# session.close()

# print_companies_and_similar_ids(companies_to_search)

# Close the session
# session.close()
# _and_similar_ids(companies_to_search)

# Close the session
# session.close()

# print_companies_and_similar_ids(companies_to_search)

# Close the session
# session.close()
# _and_similar_ids(companies_to_search)

# Close the session
# session.close()

# print_companies_and_similar_ids(companies_to_search)

# Close the session
# session.close()
_and_similar_ids(companies_to_search)

# Close the session
# session.close()

# print_companies_and_similar_ids(companies_to_search)

# Close the session
# session.close()
_and_similar_ids(companies_to_search)

# Close the session
# session.close()

# print_companies_and_similar_ids(companies_to_search)

# Close the session
# session.close()
