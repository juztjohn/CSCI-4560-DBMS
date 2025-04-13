# CSCI-4560-DBMS
[Github Repository](https://github.com/juztjohn/CSCI-4560-DBMS)

We will be creating a fully functional healthcare portal that allows patients and staff to access relevant information. Security and availability will be our main focuses of this project, as a real healthcare portal must be HIPAA compliant and highly available. 

We will be implementing security best practices such as role-based access and password hashing using the SHA256 algorithm and ensuring that the website and database is not prone to crashes or errors that may disrupt the user experience.
# Team
**Elaina Vogel** 
- Frontend Development

**Jaron McCutcheon**
- Backend Development

**John Byrd**
- Merging/Testing
- Additional Frontend/Backend Development
# Technology Used
<div>
  <img src="https://github.com/devicons/devicon/blob/master/icons/django/django-plain-wordmark.svg" title="Django" alt="Django" width="40" height="40"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/mysql/mysql-original.svg" title="MySQL" alt="MySQL" width="40" height="40"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/python/python-original-wordmark.svg" title="Python" alt="Python" width="40" height="40"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/html5/html5-original.svg" title="html" alt="C#" width="40" height="40"/>&nbsp;
</div>

# Setup the UI

1. Install the files in your desired location
2. Create a virtual environment and activate it as your python source
3. Run the following in the terminal:
```
pip install -r requirements.txt
```
4. Navigate to the medical_records_portal folder in the terminal
5. Run the following command in the terminal:
```
python manage.py runserver
```
6. Open a browser and enter "http:127.0.0.1:8000/home" as the url to view the login page
7. Enter "http:127.0.0.1:8000/patient" as the url to view the patient view page
