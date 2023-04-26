from datetime import datetime

def main():
    print(datetime.now())
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("date and time =", dt_string)


if __name__ == "__main__":
    main()
