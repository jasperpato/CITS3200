import json 
import os 
import sys 

remake_flag = False

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import thread_obj
import parse_file

def main(in_file, out_file):
    threads = parse_file.parse_file(os.path.join(parentdir, in_file))
    posts = thread_obj.all_posts(threads)
    posts.sort(key=lambda p: p.date)
    json_obj = {'test_space': [{'Date': str(p.date), 'Subject': p.subject, 'Body': p.payload, 'Verified': str(p.verified), 'Tags': []} for p in posts[0:50]]}
    f = open(os.path.join(currentdir, out_file), 'w')
    json.dump(json_obj, f, indent=4)
    f.close()

if __name__ == '__main__' and remake_flag:
    main('help2002-2019.txt', 'test_Space_2019_2.json')



