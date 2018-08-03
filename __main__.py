import sys, argparse

def argument():
    parser = argparse.ArgumentParser(description="Application Register")
    parser.add_argument('action', choices= ['register', 'deregister'], action = "store", default = 'register' ,help="Action to register | deregister your Application ")
    return parser.parse_args()

def main():
    pass

if __name__ == '__main__':
    main()