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

    path = 'J:\projects\jamaica_training_day\jamaica_training_day_maya\jamaica_training_day\images'
    switch_order_of_extensions(path)

if __name__ == '__main__':

    main()