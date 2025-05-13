import os

def switch_order_of_extensions(path):

    paths = [os.path.join(path, f) for f in os.listdir(path)]

    for path in paths:
        if path[-1].isdigit():
            new_path = path.split('.')[0] + '.' + path.split('.')[2] + '.' + path.split('.')[1]
            print(new_path)
            print(path)

            #os.rename(path, new_path)


def main():

    path = ''
    switch_order_of_extensions(path)

if __name__ == '__main__':

    main()
