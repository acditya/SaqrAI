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
        {"role": "system", "content": "You are a CV formatting assistant that will intake a CV, upgrade its English grammar and spelling, and return parts of it back as Python 3 datatypes."}
]

def talk_to_model(input_text: str) -> str:
    global messages

    messages.append({"role": "user", "content": input_text})

    response = client.chat.completions.create(
        model="tiiuae/falcon-40b-instruct",
        messages=messages,
    ).choices[0].message.content

    messages.append({"role": "assistant", "content": response})

    return response


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
        return f"Skillset: {self.skillset}, Training: {self.training}"

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
    
    def write_document(self, template_path: str = r"TurView/Docxtpl Templates/TurView Docxtpl Compatible CV Template.docx", output_path: str = r"TurView/Docxtpl Templates") -> None:
        # Load the template
        doc = DocxTemplate(template_path)

        output_path = os.path.join(output_path, f"{self.header.name} CV.docx")

        # Create context from the provided data
        context = {
            "header": self.header,
            "education": self.education,
            "work": self.work
            # "skills": self.skills
        }

        # Render and Save the Document
        doc.render(context)
        doc.save(output_path)
        convert(output_path, output_path.replace(".docx", ".pdf"))

def cv_formatter(cv_txt: str) -> Resume:
    # 1. Initialize CV Writer
    talk_to_model(f"This is the CV to Upgrade: {cv_txt}")
    
    # 3. Format it Section by Section
    queries = {
        "header": "Return a list of 6 strings that include this person's Name, Email, Phone, Location, LinkedIn, and Github as a list of strings ['Name', 'Email', 'Phone', 'Location', 'LinkedIn', 'Github']. You will typically find this at the top of the unformatted CV. If any of these fields are empty, return an empty string for that field. Be smart, the CV may not be labelled very well so find the section that matches this. If this entire section is empty, just return one big empty list: []. Make sure to close all parentheses properly. Do not return anything except the list. no extra words at all",
        "education": "From the CV, extract only one education experience as a list I will now describe such that I can parse it in Python ['University Name 1', 'Location', 'Dates of Enrollment', 'Major', 'GPA', 'Coursework', 'Brief sentence explaining some details']. Stick to this data type, do not return anything else. Be efficient in filling out these fields.",
        "work": "From the CV, extract only one work experience as a list I will now describe such that I can parse it in Python ['Company', 'Position 1', 'Location', 'Dates of Work', 'very short sentence explaining this work experience'] Stick to this data type, do not return anything else. Be efficient in filling out these fields."
        # "skills": "From the CV, extract one word/phrase skills as a list of string I will now describe such that I can parse it in Python. ['skill1', 'skill2', ...]. Stick to this data type, do not return anything else. Be efficient in filling out these fields."
    }

    for key in queries:
        # Query the API for the Formatted Section
        print(f"Current key is {key}")
        response = talk_to_model(queries[key])
        if "User:" in response:
            formatted_query_data = response.replace("User:", "").strip()
        else:
            formatted_query_data = response.strip()
        
        # Ensure the extracted part is valid Python syntax
        try:
            queries[key] = ast.literal_eval(formatted_query_data)  # Convert Literal String to Pythonic Datatype
        except SyntaxError as e:
            print(f"SyntaxError: {e}")
            print(f"Response was: {formatted_query_data}")
            queries[key] = None  # Handle the error or set a default value

        print(f"{key}: {formatted_query_data}")

    # 4. Create Each Individual Section as an Object
    print("Formulating Header Section") 
    if queries["header"]:
        header = Header(name = queries["header"][0].upper(),
                        email = queries["header"][1],
                        phone = queries["header"][2],
                        location = queries["header"][3],
                        linkedin = queries["header"][4],
                        github = queries["header"][5])
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
        
    # print("Formulating Skills Section")
    # if queries["skills"]:
    #     skills = Skills(skillset = queries["skills"])
    # else:
    #     skills = None

    print("Returning Resume Object to Function Caller")
    # Arrange all Objects into a Single Formatted Resume Object and reutrn to Caller
    return Resume(header = header, work = work, education = education)

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
    resume = cv_formatter(extract_text(r"TurView\Docxtpl Templates\Formatted CVs\Formatted_h-1995-alameri-gmail-com.pdf"))
    resume.write_document()

# print(talk_to_model(f"This is my CV: {extract_text(r'TurView/Docxtpl Templates/Formatted CVs/Ahmed Almaeeni CV - Civil & Transportation Engineer --.pdf')}")) 

# print(talk_to_model("From the CV, extract a list I will now describe such that I can parse it in Python (one sublist in the MASTER list of lists for each education) [['University Name 1', 'Location', 'Dates of Enrollment', 'Major', 'GPA', 'Coursework', 'Details']]. Stick to this data type, do not return anything else. Be efficient in filling out these fields."))
