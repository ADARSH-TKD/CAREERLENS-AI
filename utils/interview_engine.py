import re

QUESTION_BANK = {
    "Microsoft": [
        {"category":"OOP","question":"Explain the four pillars of OOP with a simple example.","keywords":["encapsulation","inheritance","polymorphism","abstraction"]},
        {"category":"DSA","question":"What is the difference between an array and a linked list?","keywords":["array","linked list","random access","insertion"]},
        {"category":"Java","question":"What is the difference between ArrayList and LinkedList in Java?","keywords":["arraylist","linkedlist","dynamic array","nodes"]},
        {"category":"DBMS","question":"What is normalization and why is it used in DBMS?","keywords":["normalization","redundancy","database","normal form"]},
        {"category":"OS","question":"What is the difference between a process and a thread?","keywords":["process","thread","memory","execution"]},
    ],
    "Google": [
        {"category":"DSA","question":"Explain the time complexity of binary search and why it is logarithmic.","keywords":["binary search","logarithmic","divide","sorted"]},
        {"category":"OOP","question":"What is polymorphism? Explain compile-time and runtime polymorphism.","keywords":["polymorphism","overloading","overriding","runtime"]},
        {"category":"DSA","question":"How would you detect a cycle in a linked list?","keywords":["cycle","linked list","slow","fast","floyd"]},
        {"category":"DBMS","question":"Explain an index in a database and one advantage and disadvantage.","keywords":["index","search","query","storage"]},
        {"category":"OS","question":"What is deadlock? Mention the four necessary conditions.","keywords":["deadlock","mutual exclusion","hold","wait","circular"]},
    ],
    "Amazon": [
        {"category":"DSA","question":"Explain how a hash map works at a high level.","keywords":["hash","bucket","key","value","collision"]},
        {"category":"DSA","question":"What is the difference between BFS and DFS?","keywords":["bfs","dfs","queue","stack","graph"]},
        {"category":"OOP","question":"Explain abstraction and encapsulation with examples.","keywords":["abstraction","encapsulation","implementation","data"]},
        {"category":"DBMS","question":"What is a primary key and how is it different from a foreign key?","keywords":["primary key","foreign key","unique","reference"]},
        {"category":"Behavioral","question":"Describe a technical project you are proud of and the challenge you solved.","keywords":["project","challenge","solution","result"]},
    ],
    "TCS": [
        {"category":"Java","question":"Explain method overloading and method overriding.","keywords":["overloading","overriding","compile","runtime"]},
        {"category":"DSA","question":"What is the difference between a stack and a queue?","keywords":["stack","queue","lifo","fifo"]},
        {"category":"SQL","question":"What is the difference between WHERE and HAVING?","keywords":["where","having","group","aggregate"]},
        {"category":"OOP","question":"What is inheritance and why is it useful?","keywords":["inheritance","parent","child","reuse"]},
        {"category":"Behavioral","question":"Tell me about a project where you had to learn something new.","keywords":["project","learning","challenge","result"]},
    ],
    "Infosys": [
        {"category":"Java","question":"What is exception handling in Java?","keywords":["exception","try","catch","finally"]},
        {"category":"DSA","question":"What is the time complexity of searching in a binary search tree in the average case?","keywords":["binary search tree","search","log","balanced"]},
        {"category":"DBMS","question":"What is a transaction in DBMS?","keywords":["transaction","acid","atomicity","consistency"]},
        {"category":"OOP","question":"Explain abstraction with a practical example.","keywords":["abstraction","interface","implementation"]},
        {"category":"Behavioral","question":"Why should we hire you for a software engineering role?","keywords":["skills","learning","problem solving","team"]},
    ],
    "Accenture": [
        {"category":"OOP","question":"Explain the difference between an abstract class and an interface.","keywords":["abstract class","interface","implementation","inheritance"]},
        {"category":"SQL","question":"What is a JOIN? Explain INNER JOIN and LEFT JOIN.","keywords":["join","inner join","left join","tables"]},
        {"category":"Networking","question":"What is the difference between HTTP and HTTPS?","keywords":["http","https","encryption","tls"]},
        {"category":"Cloud","question":"What is the difference between scalability and elasticity?","keywords":["scalability","elasticity","resources","demand"]},
        {"category":"Behavioral","question":"Tell me about a technical problem you solved and how you approached it.","keywords":["problem","approach","solution","result"]},
    ],
    "Deloitte": [
        {"category":"Consulting","question":"What is the difference between consulting and advisory roles in a tech firm?","keywords":["consulting","advisory","client","solutions","strategy"]},
        {"category":"SQL","question":"How would you optimize a slow-running SQL query?","keywords":["index","query plan","execution","optimization","join"]},
        {"category":"Cloud","question":"Explain the key differences between IaaS, PaaS, and SaaS.","keywords":["iaas","paas","saas","infrastructure","platform","software"]},
        {"category":"OOP","question":"What is the SOLID principle? Briefly explain each letter.","keywords":["single responsibility","open closed","liskov","interface segregation","dependency inversion"]},
        {"category":"Behavioral","question":"Describe a situation where you had to deliver a project under tight deadlines.","keywords":["deadline","prioritize","deliver","team","result"]},
    ],
    "Cognizant": [
        {"category":"Java","question":"What are the differences between HashMap and ConcurrentHashMap in Java?","keywords":["hashmap","concurrenthashmap","thread safe","synchronization","concurrent"]},
        {"category":"DSA","question":"Explain the concept of dynamic programming with an example.","keywords":["dynamic programming","memoization","subproblem","overlap","optimal"]},
        {"category":"DBMS","question":"What is the difference between DELETE, TRUNCATE, and DROP in SQL?","keywords":["delete","truncate","drop","rows","table","rollback"]},
        {"category":"Agile","question":"What is Agile methodology and how does a sprint work?","keywords":["agile","sprint","scrum","iteration","backlog","retrospective"]},
        {"category":"Behavioral","question":"Tell me about a time you worked with a difficult team member. How did you handle it?","keywords":["conflict","communication","collaboration","resolve","team"]},
    ],
    "LTIMindtree": [
        {"category":"Java","question":"Explain the concept of multithreading in Java and when you would use it.","keywords":["multithreading","thread","runnable","synchronized","concurrency"]},
        {"category":"DSA","question":"What is the difference between a min-heap and a max-heap?","keywords":["heap","min-heap","max-heap","priority queue","root"]},
        {"category":"Cloud","question":"What are microservices and what problems do they solve compared to monolithic applications?","keywords":["microservices","monolithic","independent","scalability","deployment","api"]},
        {"category":"DBMS","question":"What is an ORM and what are its advantages and disadvantages?","keywords":["orm","object relational mapping","hibernate","query","abstraction"]},
        {"category":"Behavioral","question":"Describe a project where you had to quickly adapt to a new technology.","keywords":["adapt","learn","technology","project","challenge"]},
    ],
    "Capgemini": [
        {"category":"Testing","question":"What is the difference between unit testing, integration testing, and system testing?","keywords":["unit test","integration test","system test","scope","level"]},
        {"category":"OOP","question":"What is method overriding and why is it important in OOP?","keywords":["overriding","runtime","polymorphism","parent","child"]},
        {"category":"Networking","question":"What is the OSI model? Name the seven layers.","keywords":["osi","physical","data link","network","transport","session","presentation","application"]},
        {"category":"SQL","question":"What are stored procedures in SQL and why are they useful?","keywords":["stored procedure","reusable","sql","database","performance"]},
        {"category":"Behavioral","question":"Give an example where you proactively identified and fixed a bug before it caused a production issue.","keywords":["bug","proactive","fix","production","testing"]},
    ],
    "Wipro": [
        {"category":"Java","question":"What is the difference between an interface and an abstract class in Java 8+?","keywords":["interface","abstract class","default method","java 8","implementation"]},
        {"category":"DSA","question":"Explain the working of quicksort and its average-case time complexity.","keywords":["quicksort","pivot","partition","average","o n log n"]},
        {"category":"DBMS","question":"What is denormalization and when would you use it?","keywords":["denormalization","performance","redundancy","read","query speed"]},
        {"category":"Cloud","question":"What is a REST API and what are the HTTP methods used?","keywords":["rest","api","get","post","put","delete","http","stateless"]},
        {"category":"Behavioral","question":"How do you prioritize your tasks when multiple deadlines overlap?","keywords":["prioritize","deadline","time management","organize","task"]},
    ],
    "PwC": [
        {"category":"Finance Tech","question":"What is the role of technology in modern auditing and compliance?","keywords":["audit","compliance","automation","data analytics","risk"]},
        {"category":"SQL","question":"Write a SQL query to find the second-highest salary from an employee table.","keywords":["subquery","max","salary","rank","limit","second"]},
        {"category":"Cloud","question":"How does cloud computing support data security and compliance requirements?","keywords":["cloud","security","compliance","encryption","access control"]},
        {"category":"OOP","question":"What is encapsulation and why is data hiding important?","keywords":["encapsulation","data hiding","private","public","access modifier"]},
        {"category":"Behavioral","question":"Describe a time you identified a process inefficiency and suggested an improvement.","keywords":["process","improvement","efficiency","suggest","impact"]},
    ],
    "IBM": [
        {"category":"AI/ML","question":"What is the difference between supervised, unsupervised, and reinforcement learning?","keywords":["supervised","unsupervised","reinforcement","label","reward","pattern"]},
        {"category":"Cloud","question":"What is IBM Cloud and how does it differ from AWS and Azure?","keywords":["ibm cloud","aws","azure","services","enterprise","hybrid"]},
        {"category":"DSA","question":"Explain the concept of a graph and give two real-world applications.","keywords":["graph","vertex","edge","social network","maps","application"]},
        {"category":"OS","question":"What is virtual memory and how does paging work?","keywords":["virtual memory","paging","page table","swap","physical memory"]},
        {"category":"Behavioral","question":"Tell me about a time you collaborated with cross-functional teams on a complex project.","keywords":["cross functional","collaborate","communication","outcome","team"]},
    ],
    "HCLTech": [
        {"category":"Java","question":"Explain the Java memory model. What is the difference between stack and heap memory?","keywords":["stack","heap","memory","jvm","garbage collection","object"]},
        {"category":"Networking","question":"What is the difference between TCP and UDP? When would you use each?","keywords":["tcp","udp","reliable","connection","streaming","protocol"]},
        {"category":"DBMS","question":"What are the ACID properties of a database transaction? Explain each.","keywords":["atomicity","consistency","isolation","durability","transaction","acid"]},
        {"category":"Cloud","question":"What is containerization and how does Docker differ from a virtual machine?","keywords":["docker","container","virtual machine","image","lightweight","os"]},
        {"category":"Behavioral","question":"Share an example of when you had to debug a complex issue in production.","keywords":["debug","production","root cause","logs","fix","impact"]},
    ],
    "Tech Mahindra": [
        {"category":"Telecom","question":"What is 5G and how does it differ from 4G LTE in terms of technical architecture?","keywords":["5g","4g","latency","bandwidth","mmwave","network slicing"]},
        {"category":"Java","question":"What are design patterns? Explain the Singleton and Factory patterns.","keywords":["design pattern","singleton","factory","creational","instance"]},
        {"category":"SQL","question":"What is an index in a database? What are clustered vs non-clustered indexes?","keywords":["index","clustered","non-clustered","search","b-tree","performance"]},
        {"category":"DSA","question":"Explain the difference between merge sort and bubble sort in terms of complexity.","keywords":["merge sort","bubble sort","o n log n","o n squared","comparison","efficiency"]},
        {"category":"Behavioral","question":"How do you keep your technical skills updated in a fast-changing technology landscape?","keywords":["learning","certifications","upskill","technology","courses","practice"]},
    ],
    "JP Morgan Chase": [
        {"category":"Finance Tech","question":"What is algorithmic trading and what role does low-latency programming play?","keywords":["algorithmic trading","latency","execution","order","market","performance"]},
        {"category":"DSA","question":"Explain how a priority queue works and where it is used in financial systems.","keywords":["priority queue","heap","order book","scheduling","latency"]},
        {"category":"Security","question":"What is SQL injection and how do you prevent it?","keywords":["sql injection","parameterized","prepared statement","input validation","security"]},
        {"category":"DBMS","question":"Explain the difference between OLTP and OLAP systems.","keywords":["oltp","olap","transaction","analytical","data warehouse","query"]},
        {"category":"Behavioral","question":"Describe how you would handle a situation where a production system goes down during peak trading hours.","keywords":["incident","production","response","escalate","recovery","priority"]},
    ],
    "Cisco": [
        {"category":"Networking","question":"What is the difference between a router, switch, and hub?","keywords":["router","switch","hub","layer","routing","broadcast"]},
        {"category":"Networking","question":"Explain how DNS works step by step.","keywords":["dns","domain","resolver","root","record","ip address"]},
        {"category":"Security","question":"What is a firewall and how does a stateful firewall differ from a stateless one?","keywords":["firewall","stateful","stateless","packet","connection","rules"]},
        {"category":"Cloud","question":"What is SD-WAN and why is it becoming popular in enterprise networking?","keywords":["sd-wan","software defined","wan","bandwidth","cloud","flexibility"]},
        {"category":"Behavioral","question":"Tell me about a time you diagnosed and resolved a complex network issue.","keywords":["network","diagnose","troubleshoot","resolution","tools","log"]},
    ],
    "BNP Paribas": [
        {"category":"Finance Tech","question":"What is risk management in banking and what role does technology play?","keywords":["risk","credit risk","market risk","technology","analytics","model"]},
        {"category":"SQL","question":"How would you design a database schema for a banking transaction system?","keywords":["schema","account","transaction","foreign key","balance","audit"]},
        {"category":"Security","question":"What is two-factor authentication and why is it critical in financial applications?","keywords":["2fa","authentication","otp","security","token","banking"]},
        {"category":"OOP","question":"What is the Repository pattern and why is it used in enterprise applications?","keywords":["repository","pattern","data access","abstraction","enterprise","layer"]},
        {"category":"Behavioral","question":"Describe a time when you ensured the quality and accuracy of financial data in a project.","keywords":["accuracy","validation","financial","data quality","testing","compliance"]},
    ],
    "KPIT Technologies": [
        {"category":"Embedded","question":"What is the difference between a microcontroller and a microprocessor?","keywords":["microcontroller","microprocessor","integrated","peripheral","cpu","embedded"]},
        {"category":"Automotive","question":"What is AUTOSAR and what problem does it solve in automotive software development?","keywords":["autosar","automotive","standard","software component","ecu","scalability"]},
        {"category":"C/C++","question":"What is a pointer in C and how does pointer arithmetic work?","keywords":["pointer","address","memory","arithmetic","dereference","c"]},
        {"category":"OS","question":"What is a Real-Time Operating System (RTOS) and how is it different from a general-purpose OS?","keywords":["rtos","real time","deterministic","scheduling","latency","priority"]},
        {"category":"Behavioral","question":"Tell me about a project where you worked on embedded systems or hardware-software integration.","keywords":["embedded","hardware","software","integration","firmware","project"]},
    ],
}

