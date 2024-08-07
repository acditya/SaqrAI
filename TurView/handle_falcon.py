from ai71 import AI71
import ast
import random
import turview_report as tr

AI71_BASE_URL = "https://api.ai71.ai/v1/"
# AI71_API_KEY = "api71-api-cbdf95af-ec38-4f97-8d7e-cb2ec3823f46" # Adi 1
AI71_API_KEY = "api71-api-52cc69d3-4619-425f-b618-cc53d3e59f37" # Adi 2

class FalconChatbot:
    def __init__(self, cv_text, job_desc_text, name=None, TurView: bool = True):
        print(f"Initializing FalconChatbot with TurView={TurView}")

        self.client = AI71(api_key=AI71_API_KEY)
        self.name = name
        self.question_messages = [{"role": "system", "content": """You are an interview chatbot, called TurViewBot. 
                          You will be passed a CV and a job description, and you will generate 5 interview questions based on them.
                          3 questions should be behavioral, and 2 questions should be technical.
                          """}] if TurView else []
        self.answer_messages = [{"role": "system", "content": """You are an interview chatbot, called TurViewBot. 
                          You will be passed 5 questions and you will generate the ideal answers to them.
                          """}] if TurView else []
        self.report_messages = [{"role": "system", "content": """You are an interview chatbot, called TurViewBot. 
                          You will be passed 5 questions, 5 ideal answers, and 5 candidate answers.
                          You will compare the candidate's answers to the ideal answers and provide a score and comment for each.
                          """}] if TurView else []
        self.model = "tiiuae/falcon-180B-chat" # tiiuae/falcon-40b-instruct, tiiuae/falcon-40b, tiiuae/falcon-7b-instruct, tiiuae/falcon-7b
        self.cv = cv_text
        self.job_desc = job_desc_text
        self.streaming = True
        self.questions = self.get_questions() if TurView else None
        self.answers_from_user = []
        self.answers_from_llm = []
        self.results = []
        self.greetings = "Hello! I am Ter View Bot and I will be interviewing you today based on your uploaded resume and chosen job description, good luck!"

        # Fillers in Between Each Question --> 100 Fillers
        self.fillers = [ 
            "That's interesting. Let's move on to the next question.",
            "Great, thank you for that. Here's the next question.",
            "I appreciate your response. Now, onto the next question.",
            "Thanks for sharing. Let's proceed with the next question.",
            "Good to know. Here's another question for you.",
            "Thank you for your answer. Let's continue.",
            "Alright, let's move to the next question.",
            "Thanks for that. Here's the next question.",
            "I see. Let's go to the next question.",
            "Appreciate your input. Next question coming up.",
            "Got it. Now, let's move on.",
            "Thanks for your response. Next question.",
            "Understood. Let's proceed.",
            "Okay, let's continue with the next question.",
            "Thank you. Here's another question.",
            "Great, let's move forward.",
            "Thanks for that. Moving on.",
            "I appreciate that. Next question.",
            "Alright, let's continue.",
            "Thanks for sharing. Next question.",
            "Good, let's proceed.",
            "Thank you. Let's move on.",
            "Got it. Next question.",
            "Appreciate your answer. Moving on.",
            "Okay, let's go to the next question.",
            "Thanks for your input. Next question.",
            "Understood. Moving forward.",
            "Alright, let's proceed.",
            "Thank you for that. Next question.",
            "Great, let's continue.",
            "Thanks for sharing. Moving on.",
            "Good to know. Next question.",
            "Thank you. Let's proceed.",
            "Got it. Moving on.",
            "Appreciate your response. Next question.",
            "Okay, let's continue.",
            "Thanks for that. Next question.",
            "Understood. Let's move on.",
            "Alright, let's go to the next question.",
            "Thank you for your answer. Moving on.",
            "Great, let's proceed.",
            "Thanks for sharing. Next question.",
            "Good, let's continue.",
            "Thank you. Moving on.",
            "Got it. Next question.",
            "Appreciate your input. Let's proceed.",
            "Okay, let's move forward.",
            "Thanks for your response. Next question.",
            "Understood. Moving on.",
            "Alright, let's continue.",
            "Thanks for that. Here's another question.",
            "I appreciate your insight. Let's move on.",
            "Thank you for sharing. Next question.",
            "That's helpful. Let's proceed.",
            "Thanks for that. Moving forward.",
            "I see. Let's continue.",
            "Good answer. Next question.",
            "Thank you for your thoughts. Let's move on.",
            "Alright, let's go ahead.",
            "Thanks for your input. Moving on.",
            "Understood. Let's continue.",
            "Okay, let's proceed.",
            "Thanks for sharing. Let's move forward.",
            "I appreciate your response. Next question.",
            "Great, let's go to the next question.",
            "Thank you for that. Moving on.",
            "Good, let's continue.",
            "Thanks for your answer. Next question.",
            "Alright, let's move forward.",
            "Thank you for your input. Let's proceed.",
            "Got it. Let's continue.",
            "Thanks for sharing. Moving forward.",
            "I see. Next question.",
            "Appreciate your response. Let's move on.",
            "Okay, let's go ahead.",
            "Thanks for that. Next question.",
            "Understood. Let's move forward.",
            "Alright, let's continue.",
            "Thank you for your answer. Next question.",
            "Great, let's proceed.",
            "Thanks for sharing. Moving on.",
            "Good to know. Next question.",
            "Thank you. Let's continue.",
            "Got it. Moving on.",
            "Appreciate your input. Next question.",
            "Okay, let's proceed.",
            "Thanks for that. Next question.",
            "Understood. Let's move on.",
            "Alright, let's go to the next question.",
            "Thank you for your answer. Moving on.",
            "Great, let's continue.",
            "Thanks for sharing. Next question.",
            "Good, let's proceed.",
            "Thank you. Moving on.",
            "Got it. Next question.",
            "Appreciate your input. Let's proceed.",
            "Okay, let's move forward.",
            "Thanks for your response. Next question.",
            "Understood. Moving on."
        ]

    def get_question_response(self, prompt):
        self.question_messages.append({"role": "user", "content": prompt}) 

        response = self.client.chat.completions.create(
            model="tiiuae/falcon-180b-chat",
            messages=self.question_messages,
        )

        text = response.choices[0].message.content


        print(f"Tokens Used: {response.usage}\n")
        print(text + "\nEND OF RESPONSE\n")

        self.question_messages.append({"role": "assistant", "content": text})

        return text


    def get_answer_response(self, prompt):
        self.answer_messages.append({"role": "user", "content": prompt}) 

        response = self.client.chat.completions.create(
            model="tiiuae/falcon-180b-chat",
            messages=self.answer_messages,
        )

        text = response.choices[0].message.content

        print(f"Tokens Used: {response.usage}\n")
        print(text + "\nEND OF RESPONSE\n")

        self.answer_messages.append({"role": "assistant", "content": text})

        return text


    def get_report_response(self, prompt):
        self.report_messages.append({"role": "user", "content": prompt}) 

        response = self.client.chat.completions.create(
            model="tiiuae/falcon-180b-chat",
            messages=self.report_messages,
        )

        text = response.choices[0].message.content

        tokens = 0

        print(f"Tokens Used: {response.usage}\n")
        print(text + "\nEND OF RESPONSE\n")

        self.report_messages.append({"role": "assistant", "content": text})

        return text
    

    def get_questions(self):
        prompt = f"""
            CV: {self.cv}
            Job Description: {self.job_desc}

            Generate 5 interview questions: 3 behavioral and 2 technical, based on this CV and Job description in this format so i can parse it in Python: ["question1", "question2", "question3", "question4", "question5"].
            """
        
        response = self.get_question_response(prompt)

        if "User:" in response:
            print("Found User: in Response")
            response = response.replace("User:", "").strip()

        else:
            response = response.strip()

        return ast.literal_eval(response)


    def get_llm_answer(self, question):
        prompt = f"""
            Question: {question}
            Generate the ideal answer to this interview question in no more than 3 sentences in string format so I can parse it in Python.
            """
        
        response = self.get_answer_response(prompt)

        if "User:" in response:
            print("Found User: in Response")
            response = response.replace("User:", "").strip()
        else:
            response = response.strip()

        return ast.literal_eval(response)
    
    def set_ideal_answers(self):
        self.answers_from_llm = [self.get_llm_answer(question) for question in self.questions]

    def analyze_answers(self):
        for question, ideal_answer, answer in zip(self.questions, self.answers_from_llm, self.answers_from_user):
            prompt = f"""
                Question: {question}
                Ideal Answer: {ideal_answer}
                Candidate Answer: {answer}

                Return a Score (1-10) and comment (pros and cons) for the candidate answer based on question and ideal answer.
                Format for Python: (score, "comment").
                """
            response = self.get_report_response(prompt)

            if "User:" in response:
                print("Found User: in Response")
                response = response.replace("User:", "").strip()

            else:
                response = response.strip()

            self.results.append(ast.literal_eval(response))


    def insert_user_answer(self, answer_as_text):
        self.answers_from_user.append(answer_as_text)


    def get_filler(self):
        return random.choice(self.fillers)


    def get_report(self):
        turview_report = tr.TurViewReport(name=self.name, job_desc=self.job_desc, questions=self.questions, ideal_answers=self.answers_from_llm, client_answers=self.answers_from_user, results=self.results)

        return turview_report
    

