# f24_ECE590_team06

## Name
Pendream--An Interactive Spelling Practice System with an OCR Model


## Description
Spelling proficiency is a foundational skill for young children. To enhance spelling practice, we propose developing a handwriting-based spelling fill-in-the-blank application. 
Leveraging deep learning algorithms for handwriting recognition, this software will provide a user-friendly platform for learners to practice spelling in a natural and interactive manner. 
The system will allow users to handwrite their answers directly and receive automated evaluations, offering personalized feedback for improvement.

## Installation
To set up and run the application, ensure you have the following dependencies installed in your Python environment. Below is a list of the required packages:

## Required Libraries
- **transformers**: For the TrOCRProcessor and VisionEncoderDecoderModel.
- **Pillow**: For image handling and processing.
- **PyQt5**: For the graphical user interface components.

## Usage/Quick Start
Run main.py!

Waiting for the windows open and choose the catagories, levels of the vocabulary and the number of the questions.Waiting for the question showing up and click 'Start Handwriting'.

Then you can write down the answer on the whiteboard. Click on 'Save' and then click on the evaluate button to evaluate your answer.
 
Once you see the right answer showing up, you can click on 'Next question' and do a new one by clicking on 'Start Handwriting' again.

Once you finished all the questions, you can click on 'Final Report' to see the final score and all the questions you've answered.

Once you finished the practice, you can click 'Exit' to exit the program.

## Addition explaination for testing coverage
- The reason why the __init__ function of main.py and the load_next_question function in interface.py do not have automated tests: This is because my Qt interface uses a dropdown menu, which can only be generated after the __init__ function has been executed. Testing this menu leads to an access violation error, as the pytest file encounters insufficient memory access permissions. The reason the latter function cannot be tested is that the question generation function generates questions purely at random, making it impossible to establish precise and specific test cases.
Nevertheless, I have conducted manual testing on these two functions, including as many comprehensive corner cases as possible and cover all branches and statements. I believe that these two functions and the class they belong to have been thoroughly refined.
- For the "No more questions available." branch in interface.py that cannot be tested, the reason is that this message only appears when the question list reaches its end. However, the number of questions in the list (i.e., the number of times the "next question" button can be pressed) is not determined by this class, making it untestable.
- The reason why question.py does not achieve full coverage is that it contains an abstract method which cannot be covered by tests.