def get_questions(company):
    return QUESTION_BANK.get(company, QUESTION_BANK["Microsoft"])

def generate_jd_questions(jd_text: str, resume_text: str = "") -> list:
    """
    Generate interview questions dynamically from a pasted Job Description.
    Extracts tech keywords from the JD and maps them to curated questions.
    Falls back to generic behavioral + technical questions if keywords are sparse.
    """
    import re
    jd_lower = jd_text.lower()
    resume_lower = resume_text.lower()

    # Keyword → (category, question, keywords)
    _JD_KEYWORD_MAP = [
        ("python",        "Python",       "You mentioned Python in this role. What Python libraries have you used for data processing or automation?", ["python","library","pandas","numpy","automation"]),
        ("java",          "Java",         "The JD mentions Java. Explain the difference between an abstract class and an interface in Java.", ["abstract","interface","java","inheritance","class"]),
        ("machine learning","ML",         "This role involves ML. Explain how you would choose between two classification algorithms for a given dataset.", ["classification","model","accuracy","precision","recall","dataset"]),
        ("deep learning", "Deep Learning","The JD mentions deep learning. What is backpropagation and why is it important?", ["backpropagation","gradient","neural network","weights","loss"]),
        ("sql",           "SQL",          "The JD requires SQL. Write a query logic to find the top 3 salaries per department.", ["sql","group by","rank","partition","department","salary"]),
        ("nosql",         "NoSQL",        "The role mentions NoSQL. Compare MongoDB and a relational database for a high-read application.", ["nosql","mongodb","document","schema","scalability"]),
        ("react",         "React",        "This role uses React. Explain the difference between state and props in React.", ["state","props","component","react","re-render"]),
        ("node",          "Node.js",      "The JD mentions Node.js. How does the event loop work in Node.js?", ["event loop","non-blocking","async","callback","node"]),
        ("aws",           "Cloud/AWS",    "The JD requires AWS experience. What is the difference between S3, EC2, and Lambda?", ["s3","ec2","lambda","storage","compute","serverless"]),
        ("azure",         "Cloud/Azure",  "The role requires Azure. Explain Azure DevOps and its CI/CD pipeline capabilities.", ["azure","devops","pipeline","ci/cd","deployment"]),
        ("docker",        "DevOps",       "The JD mentions Docker. How does containerization improve deployment reliability?", ["docker","container","image","portability","deployment"]),
        ("kubernetes",    "DevOps",       "The role requires Kubernetes. Explain how Kubernetes manages pod scaling.", ["kubernetes","pod","replica","autoscaling","cluster"]),
        ("rest",          "API Design",   "The JD requires REST API experience. What are the HTTP methods and when would you use each?", ["get","post","put","delete","patch","rest","api"]),
        ("microservice",  "Architecture", "The role involves microservices. How do microservices communicate, and what are the failure handling strategies?", ["microservice","api gateway","circuit breaker","fault tolerance","communication"]),
        ("agile",         "Agile",        "The JD mentions Agile. Describe your experience with sprint planning, retrospectives, and daily standups.", ["agile","sprint","scrum","standup","retrospective","backlog"]),
        ("data",          "Data",         "This role is data-focused. How would you handle missing values and outliers in a real-world dataset?", ["missing values","outliers","imputation","preprocessing","cleaning"]),
        ("security",      "Security",     "The JD mentions security. What is OWASP and name three common vulnerabilities from the OWASP Top 10.", ["owasp","sql injection","xss","csrf","vulnerability","security"]),
        ("testing",       "QA",           "The role requires testing skills. What is the difference between unit, integration, and end-to-end testing?", ["unit test","integration","e2e","selenium","pytest","coverage"]),
        ("c++",           "C/C++",        "The JD requires C++. What is the difference between stack and heap memory allocation in C++?", ["stack","heap","pointer","memory","c++","allocation"]),
        ("golang",        "Go",           "The role mentions Go. What makes Go's goroutines different from OS threads?", ["goroutine","channel","concurrency","go","lightweight"]),
        ("nlp",           "NLP",          "The JD involves NLP. Compare TF-IDF and word embeddings for text classification.", ["tfidf","embedding","word2vec","transformer","tokenization"]),
        ("communication", "Behavioral",   "The JD emphasizes communication skills. Give an example of how you explained a complex technical concept to a non-technical stakeholder.", ["explain","stakeholder","communication","clarity","simplify"]),
        ("leadership",    "Behavioral",   "The role requires leadership. Describe a time you led a team through a technical challenge.", ["lead","team","challenge","decision","outcome"]),
        ("problem",       "Behavioral",   "The JD values problem-solving. Walk me through a difficult technical problem you solved and what approach you took.", ["problem","debug","root cause","solution","approach"]),
    ]

    questions = []
    used_categories = set()

    for kw, cat, question, kws in _JD_KEYWORD_MAP:
        if kw in jd_lower and cat not in used_categories:
            questions.append({"category": cat, "question": question, "keywords": kws, "is_jd": True})
            used_categories.add(cat)
        if len(questions) >= 8:
            break

    # Add resume-matched questions too
    _resume_extras = [
        ("project",     "Projects",  "Your resume mentions projects. Walk me through your most technically challenging project.", ["project","challenge","architecture","result","technology"]),
        ("intern",      "Experience","You have internship experience. What was the most valuable technical skill you developed during your internship?", ["internship","skill","learn","contribute","team"]),
        ("certif",      "Growth",    "You have certifications on your resume. How have these helped you in real project work?", ["certification","practical","applied","project","skill"]),
    ]
    for kw, cat, question, kws in _resume_extras:
        if kw in resume_lower and cat not in used_categories and len(questions) < 8:
            questions.append({"category": cat, "question": question, "keywords": kws, "is_jd": True})
            used_categories.add(cat)

    # Fallback generic questions if JD is too sparse
    if len(questions) < 3:
        questions += [
            {"category": "DSA",      "question": "Explain the difference between BFS and DFS and when you would use each.", "keywords": ["bfs","dfs","queue","stack","graph","traversal"], "is_jd": True},
            {"category": "OOP",      "question": "Explain the SOLID principles and give a real-world example of one.", "keywords": ["solid","single responsibility","open closed","dependency","interface"], "is_jd": True},
            {"category": "Behavioral","question": "Tell me about a time you had to learn a new technology quickly under a deadline.", "keywords": ["learn","deadline","fast","technology","challenge","result"], "is_jd": True},
        ]

    return questions[:8]


