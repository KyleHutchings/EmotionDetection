EmotionDetection v1

Bio:
 Sentiment analysis system operating off a multinomial Naive Bayes classififer.
 There are 13 possible labels that text can be labelled as, the emotions are:
  -empty
  -sadness
  -enthusiasm
  -neutral
  -worry
  -surprise
  -love
  -fun
  -hate
  -happiness
  -boredom
  -relief
  -anger

Requirements:
 This software was developed using python2 and as such may have issues when being run
 with python3.
 
 If using Windows make sure the installation of Python is 32-bit.

 There are a number of required packages that must be installed to run this software.
 These packages are found in the "requirements.txt" file and can be installed from
 "PyPi" with the "pip" command on the terminal.

 Also required is Tkinter for Python, which should come pre-installed with python.

Setup:
 -install required packages in "requirements.txt", if pip is installed use command "pip install -r 'requirements.txt'"
 -download data required for the NLTK package, using "setup_nltk.py"
 -run main.py to begin
