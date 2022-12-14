
def count_words(filename):
    """파일에 들어 있는 단어를 셉니다"""
    try:
        with open(filename, encoding='utf-8') as f:
            contents = f.read()
    except FileNotFoundError:
        pass    
    else:
        words = contents.split()
        num_words = len(words)
        print(f"The file {filename} has about {num_words} words.")


filenames = ['text_files/alice.txt', 'text_files/moby_dick.txt', 'text_files/pi_million_digits.txt']
for filename in filenames:
    count_words(filename)