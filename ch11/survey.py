class AnonymousSurvey:
    """설문 조사에서 익명 응답을 수집합니다"""

    def __init__(self, question):
        """설문을 저장하고 응답을 저장할 준비를 합니다"""
        self.question = question
        self.responses = []

    def show_question(self):
        """설문을 표시합니다."""
        print(self.question)

    def store_response(self, new_response):
        """응답 하나를 저장합니다."""
        self.responses.append(new_response)

    def show_results(self):
        """받은 응답을 모두 표시합니다"""
        print("Survey results:")
        for response in self.responses:
            print(f"- {response}")