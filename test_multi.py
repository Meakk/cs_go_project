import multiprocessing
import time
from awpy.parser import DemoParser
from multiprocessing import get_context
import json
import os
import re
def multi(filename):
        print("debut du parse multi")
        print(filename)
        import re
        id = re.sub("[^0-9]", "", filename)
        demo_parser = DemoParser(demofile='demo_csgo/dem_file/' + filename,
                                demo_id=str(id), parse_rate=128)
        data  = demo_parser.parse()
        print("child :",data.keys())
        with open('demo_csgo/'+filename+'.json', 'w') as json_file:
            json.dump(data, json_file)
            
   
if __name__ == "__main__":
        print("debut du parse")
        # processors = multiprocessing.cpu_count()
        #queue = multiprocessing.Queue()
        # for root, dirs, files in os.walk("demo_csgo/dem_file/"):
        #     queue.put(files)
        for root, dirs, files in os.walk("demo_csgo/dem_file/"):
                for filename in files :
                        processes = multiprocessing.Process(target=multi, args=(files,))
                        processes.start()