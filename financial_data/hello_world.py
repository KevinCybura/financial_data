from prefect import task


@task()
def say_hello():
    print("Hello, world!")
