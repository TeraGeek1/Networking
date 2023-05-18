# Threading allows use to speed up programs by executing multiple tasks at the same time.
# Each task will run on its own thread.
# Each thread can run simultaneously and share data with each other.

# Every thread when you start it must do SOMETHING, which we can define with a function.
# Our threads will then target these functions.
# When we start the threads, the target functions will be run.

import threading


def func1():
    for i in range(10):
        print("ONE ")


def func2():
    for i in range(10):
        print("TWO ")


def func3():
    for i in range(10):
        print("THREE ")


## If we call the functions The first function called must complete before the next can begin
# print("Normal call\n")

# func1()
# func2()
# func3()


## We can execute these functions concurrently using treads!   We MUST have a target for a thread
print("\n\nTreading call\n")

# t1 = threading.Thread(target=func1)
# t2 = threading.Thread(target=func2)
# t3 = threading.Thread(target=func3)

# t1.start()
# t2.start()
# t3.start()

## Threads can only be started once. So if you want to reuse, you must redefine.
t1 = threading.Thread(target=func1)
t1.start()

## If you want to 'pause' the main program until a thread is done you can!
t1 = threading.Thread(target=func1)
t1.start()
t1.join()  # This 'pauses' the main program until the thread is complete
print("Threading rules!")
