import ast
from sqlite3 import DataError
from docxtpl import DocxTemplate
import docx2txt
from docx2pdf import convert
from typing import Optional
import os
from PyPDF2 import PdfReader
from ai71 import AI71
import time

AI71_API_KEY = "api71-api-cbdf95af-ec38-4f97-8d7e-cb2ec3823f46"
client = AI71(AI71_API_KEY)

global messages
messages = [
    {"role": "system", "content": "You are a CV formatting assistant. Improve the English grammar and spelling of a given CV and return the sections as Python 3 data types."}
]

def talk_to_model(input_text: str) -> str:
    global messages

    messages.append({"role": "user", "content": input_text})

    response = client.chat.completions.create(
        model="tiiuae/falcon-40b-instruct",
        messages=messages,
    )

    text = response.choices[0].message.content

    if "User:" in text:
        "Found 'User:' in Text"
        text = text.replace("User:", "").strip()
    else:
        text = text.strip()

    print(f"Tokens Used: {response.usage}\n")
    print(text + "\nEND OF RESPONSE\n")

    messages.append({"role": "assistant", "content": text})

    return text

# Define the Classes for the Resume
class Header:
    def __init__(self, email: str,  location: str, name: str, phone: str, github: Optional[str] = None, linkedin: Optional[str] = None):
        self.email = email
        self.github = github
        self.linkedin = linkedin
        self.location = location 
        self.name = name
        self.phone = phone

    def __str__(self):
        return f"Name: {self.name}, Email: {self.email}, Phone: {self.phone}, Location: {self.location}, LinkedIn: {self.linkedin}, Github: {self.github}"

class Project:
    def __init__(self, date: str, details: list[str], location: str, title: str, position: str): 
        self.date = date
        self.details = details
        self.location = location
        self.title = title
        self.position = position
    
    def __str__(self):
        return f"Title: {self.title}, Position: {self.position}, Date: {self.date}, Location: {self.location}, Details: {self.details}"
        
class WorkAndLeadershipExperience:
    def __init__(self, company: str, date: str, details: list[str], location: str, position: str): 
        self.company = company
        self.date = date
        self.details = details
        self.location = location
        self.position = position

    def __str__(self):
        return f"Company: {self.company}, Position: {self.position}, Date: {self.date}, Location: {self.location}, Details: {self.details}"

class EducationExperience:
    def __init__(self, coursework:list[str], date: str, details: list[str], location: str, major: str, university: str, GPA: str):  
        self.coursework = coursework
        self.date = date
        self.details = details
        self.gpa = GPA
        self.location = location
        self.major = major
        self.university = university
        if GPA:
            self.gpa_hidden = GPA
        else:
            self.gpa_hidden = "N/A"

    def __str__(self):
        return f"University: {self.university}, Location: {self.location}, Date: {self.date}, Major: {self.major}, GPA: {self.gpa_hidden}, Details: {self.details}, Coursework: {self.coursework}"

    @property
    def gpa(self):
        return self._gpa
    
    @gpa.setter
    def gpa(self, gpa):
        if gpa:    
            if float(gpa) >= 3.2 and float(gpa) <= 5.0:
                self._gpa = gpa
            elif float(gpa) >= 90.0 and float(gpa) <= 100.0: # It is a percentage (above 90%, only show percentages above 90%)
                self._gpa = gpa + "%"
            else:
                self._gpa = ""

class Skills: 
    def __init__(self, skillset: list[str]): 
        self.skillset = skillset

    def __str__(self):
        return f"Skillset: {self.skillset}"

# Combines Everything Together To Create A Resume
class Resume:
    def __init__(self, education: list[EducationExperience], header: Header, work: list[WorkAndLeadershipExperience], skills=None):
        self.education = education
        self.header = header
        self.skills = skills
        self.work = work

    def __str__(self):
        education_str = ', '.join([education.__str__() for education in self.education]) if self.education else ''
        work_str = ', '.join([work.__str__() for work in self.work]) if self.work else ''
        projects_str = ', '.join([project.__str__() for project in self.projects]) if self.projects else ''
        leadership_str = ', '.join([lship.__str__() for lship in self.lship]) if self.lship else ''
        skills_str = self.skills.__str__() if self.skills else ''
        
        return f"Header: {self.header.__str__()}, Education: {education_str}, Work: {work_str}, Projects: {projects_str}, Leadership: {leadership_str}, Skills: {skills_str}"
    
    def write_document(self, template_path: str = r"Docxtpl Templates/TurView Docxtpl Compatible CV Template.docx", output_path: str = r"Docxtpl Templates") -> None:
        # Load the template
        doc = DocxTemplate(template_path)

        # Create context from the provided data
        context = {
            "header": self.header,
            "education": self.education,
            "work": self.work,
            "skills": self.skills
        }

        # Render and Save the Document
        doc.render(context)
        doc.save(output_path)
        convert(output_path, output_path.replace(".docx", ".pdf"))

