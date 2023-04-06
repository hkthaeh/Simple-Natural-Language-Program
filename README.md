# Simple-Natural-Language-Program


A simple natural language program using the NLTK library 


Put any .txt articles in the "corpus" folder and this program will tokenize 
all the words in each file

Input in terminal:

    python questions.py corpus 

then ask it a question relating to the .txt files in the folder "corpus"




TimeLine:
  
  Start to questions v1.py:
      
      took around 1 month
        -coding/testing
      
      
      Files created/tests/my thought process:
        -questions v1.py
        -test.py
        -test1.py
        -test2.py
        -test3.py
        -test4.py
        -test5.py
  
  questions v1.py to questions.py ( version 2 )
      
      took around 3 days
        - refactoring/cleaning up the code/testing
      
      Files created/tests/my thought process:
        -questions.py ( version 2 )
        -test6.py
        -test7.py
        -test8.py
        -output.txt
        -output2.txt



Software Requirements Specification (SRS)

	Functionality
	
		-takes in any article/writing of a txt filetype inside the corpus folder and using the NLTK natural language library, we can ask the program questions relating to any of the inputed txt files and receive an relative accurate answer relating to the question asked 

	Intended Audience
	
		-This program is intended for all general audience that wants to find a quick answer to a question relating to an article/articles. 
	Benchmarks
	
	Constraints 
	
		-Only txt filetypes can be input into the corpus folder 
		-The more files in the corpus folder, the longer the program will take to run
		-Only questions relating the the txt files inside the corpus folder will receive a relatively accurate answer 
		-Only questions inputed in the English language, ASCII alphabets, will be recognize by the program 
		-This program is dependent on the NLTK natural language Python library
	
	
	Requirements
	
		Functional
			-Python version 3.7 or higher
			-Installation of the NLTK Python Library 
				https://www.nltk.org/install.html
		External Interface Requirements 
			-A Mac or PC computer using any IDEs such as VS Code
		
		System Features 
			Mac
				-Running any Mac operating system version
			Windows
				-Running any Windows operating system version

	Non-Functional Requirements
	
		Performance
			-The more txt files inside the corpus folder, the slower it will run
		Safety/Security 
			-All files put inside the corpus folder will stay there and will need to be manually deleted if required 
		Quality
			-Inputed articles that are very similar to one another will result in a answer that might not satisfy the user


User Requirements Specification ( URS ) 

	Who is the User?
		-Anyone who wants to quickly find a answer to a particular question relating to a specific article. 
	What is the function that needs to be performed? 
		-To quickly find a answer to a question relating to one article
	Why does the user want this functionality?
		-To save time on trying to find the answer of a specific question in a very long article/writing 


System Requirement Specification ( SysRS ) 

	Policy 
		-Anyone can use this program 
	Regulation
		-None
	Personnel
		-Anyone can use this program 
	Performance 
		-The more txt files inside the corpus folder, the slower the program will run
	Security 
		-All files will be saved inside the corpus folder and will need to be manually removed if required 
	Hardware Expectation 
		- Any computer that can run VS Code with Python version 3.7 or higher
