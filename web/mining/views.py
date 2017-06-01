# coding: utf-8
import os
import json
import subprocess
import signal

import torndb
from web.common.init import *
from web.settings import *

import tasks

db = torndb.Connection(db_server, db_database, db_username, db_password)

class Defect_Mining_Crash_File_Handler(WiseHandler):
    def post(self):
        id = self.get_argument("id", None, strip=True)
        sql = 'select binary_name FROM binarys WHERE id = %s' % id
        binary_name = db.get(sql)['binary_name']

        crashes = []
        output_path = os.path.join(os.path.dirname(__file__), '../../output/%s/sync' % binary_name)
        for fuzzer in os.listdir(output_path):
            crashes_dir = os.path.join(output_path, fuzzer, "crashes")

            if not os.path.isdir(crashes_dir):
                # if this entry doesn't have a crashes directory, just skip it
                continue

            for crash in os.listdir(crashes_dir):
                if crash == "README.txt":
                    # skip the readme entry
                    continue

                attrs = dict(map(lambda x: (x[0], x[-1]), map(lambda y: y.split(":"), crash.split(","))))
                signals = [signal.SIGSEGV, signal.SIGILL]
                if int(attrs['sig']) not in signals:
                    continue

                crash_path = os.path.join(crashes_dir, crash)
                with open(crash_path, 'rb') as f:
                    crashes.append(f.read())
        self.write("<br><br>".join(crashes))

class Defect_Mining_Binary_Start_Handler(WiseHandler):
    def post(self):
        id = self.get_argument("id", None, strip=True)
        sql = 'select binary_name FROM binarys WHERE id = %s' % id
        binary_name = db.get(sql)['binary_name']

        tasks.fuzz.delay(binary_name)
        sql = 'update binarys SET status=1 WHERE id = %s' % id
        db.execute(sql)
        self.write('finished!')

class Defect_Mining_Binary_Delete_Handler(WiseHandler):
    def post(self):
        id = self.get_argument("id", None, strip=True)
        sql = 'select binary_name FROM binarys WHERE id = %s' % id
        binary_name = db.get(sql)['binary_name']

        sql = 'delete FROM binarys WHERE id = %s' % id
        db.execute(sql)

        filepath = os.path.join(os.path.dirname(__file__), '../../binarys/%s' % binary_name)
        output_path = os.path.join(os.path.dirname(__file__), '../../output/%s' % binary_name)
        if(os.path.exists(filepath)):
            os.remove(filepath)
        subprocess.Popen('rm -rf %s' % output_path, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	self.write('finished!')

class Defect_Mining_Binary_Upload_Handler(WiseHandler):
    def post(self):
        upload_path = os.path.join(os.path.dirname(__file__), '../../binarys')
        file_metas = self.request.files['file']
        for meta in file_metas:
            filename = meta['filename']
            filepath = os.path.join(upload_path, filename)
            if(os.path.exists(filepath)):
                self.send_error(100)
                return

            with open(filepath, 'wb') as up:
                up.write(meta['body'])
            subprocess.Popen('chmod +x %s' % filepath, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            file_size = round(float(len(meta['body'])) / 1024, 2)
            sql = 'insert INTO binarys (binary_name,file_size,status,upload_datetime,update_datetime) VALUES ("%s",%s,%s,now(),now())' \
                  % (filename, file_size, 0)
            db.execute(sql)
            self.write('finished!')

class Defect_Mining_Binarys_Data_Handler(WiseHandler):
    def get(self):
        table = 'binarys'
        sql = "select * from %s" % table
        results = db.query(sql)
        for result in results:
            result['upload_datetime'] = result['upload_datetime'].strftime('%Y-%m-%d %H:%M:%S')
            result['update_datetime'] = result['update_datetime'].strftime('%Y-%m-%d %H:%M:%S')
        results = {'binarys': results}
        self.write(json.dumps(results))

class Defect_Mining_Binarys_Page_Handler(WiseHandler):
    def get(self):
        self.render("mining/binarys.html")

class Defect_Mining_Logs_Data_Handler(WiseHandler):
    def get(self):
        def get_last_n_lines(logfile, n):
            blk_size_max = 4096
            n_lines = []
            with open(logfile, 'rb') as fp:
                fp.seek(0, os.SEEK_END)
                cur_pos = fp.tell()
                while cur_pos > 0 and len(n_lines) < n:
                    blk_size = min(blk_size_max, cur_pos)
                    fp.seek(cur_pos - blk_size, os.SEEK_SET)
                    blk_data = fp.read(blk_size)
                    assert len(blk_data) == blk_size
                    lines = blk_data.split('\n')

                    # adjust cur_pos
                    if len(lines) > 1 and len(lines[0]) > 0:
                        n_lines[0:0] = lines[1:]
                        cur_pos -= (blk_size - len(lines[0]))
                    else:
                        n_lines[0:0] = lines
                        cur_pos -= blk_size

                    fp.seek(cur_pos, os.SEEK_SET)

            if len(n_lines) > 0 and len(n_lines[-1]) == 0:
                del n_lines[-1]
            return "<br>".join(n_lines[-n:])

        type = self.get_argument("type", None, strip=True)
        if type == "fuzzer":
            p = subprocess.Popen('tail log/fuzzer-err.log -n 40 | ./ansi2html.sh --bg=dark --palette=tango', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            stdout, stderr = p.communicate()
            self.write(stdout)
        elif type == "concolic":
            p = subprocess.Popen('tail log/concolic-err.log -n 40 | ./ansi2html.sh --bg=dark --palette=tango', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            stdout, stderr = p.communicate()
            self.write(stdout)

class Defect_Mining_Logs_Page_Handler(WiseHandler):
    def get(self):
        self.render("mining/logs.html")
