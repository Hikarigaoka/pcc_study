from survey import AnonymousSurvey

#설문을 정의하고 설문조사를 만듭니다
question = "What language did you first learn to speak?"
my_survey = AnonymousSurvey(question)

#설문을 표시하고 응답을 저장합니다
my_survey.show_question()
print("Enter 'q' at any time to quit.\n")
while True:
    response = input("Language: ")
    
    if response == 'q':
        break

    my_survey.store_response(response)

#설문조사 결과를 표시합니다
print("\nThank you to everyone who participated in the survey!")
my_survey.show_results()