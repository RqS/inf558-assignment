import os
import sys
import time
import json
import codecs
import urllib

directory = sys.argv[1]
cdr_output = sys.argv[2]
# directory = "/Users/runqishao/Desktop/inf558/assignment/assignment1/samples"
# cdr_output = "/Users/runqishao/Desktop/inf558/assignment/assignment1/cdr.jl"

output_f = codecs.open(cdr_output, "w")

idx = 0

size_lst = []

for filename in os.listdir(directory):
    if not filename.startswith('.'):
        this_line = dict()

        this_line["doc_id"] = idx
        idx = idx + 1

        url = urllib.unquote(filename)
        this_line["url"] = url

        file_path = directory + "/" + filename
        crawl_time = time.ctime(os.path.getctime(file_path))
        this_line["timestamp_crawl"] = crawl_time

        filesize = os.path.getsize(file_path)
        size_lst.append(filesize)

        with codecs.open(file_path, 'r', encoding='latin-1') as myfile:
            raw_content = myfile.read()
        this_line["raw_content"] = raw_content
        
        json.dump(this_line, output_f)
        output_f.write("\n")

output_f.close()
