# career_forge/engine/feature_extractor.py

from typing import List, Dict
from pydantic import BaseModel, Field
from spacy.matcher import PhraseMatcher

# Import the tools we created in the last step
from .parser import ParsedResume, NLP

# --- A small setup note ---
# Ensure the spaCy model is available, as this file depends on it.
if NLP is None:
    raise ImportError("spaCy model 'en_core_web_sm' not loaded. Please run the download command.")

# -----------------------------------------------------------------------------
# 1. Define Known Skills & Output Schema
# -----------------------------------------------------------------------------

# This is the comprehensive, high-end skill dictionary.
SKILL_PATTERNS = {
    "PROGRAMMING": [
        "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "C", "Go", "Rust", "Ruby",
        "PHP", "Swift", "Kotlin", "Scala", "Perl", "R", "MATLAB", "Lua", "Objective-C", "Bash",
        "Shell Scripting", "PowerShell"
    ],
    "WEB_DEVELOPMENT": [
        "HTML", "CSS", "Sass", "LESS", "Node.js", "Express.js", "React", "Angular", "Vue.js",
        "jQuery", "ASP.NET", "Django", "Flask", "Ruby on Rails", "Spring Boot", "Next.js",
        "Nuxt.js", "Svelte", "Gatsby", "Bootstrap", "Tailwind CSS", "Redux", "MobX", "Webpack",
        "Vite", "WebSockets", "SEO", "Web Accessibility", "WCAG", "Progressive Web Apps", "PWA"
    ],
    "DATABASE": [
        "SQL", "MySQL", "PostgreSQL", "SQLite", "Microsoft SQL Server", "Oracle", "MongoDB",
        "Redis", "Cassandra", "DynamoDB", "Firebase", "Elasticsearch", "SQLAlchemy", "Prisma",
        "InfluxDB", "Neo4j", "Graph Databases", "DBeaver"
    ],
    "AI_MACHINE_LEARNING": [
        "Machine Learning", "Deep Learning", "Natural Language Processing", "NLP", "Computer Vision",
        "Reinforcement Learning", "TensorFlow", "PyTorch", "Keras", "Scikit-learn", "Pandas",
        "NumPy", "SciPy", "Matplotlib", "Seaborn", "spaCy", "NLTK", "OpenCV", "XGBoost",
        "LightGBM", "Hugging Face", "Transformers", "Generative AI", "LLM", "Large Language Models"
    ],
    "DATA_SCIENCE": [
        "Data Analysis", "Data Mining", "ETL", "Data Warehousing", "Business Intelligence",
        "Apache Spark", "Hadoop", "Kafka", "Tableau", "Power BI", "Looker", "Airflow", "dbt",
        "Data Bricks"
    ],
    "DEVOPS_CLOUD": [
        "CI/CD", "Jenkins", "GitLab CI", "GitHub Actions", "Docker", "Kubernetes", "Terraform",
        "Ansible", "Puppet", "Chef", "AWS", "Amazon Web Services", "Azure", "Google Cloud Platform",
        "GCP", "Heroku", "DigitalOcean", "Vercel", "Netlify", "Linux", "EC2", "S3", "Lambda",
        "RDS", "VPC", "CloudFormation", "Azure VMs", "Blob Storage", "Azure Functions", "Prometheus",
        "Grafana", "Datadog", "Splunk"
    ],
    "MOBILE_DEVELOPMENT": [
        "Swift", "SwiftUI", "Objective-C", "Kotlin", "Java", "React Native", "Flutter", "Xamarin",
        "Android SDK", "iOS SDK"
    ],
    "ARCHITECTURE_DESIGN": [
        "Microservices", "REST API", "GraphQL", "gRPC", "Agile", "Scrum", "Kanban", "Waterfall",
        "Design Patterns", "SOLID", "TDD", "BDD", "Domain-Driven Design", "DDD", "SOA"
    ],
    "DESIGN_UI_UX": [
        "Figma", "Sketch", "Adobe XD", "InVision", "Zeplin", "User Interface Design", "UI",
        "User Experience Design", "UX", "Wireframing", "Prototyping", "User Research"
    ],
    "TESTING_QA": [
        "Selenium", "JUnit", "TestNG", "PyTest", "Cypress", "Jest", "Mocha", "Chai", "Postman",
        "SoapUI", "JMeter", "Quality Assurance", "QA", "Automated Testing", "Manual Testing",
        "Performance Testing", "End-to-End Testing", "Unit Testing", "Integration Testing"
    ],
    "CYBER_SECURITY": [
        "Cybersecurity", "Network Security", "Penetration Testing", "Ethical Hacking", "SIEM",
        "Vulnerability Assessment", "Encryption", "Cryptography", "OWASP", "Wireshark",
        "Metasploit", "Burp Suite", "Nmap", "Firewalls"
    ],
    "BUSINESS_TOOLS": [
        "Microsoft Office Suite", "MS Office", "Microsoft Excel", "Microsoft Word", "PowerPoint",
        "Google Workspace", "Salesforce", "SAP", "SharePoint"
    ],
    "PROJECT_MANAGEMENT_TOOLS": [
        "Jira", "Confluence", "Trello", "Asana", "Slack", "Monday.com", "ClickUp", "Microsoft Project"
    ],
    "SOFT_SKILL": [
        "Leadership", "Teamwork", "Collaboration", "Communication", "Problem Solving",
        "Creativity", "Adaptability", "Time Management", "Critical Thinking", "Detail-oriented",
        "Emotional Intelligence", "Mentorship", "Public Speaking", "Negotiation",
        "Conflict Resolution", "Stakeholder Management", "Client Relations", "Active Listening",
        "Interpersonal Skills", "Strategic Thinking"
    ]
}


