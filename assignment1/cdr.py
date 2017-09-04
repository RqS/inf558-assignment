import os
import sys
import time
import json

directory = sys.argv[1]
cdr_output = sys.argv[2]
# directory = "/Users/runqishao/Desktop/inf558/assignment/assignment1/samples"
# cdr_output = "/Users/runqishao/Desktop/inf558/assignment/assignment1/cdr.jl"

output_f = open(cdr_output, "w")

idx = 0
for filename in os.listdir(directory):
    if not filename.startswith('.'):
        this_line = dict()
        this_line["doc_id"] = idx
        idx = idx + 1
        url = filename.replace('%2F', '/').replace('%3A', ':')
        this_line["url"] = url
        file_path = directory + "/" + filename
        crawl_time = time.ctime(os.path.getctime(file_path))
        this_line["timestamp_crawl"] = crawl_time
        with open(file_path, 'r') as myfile:
            raw_content = myfile.read().replace('\n', '')
        this_line["raw_content"] = raw_content
        json.dump(this_line, output_f)
        output_f.write("\n")

output_f.close()
