import datetime

def greet(name):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"👋 Hello, {name}! ⏰ Current time: {current_time}"

if __name__ == "__main__":
    user = "World"
    print(greet(user))
