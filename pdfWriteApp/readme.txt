1) requirements.txt file has been added. There are new python files for exception handling.

2) Now to run the script, please use "python run.py" in the command prompt.
You should get a successful Application startup if every module has been installed in python.

3) A log file will be created app.log when the application is run or during the errors or exception.

4) For every new request a new pdf file with random name is created now.

Tested locally, it's working fine. Tested it only with the links of pdf. The other languages can also be tested, it should work fine for other languages as well.

Also Other PDFs can also be tested and it should work fine with the same code.


5) The syntax now for the input testing from POSTMAN is :

{
  "blank_pdf": "https://test-devops.s3.ap-south-1.amazonaws.com/example.pdf",
  "json_link": "https://test-devops.s3.ap-south-1.amazonaws.com/example_en.json",
  "language":"English"
}

6) Here I am just reading the language, but not using it anywhere in the code. Based on the language of the json file, the code automatically writes that language to the blank pdf, the requirement of adding a language is not used anywhere in the code.

Pending items:
1) Optimization of the code to return the pdf faster.
2)  If there are any additional changes to the requirements then we can discuss it.
3) Further testing of the code is required to find any additional issues.
