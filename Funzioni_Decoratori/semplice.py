def my_decorator(func):
    def my_wrapper(*args, **kwargs):
        print("Prima")
        func(*args, **kwargs)
        print("Dopo")

    return my_wrapper


@my_decorator
def echo(msg):
    print(msg)


# echo = my_decorator(echo)

if __name__ == "__main__":
    echo("Ciao")

