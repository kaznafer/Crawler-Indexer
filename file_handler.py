import os


# create a folder that's starts from a homepage that handles the websites
def create_proj_directory(directory):
    if not os.path.exists(directory):
        print('Creating directory ' + directory)
        os.makedirs(directory)


# Create queue and crawled files (if not created).Use the write_to_file method.
def create_files(project, first_url):
    pages_in_queue = os.path.join(project, 'queue.txt')  # add websites in queue
    crawled_pages = os.path.join(project, "crawled.txt")  # update crawled webpages
    if not os.path.isfile(pages_in_queue):
        write_to_file(pages_in_queue, first_url)
    if not os.path.isfile(crawled_pages):
        write_to_file(crawled_pages, '')


# Create a new file and data from scratch
def write_to_file(path, data):
    with open(path, 'w') as f:
        f.write(data)


# Delete the contents of a file
def delete_file_inside(path):
    open(path, 'w').close()


# Read a file and convert each line to set items
def file_to_set(file_name):
    results = set()
    with open(file_name, 'rt') as f:
        for line in f:
            results.add(line.replace('\n', ''))  # replace new line with 'nothing'
    return results


# Iterate through a set, each item will be a line in a file
def set_to_file(links, file_name):
    with open(file_name, "w") as f:
        for l in sorted(links):
            f.write(l + "\n")
