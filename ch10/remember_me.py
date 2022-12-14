import json

def get_stored_username():
    """저장된 사용자 이름이 있다면 불러옵니다."""

    filename = 'username.json'

    try:
        with open(filename) as f:
            username = json.load(f)

    except FileNotFoundError:
        return None
    
    else:
        return username

def get_new_username():
    """새 사용자 이름을 묻습니다."""
    
    username = input('What is your name? ')
    
    filename = 'username.json'
    with open(filename, 'w') as f:
        json.dump(username, f)
    
    return username
    

def greet_user():
    """사용자를 이름으로 환영합니다."""

    username = get_stored_username()

    if username:
        print(f"Welcome back, {username}!")
    else:
        username = get_new_username()
        print(f"We'll remember you when you come back, {username}!")

greet_user()