class ExtractedFeatures(BaseModel):
    """
    This is the structured output from our feature extractor. It categorizes
    the extracted information, making it easy for other parts of the system
    (like gamification) to use.
    """
    skills: Dict[str, List[str]] = Field(default_factory=dict, description="Skills categorized by type.")
    entities: Dict[str, List[str]] = Field(default_factory=dict,
                                           description="Named entities like organizations or locations.")


# -----------------------------------------------------------------------------
# 2. The Core AI Analysis Logic
# -----------------------------------------------------------------------------

def extract_features(resume: ParsedResume) -> ExtractedFeatures:
    """
    Analyzes a parsed resume to extract structured features like skills
    and named entities using spaCy's powerful toolset.
    """
    # 1. Initialize the PhraseMatcher for Skill Extraction
    matcher = PhraseMatcher(NLP.vocab, attr="LOWER")
    for category, skills in SKILL_PATTERNS.items():
        patterns = [NLP.make_doc(skill) for skill in skills]
        matcher.add(category, patterns)

    # 2. Process the Document to Find Matches
    matches = matcher(resume.doc)

    # 3. Organize Found Skills
    found_skills = {}
    for match_id, start, end in matches:
        category_id = NLP.vocab.strings[match_id]
        skill_text = resume.doc[start:end].text

        if category_id not in found_skills:
            found_skills[category_id] = []

        # Add skill only if it's not already listed to avoid duplicates
        if skill_text not in found_skills[category_id]:
            found_skills[category_id].append(skill_text)

    # 4. Extract Named Entities (e.g., Universities, Companies)
    # This uses spaCy's built-in NER model. It automatically finds things
    # like organizations (ORG), locations (GPE), and dates (DATE).
    found_entities = {}
    # We're interested in specific entity types
    interesting_labels = ["ORG", "GPE", "DATE"]
    for ent in resume.doc.ents:
        if ent.label_ in interesting_labels:
            if ent.label_ not in found_entities:
                found_entities[ent.label_] = []

            if ent.text not in found_entities[ent.label_]:
                found_entities[ent.label_].append(ent.text)

    return ExtractedFeatures(skills=found_skills, entities=found_entities)