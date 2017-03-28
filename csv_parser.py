from __future__ import print_function
import csv

test_file = 'neon9.txt'


def parse_it(file_):
    parsed_file = csv.reader(open(file_), dialect="excel-tab")
    return parsed_file


def servers_sorted(file_):
    servers = []
    for i in parse_it(file_):
        if len(i) == 5 and i[4] != "Server":
            servers.append(i[4])
        else:
            pass
    return sorted(set(servers))


def get_job_name(file_):
    job_name = ''
    for i in parse_it(file_):
        if len(i) == 1 and i[0][:4] == "Job:":
            job_name = i[0].split()[1]
    return job_name


def return_frames(file_, server):
    for line_ in parse_it(file_):
        try:
            if line_[4] == server:
                if line_[2] == "00000":
                    frame = line_[2][:1]
                else:
                    frame = line_[2].lstrip("0")
                yield frame
            else:
                pass
        except IndexError:
            pass


def print_all_jobs(file_):
    for server in servers_sorted(file_):
        print(server)
        for n in return_frames(file_, server):
            print(n, end=', ')
        print('\n')


#def make_dict(file_):
#    d = {}
#    for i in servers_sorted(file_):
#        d[i] = list(return_frames(file_, i))
#    return d.items()


if __name__ == '__main__':
    print_all_jobs(test_file)