def generate_project_authenticity_question(first_name: str, project) -> dict:
    """
    Project Authenticity Probing:
    Asks increasingly specific questions about a claimed project in every interview,
    explicitly citing the project name from the candidate's resume.
    """
    raw_first = first_name.strip() if first_name else "there"
    c_name = raw_first.split()[0].capitalize() if raw_first.lower() != "there" else "there"

    if isinstance(project, dict):
        p_name = project.get("name", "Key Project")
        tech_stack = project.get("tech_stack", [])
    elif isinstance(project, str) and project.strip():
        p_name = project.strip()
        tech_stack = []
    else:
        p_name = "Full-Stack Project"
        tech_stack = []

    tech_hint = f" using {', '.join(tech_stack[:3])}" if tech_stack else ""
    
    llm_question = None
    try:
        from utils.llm_engine import generate_llm_project_probe
        llm_question = generate_llm_project_probe(c_name, p_name, tech_hint)
    except Exception:
        pass

    question = llm_question or (
        f"So {c_name}, on your resume you highlighted your project '{p_name}'{tech_hint}. "
        f"Could you walk me through the end-to-end system architecture, your specific technical contributions, "
        f"and the single toughest engineering roadblock or bug you encountered while building it?"
    )

    base_kws = ["architecture", "database", "api", "contribution", "roadblock", "challenge", "bug", "scale", "performance", "deployment"]
    tech_kws = [t.lower() for t in tech_stack if t.lower() not in base_kws]

    return {
        "category": "Project Authenticity",
        "question": question,
        "keywords": list(dict.fromkeys(base_kws + tech_kws)),
        "is_project_probe": True,
        "is_llm": bool(llm_question),
        "project_name": p_name,
    }


