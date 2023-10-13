# TDP003


```
cd existing_repo
git remote add origin https://gitlab.liu.se/phibr608/tdp003.git
git branch -M main
git push -uf origin main
```


Navigate to documents
$ git clone git@gitlab.liu.se:phibr608/tdp003.git eller https://gitlab.liu.se/phibr608/tdp003.git
$ cd tdp003
$ cd Presentationlager
$ python3 -m venv .venv
$ . .venv/bin/activate
$ pip install flask
$ python3 app.py


TDP003
Project Summary:
	create a portfolio page that is divided into two parts a presentation layer and a data layer
	The data layer should handel all the data in the system. The data should be storde on a text file in the JSON format
	The presentation layer should present this data in a well done manner. The presentation should be done in HTML
	The presentation layer and data layer will comunicate through a API that will be provided.
	The API sould work in according to its specifications witch are provided
	A give project(not the overall project but a give post) will handel: Project name, Project id-number, start date, end date, course code, 
	course name, course points, A short descreption, A thourgh descreption, a small and large picture, 
	group size and a link to the course page.
	Project id should be uniqe.
	Every project should contain a squense of techniques used
	A sherch function must exist
	Data is to be storde on a data.json file in UTF-8 
	Data to the json file can be inserted manualy or through other tools
	changes to data.json should be applied with out server restart 
	optinal expansion of system for a admin page for data editing 

Requirements:
	Code Complete 2nd Edition
	Flask & Jinja
	LaTeX

Hand-in Instructions:
	All hand-ins done from student-email.
	Email subject must contain course-code (TDP003) and assignment.
	All documents (except dairy) are to be written in LaTeX and attached as PDF.
	All LaTeX documents shall be written according to template found on course webpage.
	For code hand-ins a Gitlab link is to be provided.
	Supplementing work must be handed in after five work days.

Deadlines:
	DATE | ASSIGNMENT | COMMENT
	04/09 | Group Contract
	12/09 | Timeplan Hand-in
	15/09 | LoFi Prototype | Low Fidelity Prototype/ Proof of Concept
	21/09 | Project Plan Draft & Installation Manual Draft
	28/09 | Complete Project Plan & Installation Manual
	29/09 | Data-Layer Approved | Must be done during laboration (last 28th)
	09/10 | Project Published Online & System Documentation Draft | Preferrably earlier
	??/10 | Complete System Documentation | Complete when draft is returned
	19/10 | Individual Documentation
	??/?? | Personal Work Dairy | Two moments during project to be handed in

Sub-tasks:
	Dairy: After every code-edit/ work session, write a small entry into personal work dairy.
	Group Contract: A contract outlining how the group will work together. Only "Hur vi arbetar tillsammans" is required.
	Timeplan: A rough plan how work is distriuted across the deadlines. Requires overview from lab-assistent.
	LoFi-Prototype: A proof-of-concept on how the website will look and function.
		Can be drawn on paper or produced digitally using HTML or design applications.
		Requirements are available on course webpage.
		A document for parts of the prototype that are not visible should be written besides.
	Installation Manual: A document (readme) outlining how to install all requirements for the project.
		Requirements are available on course webpage.
		Strong requirements on good language and correctness.
	Project Plan: A detailed plan with all requirements and timeplans to complete the project.
		Time disposition and work delegation to be included.
		Strong requirements on good language and correctness.
		Requirements are available on course webpage.
		Written in LaTeX.
		Contains general information about project. E.g. authors, dates, summary.
	Data Layer and Unit Testing: Project requires an API that will be provided.
		In API repository there will be unit tests to ensure API implementation works.
	Publish Project: Publish the finished project. Instructions available on course webpage.
	System Documentation: A more detailed documentation on system functionality.
		Used by other developers to interact and modify project source code.
	Self-reflection Document: A final review over how the development proess has been.
		Written individually about own self progress and experience about the project.
		Should contain references to Code Complete 2nd Edition.
		Written in LaTeX. Relies on personal dairy.
	Oral Examination: A final test to verify that participants have done their work in the group.
		Done individually at the end. Project environment must work on SU-computers.
		Sudo is not available.

Timeplan Draft:
	04/ 09:
		Hand in group contract.

	04 - 05/ 09:
		Start and finish time plan.

	06- 08/ 09:
		Start LoFi Protype.

	11/ 09:
		Finish LoFi Prototype.
		
	12 - 15/ 09:
		Project plan.
		Installation Manual.

	18 - 29/ 09:
		Data-Layer.
		When Project Plan draft is returned: Complete it.

	29 - ??:
		Work on complementary parts and individual documentation.