def cv_formatter(cv_txt: str) -> Resume:
    # 1. Initialize CV Writer
    talk_to_model(f"This is the CV to Upgrade: {cv_txt}")
    
    # 2. Format it Section by Section
    queries = {
        "header": "Extract the Name, Email, Phone, Location, and LinkedIn from the CV as ['Name', 'Email', 'Phone', 'Location', 'LinkedIn']. If a field is empty, return an empty string for that field. If the entire section is empty, return []. Return only the list.",
        "education": "Extract ONLY one education experience from the CV as ['University Name', 'Location', 'Dates of Enrollment', 'Major', 'GPA', 'Coursework', 'Brief details']. Return only the list.",
        "work": "Extract ONLY one work experience from the CV as ['Company', 'Position', 'Location', 'Dates of Work', 'Two brief sentences about the work experience']. Return only the list.",
        "skills": "Be creative and come up with or extract skills from the CV as ['skill1', 'skill2', ...]. Return only the list."
    }

    for key in queries:
        # Query the API for the Formatted Section
        print(f"Current key is {key}")
        response = talk_to_model(queries[key])
        
        # Ensure the extracted part is of valid Pythonic syntax
        try:
            queries[key] = ast.literal_eval(response)  # Convert Literal String to Pythonic Datatype
        except SyntaxError as e:
            print(f"SyntaxError: {e}")
            print(f"Response was: {response}")
            queries[key] = None  # Handle the error or set a default value

        print(f"{key}: {response}")

    # 3. Create Each Individual Section as an Object
    print("Formulating Header Section") 
    if queries["header"]:
        header = Header(name = queries["header"][0].upper(),
                        email = queries["header"][1],
                        phone = queries["header"][2],
                        location = queries["header"][3],
                        linkedin = queries["header"][4]
                        )
    else:
        header = None
        
    print("Formulating Education Section")
    if queries["education"]:
        # education = []
        # for educ in queries["education"]:
        education = EducationExperience(university = queries["education"][0],
                                    location = queries["education"][1],
                                    date = queries["education"][2],
                                    major = queries["education"][3],
                                    GPA = queries["education"][4],
                                    coursework = queries["education"][5],
                                    details = queries["education"][6])
    else:
        education = None
        
    print("Formulating Work Section")
    if queries["work"]:
        # work = []
        # for work_exp in queries["work"]:
        work = WorkAndLeadershipExperience(company = queries["work"][0],
                                        position = queries["work"][1],
                                        date = queries["work"][2],
                                        location = queries["work"][3],
                                        details = queries["work"][4])
            
    else:
        work = None    
        
    print("Formulating Skills Section")
    if queries["skills"]:
        skills = Skills(skillset = queries["skills"])
    else:
        skills = None

    print("Returning Resume Object to Function Caller")
    # 4. Arrange all Objects into a Single Formatted Resume Object and reutrn to Caller
    return Resume(header = header, work = work, education = education, skills = skills)


# Extracts Text from Unformatted .DOCX, .PDF, and .RTF Files.
def extract_text(file_path) -> str:
    if os.path.exists(file_path):
        _, file_type = os.path.splitext(file_path)

        temp_filepath = file_path

        text = ""

        # Handle Word Docx Documents
        if file_type == ".docx" or file_type == ".rtf":
            text = docx2txt.process(temp_filepath)

        # Handle PDFs
        elif file_type == ".pdf":
            reader = PdfReader(temp_filepath)
            for page in reader.pages:
                text += page.extract_text()
        else:
            print("File is not Supported. Please Provide a .DOCX, .PDF, or .RTF File.")

        if text:
            return text
        raise DataError("Couldn't Extract Text.")
    
    raise FileNotFoundError(f"Couldn't Find the File. {file_path}")

if __name__ == "__main__":
    resume = cv_formatter(extract_text(r"Docxtpl Templates\Formatted CVs\Ahmed Almaeeni CV - Civil & Transportation Engineer --.pdf"))
    resume.write_document()