def build_resume_questions(analysis: dict, resume_text: str = "", first_name: str = "there") -> list:
    """
    Resume-Aware Interview Question Generator:
    Generates tailored questions specifically from the candidate's resume, including:
    - Found technical skills and tools
    - Additional claimed projects
    - Internships / Work Experience
    - Certifications & Coursework
    - Quantified metrics and impact
    """
    raw_first = first_name.strip() if first_name else "there"
    c_name = raw_first.split()[0].capitalize() if raw_first.lower() != "there" else "there"
    prefix = f"So {c_name}, " if c_name != "there" else ""

    questions = []
    skills = [s.strip() for s in analysis.get("skills", [])]
    sections = [s.lower() for s in analysis.get("sections", [])]
    projects = analysis.get("projects", [])
    percentages = analysis.get("percentages", [])

    # Comprehensive skill mapping for deep resume-aware technical probing
    _SKILL_QUESTIONS = {
        "Python": ("Python", f"{prefix}your resume highlights Python. How have you utilized Python in your projects, and how do you handle memory management and package dependencies?", ["python","generator","gil","virtualenv","library","memory"]),
        "Java": ("Java", f"{prefix}you listed Java on your resume. How do you implement object-oriented principles, and how does JVM garbage collection work under high load?", ["java","jvm","oop","garbage collection","multithreading","memory"]),
        "C++": ("C++", f"{prefix}your resume features C++. How do you manage pointers and dynamic memory allocation, and what are smart pointers?", ["c++","pointer","smart pointer","memory","heap","stack"]),
        "Javascript": ("JavaScript", f"{prefix}you listed JavaScript in your resume. How does the JavaScript event loop handle asynchronous tasks and microtasks?", ["javascript","event loop","async","await","promise","callback"]),
        "React": ("React", f"{prefix}your resume mentions React. How do you manage application state, and how does the Virtual DOM minimize expensive browser reflows?", ["react","virtual dom","state","props","hook","component"]),
        "Angular": ("Angular", f"{prefix}you included Angular on your resume. How does two-way data binding and dependency injection work in Angular?", ["angular","typescript","dependency injection","binding","service"]),
        "Spring Boot": ("Spring Boot", f"{prefix}you mentioned Spring Boot in your resume. How do dependency injection and auto-configuration accelerate your microservice development?", ["spring boot","annotation","dependency injection","controller","bean"]),
        "Node.Js": ("Node.js", f"{prefix}your resume lists Node.js. How does Node's single-threaded event loop handle non-blocking asynchronous I/O operations?", ["node.js","event loop","async","stream","express","non-blocking"]),
        "Mysql": ("MySQL", f"{prefix}you noted MySQL in your resume. How do you design normalized database schemas, and what indexing strategies do you use for high-traffic queries?", ["mysql","normalization","index","query","join","schema"]),
        "Postgresql": ("PostgreSQL", f"{prefix}your resume highlights PostgreSQL. What are the key advantages of PostgreSQL indexing and ACID transaction isolation?", ["postgresql","acid","index","isolation","transaction","json"]),
        "Mongodb": ("MongoDB", f"{prefix}your resume mentions MongoDB. When do you choose a document-based NoSQL store over a relational database, and how do you handle relations?", ["mongodb","nosql","document","schema","aggregation","sharding"]),
        "Aws": ("AWS Cloud", f"{prefix}you listed AWS on your resume. How do you architect cloud solutions for high availability, security, and cost efficiency using services like S3 and EC2?", ["aws","s3","ec2","lambda","cloud","iam"]),
        "Azure": ("Azure Cloud", f"{prefix}your resume mentions Azure. How do you configure cloud deployment pipelines and manage serverless compute in Azure?", ["azure","cloud","devops","pipeline","functions","storage"]),
        "Gcp": ("Google Cloud", f"{prefix}you listed GCP in your resume. How do you utilize GCP services for scalable containerized deployment and data storage?", ["gcp","cloud","bigquery","kubernetes","storage","compute"]),
        "Docker": ("Docker", f"{prefix}your resume lists Docker. How does containerization streamline your deployment pipeline compared to traditional virtual machines?", ["docker","container","image","dockerfile","layer","vm"]),
        "Kubernetes": ("Kubernetes", f"{prefix}your resume mentions Kubernetes. How does Kubernetes manage pod auto-scaling, service discovery, and rolling deployments?", ["kubernetes","pod","deployment","service","scaling","cluster"]),
        "Machine Learning": ("Machine Learning", f"{prefix}your resume features Machine Learning. Walk me through your workflow for data preprocessing, feature engineering, and avoiding model overfitting.", ["machine learning","feature","overfitting","validation","dataset","accuracy"]),
        "Deep Learning": ("Deep Learning", f"{prefix}you mentioned Deep Learning on your resume. What neural network architectures have you trained, and how do you optimize loss functions via backpropagation?", ["deep learning","neural network","backpropagation","weights","gradient","loss"]),
        "Nlp": ("NLP", f"{prefix}your resume features NLP. What approaches have you used for text tokenization and embeddings, and how do you evaluate model accuracy?", ["nlp","tokenization","embedding","transformer","tfidf","text"]),
        "Tensorflow": ("TensorFlow", f"{prefix}you listed TensorFlow in your resume. How do you structure training pipelines and handle GPU tensor computation?", ["tensorflow","tensor","epoch","batch","model","training"]),
        "Pytorch": ("PyTorch", f"{prefix}your resume highlights PyTorch. What makes PyTorch's dynamic computational graph beneficial during model experimentation?", ["pytorch","tensor","autograd","graph","module","optimizer"]),
        "Word2Vec": ("Word2Vec", f"{prefix}you mentioned Word2Vec in your resume. Explain the difference between CBOW and Skip-gram architectures for learning word vectors.", ["word2vec","cbow","skip-gram","context","vector","embedding"]),
        "OpenCV": ("Computer Vision", f"{prefix}your resume includes OpenCV. How do you process video frames or image matrices for feature detection and edge filtering?", ["opencv","image","filter","contour","detection","frame"]),
        "Dsa": ("DSA", f"{prefix}your resume emphasizes Data Structures and Algorithms. How do you evaluate time and space complexity when choosing between data structures?", ["dsa","time complexity","space complexity","big o","array","tree"]),
        "Dbms": ("DBMS", f"{prefix}your resume highlights DBMS concepts. What are ACID properties and why are they critical for concurrent transaction integrity?", ["dbms","acid","atomicity","consistency","isolation","durability"]),
        "Operating Systems": ("Operating Systems", f"{prefix}you listed Operating Systems in your resume. How does the OS handle process scheduling, virtual memory, and context switching?", ["operating system","process","thread","memory","scheduling","paging"]),
        "Networking": ("Networking", f"{prefix}your resume includes Computer Networks. Explain how TCP guarantees reliable transmission compared to UDP.", ["tcp","udp","handshake","packet","network","protocol"]),
    }

    # Add questions for matched skills
    used_categories = set()
    for s in skills:
        title_s = s.title()
        matched_key = None
        for k in _SKILL_QUESTIONS:
            if k.lower() == s.lower():
                matched_key = k
                break
        if matched_key and matched_key not in used_categories:
            cat, question, kws = _SKILL_QUESTIONS[matched_key]
            questions.append({"category": f"Resume - {cat}", "question": question, "keywords": kws, "is_resume": True})
            used_categories.add(matched_key)

    # Secondary project question if candidate has multiple projects
    if len(projects) >= 2:
        p2 = projects[1]
        p2_name = p2.get("name", "Secondary Project")
        p2_tech = p2.get("tech_stack", [])
        p2_kws = ["database", "schema", "api", "testing", "edge case", "validation"] + [t.lower() for t in p2_tech]
        questions.append({
            "category": "Resume - Projects",
            "question": f"{prefix}another project on your resume is '{p2_name}'. How did you approach database schema design, API structure, and user validation for this project?",
            "keywords": list(dict.fromkeys(p2_kws)),
            "is_resume": True
        })

    # Internship / Experience probe
    if any(h in sections for h in ["internships", "experience"]):
        questions.append({
            "category": "Resume - Experience",
            "question": f"{prefix}your resume highlights practical internship and work experience. What was the most impactful feature or bug fix you contributed to, and how did you collaborate with your team?",
            "keywords": ["experience","internship","contribution","team","feature","impact","collaboration"],
            "is_resume": True
        })

    # Certifications probe
    if "certifications" in sections:
        questions.append({
            "category": "Resume - Growth",
            "question": f"{prefix}you listed technical certifications on your resume. How have the core concepts from your certifications translated directly into real project implementations?",
            "keywords": ["certification","practical","learning","applied","architecture","project"],
            "is_resume": True
        })

    # Quantified metric probe
    if percentages:
        questions.append({
            "category": "Resume - Impact",
            "question": f"{prefix}your resume features quantified outcomes and percentage improvements. Could you walk me through the baseline metrics versus the final results and how you measured them?",
            "keywords": ["metric","improvement","measure","baseline","result","performance","benchmark"],
            "is_resume": True
        })

    return questions


