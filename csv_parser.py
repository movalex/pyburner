from __future__ import print_function
import csv

test_file = 'neon9.txt'


def parse_it(file_, delimiter):
    parsed_file = csv.reader(open(file_), delimiter=delimiter)
    return parsed_file


def servers_sorted(file_):
    servers = []
    for i in parse_it(file_, delimiter='\t'):
        if len(i) == 5 and i[4] != "Server":
            servers.append(i[4])
        else:
            pass
    return sorted(set(servers))


def get_job_name(file_):
    job_field = 'Job'
    for i in parse_it(file_, delimiter=':'):
        try:
            if i[0]==job_field:
                return i[1].strip()
        except IndexError:
            pass


def return_frames(file_, server):
    for line_ in parse_it(file_, delimiter='\t'):
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


if __name__ == '__main__':
    print('Job name: {}\n'.format(get_job_name(test_file)))
    print_all_jobs(test_file)
