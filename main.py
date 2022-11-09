from wrangle import *
from visualise import *
from org import *

def main():

    make_dir()
    wrangle()
    print("wrangle successful")
    visualise()
    print("visualise successful")

if __name__ == "__main__":
    main()