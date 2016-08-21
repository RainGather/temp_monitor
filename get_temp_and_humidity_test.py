from os.path import exists


def get_temp_and_humidity(pin, outtime=10):
    if not exists('temp_test.txt'):
        with open('temp_test.txt', 'w') as fw:
            print('init')
            fw.write('0,0')
    with open('temp_test.txt', 'r') as fr:
        l = fr.read().split(',')
        return float(l[0]), float(l[1])