def evaluate_answer(q, answer):
    text = answer.lower()
    keywords = q.get("keywords", [])
    hits = [k for k in keywords if k.lower() in text]
    concept_score = round(len(hits) / max(1, len(keywords)) * 100)
    relevance = min(100, 45 + len(hits) * 11) if answer.strip() else 0
    words = re.findall(r"\b[\w+#.-]+\b", answer)
    sentences = [x for x in re.split(r"[.!?]+", answer) if x.strip()]
    fillers = sum(len(re.findall(rf"\b{re.escape(x)}\b", text)) for x in ["um","uh","like","basically","actually","you know"])
    score = round(concept_score * .55 + relevance * .35 + max(0, 100 - fillers * 8) * .10)

    strengths, weaknesses = [], []
    if concept_score >= 60: strengths.append("Covered several expected concepts.")
    if len(words) >= 25: strengths.append("Provided a reasonably developed answer.")
    if fillers <= 2: strengths.append("Used relatively few filler words.")
    if concept_score < 60: weaknesses.append("Several expected concepts were missing.")
    if len(words) < 20: weaknesses.append("Answer could be more structured and detailed.")
    if fillers > 2: weaknesses.append("Reduce filler words for a more concise answer.")

    feedback = (
        f"Detected {len(hits)}/{len(keywords)} expected concepts. "
        f"Consider explicitly covering: {', '.join([k for k in keywords if k not in hits][:3]) or 'the core concepts more clearly'}."
    )
    return {
        "question": q["question"], "score": max(0, min(100, score)),
        "concept_score": concept_score, "relevance": relevance,
        "word_count": len(words), "sentence_count": len(sentences),
        "fillers": fillers, "strengths": strengths, "weaknesses": weaknesses,
        "feedback": feedback, "answer": answer
    }

def get_company_label(company):
    return f"{company} • Company-style Practice"
