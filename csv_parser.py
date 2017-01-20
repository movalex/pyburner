import csv
from tkinter import filedialog, Tk

root = Tk()
root.withdraw()

file_path = 'neon9.csv'

def parse_it(file):
    parsed_file = csv.reader(open(file), dialect="excel-tab")
    return parsed_file

def servers_sorted(foo):
    servers = []
    for i in parse_it(foo):
        if len(i) == 5 and i[4] != "Server":
            servers.append(i[4])
        else:
            pass
    return sorted(set(servers))
#print(servers_sorted(file_path))

def get_job_name(foo):
    job_name = ''
    for i in parse_it(foo):
        if len(i) == 1 and i[0][:4] == "Job:":
            job_name = i[0].split()[1]
    return job_name
#print('Job name: {}'.format(get_job_name(file)))


def return_frames(file_, server):
    for _line in parse_it(file_):
        try:
            if _line[4] == server:
                if _line[2] == "00000":
                    frame = _line[2][:1]
                else:
                    frame = _line[2].lstrip("0")
                yield frame
            else:
                pass
        except IndexError:
            pass
#print(list(return_frames(file_path, 'aston3d')))


def all_jobs(file):
    for server in servers_sorted(file):
        print(server)
        for n in return_frames(file, server):
            print(n, end=', ')
        print('\n')


if __name__ == '__main__':
    all_jobs(file_path)