if __name__ == "__main__":
    chatbot = FalconChatbot(cv_text="""SULTAN WALEED ALHOSANI
                                    alhosani909@gmail.com | +971 56 757 7346 | Abu Dhabi, UAE
                                    EDUCATION 
                                    ADNOC Technical Academy Abu Dhabi, UAE
                                    Diploma in Process Operation 2021
                                    • Coursework: Common Core, Petroleum Core, Specialization Core, OJT, H2S Awareness Escape — Level 2
                                    Sa’ad Bin Mo’ath School Abu Dhabi, UAE
                                    Secondary School Certificate 2015
                                    • GPA: 95.7%
                                    WORK EXPERIENCE 
                                    ADNOC Technical Academy Abu Dhabi, UAE
                                    Start-up and Shutdown Supervisor 2018–2019
                                    • Supervised start-up and shutdown processes for four plants, ensuring adherence to all safety procedures.
                                    • Managed operations at the Wellhead.
                                    • Operated the Oil Plant.
                                    • Handled the Gas Dehydration Unit.
                                    • Controlled the Gas Sweetening Unit.
                                    Olympics World Summer Games Abu Dhabi, UAE
                                    Participant March 2019
                                    • Actively engaged in various competitions, enhancing team-building and discipline skills.
                                    • Demonstrated commitment and enthusiasm in representing the institution.
                                    • Gained experience in international sporting events.
                                    SKILLS AND ADDITIONAL TRAINING 
                                    1. Supervised start-up and shutdown processes
                                    2. Managed operations at the Wellhead
                                    3. Operated the Oil Plant
                                    4. Handled the Gas Dehydration Unit
                                    5. Controlled the Gas Sweetening Unit
                                    6. Executed PIGGING operations, including both Receiver and Launcher
                                    7. Conducted choke changes successfully
                                    • H2S Awareness Escape — Level 2
                                    • PET Certificate Level B1""",
    job_desc_text="""Job Title: Process Operations Supervisor

                    Location: Abu Dhabi, UAE

                    Company: Al Noor Energy Solutions

                    About the Company:
                    Al Noor Energy Solutions is a leading provider of innovative energy solutions specializing in the oil and gas industry. Our commitment to safety, efficiency, and sustainability drives our operations, and we pride ourselves on delivering top-notch services to our clients.

                    Job Description:

                    Overview:
                    Al Noor Energy Solutions is seeking a highly skilled and experienced Process Operations Supervisor to oversee and manage the start-up and shutdown processes of our plants. The ideal candidate will have a strong background in process operations, particularly within the oil and gas industry, and demonstrate a commitment to safety and efficiency.

                    Key Responsibilities:

                    Supervise the start-up and shutdown processes for multiple plants, ensuring strict adherence to safety protocols and procedures.
                    Manage operations at the wellhead, including monitoring and controlling equipment to maintain optimal performance.
                    Operate and oversee the Oil Plant, Gas Dehydration Unit, and Gas Sweetening Unit to ensure seamless and efficient operations.
                    Execute PIGGING operations, including both Receiver and Launcher, to maintain pipeline integrity and flow efficiency.
                    Conduct choke changes and manage pressure control devices to optimize production rates and ensure safety.
                    Coordinate with the maintenance team to schedule and perform regular inspections and preventive maintenance on all operational equipment.
                    Develop and implement operational procedures and guidelines to enhance efficiency and safety in all processes.
                    Provide training and guidance to junior staff and ensure compliance with all health, safety, and environmental regulations.
                    Participate in safety drills and H2S awareness programs to maintain a high level of preparedness among all team members.
                    Qualifications:

                    Diploma in Process Operation or a related field.
                    Minimum of 3 years of experience in process operations within the oil and gas industry.
                    Proven experience in supervising start-up and shutdown processes.
                    Strong knowledge of wellhead operations, oil plant operations, gas dehydration, and gas sweetening.
                    Proficiency in executing PIGGING operations and conducting choke changes.
                    Certification in H2S Awareness Escape — Level 2.
                    Excellent problem-solving skills and the ability to make sound decisions under pressure.
                    Strong communication and leadership skills.
                    Skills:

                    Supervision of start-up and shutdown processes
                    Wellhead operations management
                    Oil plant operation
                    Gas dehydration unit operation
                    Gas sweetening unit operation
                    PIGGING operations (Receiver and Launcher)
                    Choke changes
                    H2S Awareness Escape — Level 2
                    PET Certificate Level B1
                    Additional Information:

                    Competitive salary and benefits package.
                    Opportunities for career advancement and professional development.
                    Collaborative and dynamic work environment.""",

                    name="Sultan Waleed Alhosani",)

    print(chatbot.questions)


    for question in chatbot.questions:
        answer = chatbot.get_llm_answer(question=question)
        print(f"Question: {question}\nAnswer: {answer}")
        chatbot.answers_from_llm.append(answer)
    
    chatbot.answers_from_user = chatbot.answers_from_llm
    chatbot.set_ideal_answers()
    chatbot.analyze_answers()


    tr = chatbot.get_report()
    tr.write_document("test.docx")
    print(chatbot.results)