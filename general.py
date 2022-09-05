import os


# Each directory is a new project which is basically a new website to crawl.


def create_new_directory(directory):
    if not os.path.exists(directory):
        print("Creating Project " + directory)
        os.makedirs(directory)


# creating queue and crawled files
def create_data_files(project_name, base_url):
    queue = project_name + "/queue.txt"
    crawled = project_name + "/crawled.txt"
    if not os.path.exists(queue):
        write_file(queue, base_url)
    if not os.path.exists(crawled):
        write_file(crawled, '')


# writing in file
def write_file(path, data):
    f = open(path, 'w')
    f.write(data)
    f.close()


def append_data(path, data):
    with open(path, 'a') as f:
        f.write('\n' + data)
        f.close()


def delete_file_data(path):
    with open(path, 'w'):
        pass


# iterate through file and save each line in a set
def file_to_set(file_name):
    results = set()
    with open(file_name, 'rt') as f:
        for line in f:
            results.add(line.replace("\n", ""))
        f.close()
    return results

# iterate through set and save each item as line in file.
def set_to_file(links, file_name):
    delete_file_data(file_name)
    for link in sorted(links):
        append_data(file_name, link)
