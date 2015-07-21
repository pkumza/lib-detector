# -*- coding:utf-8 -*-
# Created at 2015/7/20

"""
    Function:
        ***
"""
__author__ = 'Marchon'

import ConfigParser
import glob
import re
import os
import pymongo
import get_smali
import subprocess
import thread


def get_config(section, key):
    """
    Load the config File : into_database.conf
    载入设置文件 : into_database.conf
    """
    config = ConfigParser.ConfigParser()
    path = 'into_database.conf'
    config.read(path)
    return config.get(section, key)


def main_func():
    """
    Main Function
    主方法
    """
    print("Main_Function Start.")
    conn = pymongo.MongoClient(get_config('database', 'db_host'), int(get_config('database', 'db_port')))
    db = conn.get_database(get_config('database', 'db_name'))
    packages = db.get_collection(get_config('database', 'db_packages'))
    db_api_dict = db.get_collection(get_config('database', 'db_dict'))
    api_dict = {}

    # Regex Expression for Android API
    # 字符串API的匹配
    p = re.compile(r'Landroid/.*?;?\-?>*?\(|Ljava/.*?;?\-?>*?\(|Ljavax/.*?;?\-?>*?\(|Lunit/runner/.*?;?\-?>*?\('
                   r'|Lunit/framework/.*?;?\-?>*?\('
                   r'|Lorg/apache/commons/logging/.*?;?\-?>*?\(|Lorg/apache/http/.*?;?\-?>*?\(|Lorg/json/.*?;'
                   r'?\-?>*?\(|Lorg/w3c/.*?;?\-?>*?\(|Lorg/xml/.*?;?\-?>*?\(|Lorg/xmlpull/.*?;?\-?>*?\(|'
                   r'Lcom/android/internal/util.*?;?\-?>*?\(')

    def load_api_dict():
        """
        Load API Dictionary in Database if it exits.
        载入API词典，如果存在的话。
        """
        if db_api_dict.find().count() != 0:
            for item in db_api_dict.find():
                api_dict[item['key']] = item['value']

    load_api_dict()

    def get_number(string):
        """
        Get API ID From API Dictionary.
        获得API的编号
        :param string: API Name
        :return: API ID
        """
        if string not in api_dict:
            api_dict[string] = len(api_dict)
            db_api_dict.insert({"key": string, "value": len(api_dict)})
        return str(api_dict[string])

    find_file = re.compile(r'.smali$')

    def into_db(apk_path):
        """
        Read smali files in apk_path directory and then put the features into Database.
        读取位于apk_path位置的文件，并且把相关的特征存入数据库。
        :param apk_path: The position of decoded apk
        :return: None
        """
        print ("Log: \n \t Function: %s \n \t Para : %s \n" %('into_db', apk_path))
        print ("Log: \n \t Path : %s " % (apk_path+'/smali'))
        if os.path.exists(apk_path+'/smali'):
            os.chdir(apk_path+'/smali')
            all_over(apk_path, apk_path+'/smali')
            os.chdir(apk_path)

    def all_over(apk_path, path):
        """
        Recursive body of package for getting the features and putting them into Database.
        :param apk_path: APK Path
        :param path: Packages Path
        :return: API Dict of this package, Directory Number in this Package, File Number, Total API Call.
        """
        all_thing = glob.glob('*')
        this_call_num = 0
        this_dir_num = 0
        this_file_num = 0
        direct_dir_num = 0
        direct_file_num = 0
        this_dict = {}
        for thing in all_thing:
            # If the thing is a directory.
            if os.path.isdir(thing):
                os.chdir(path+'/'+thing)
                # Merge Dictionary
                # 合并字典
                child = all_over(apk_path, path+'/'+thing)
                if child is not None:
                    this_dict.update(child[0])
                    this_dir_num += child[1] + 1
                    direct_dir_num += 1
                    this_file_num += child[2]
                    this_call_num += child[3]
                os.chdir(path)
            # If the thing is a file
            else:
                try:
                    # Is this file a smali file?
                    if not find_file.search(thing):
                        continue
                    f = open(thing, 'r')
                    for u in f:
                        # For every line in this file.
                        match = p.findall(u)
                        for system_call in match:
                            if '"' in system_call:
                                continue
                            this_call_num += 1
                            if "\"" in system_call or "'" in system_call or "“" in system_call or "‘" in system_call:
                                continue
                            if ";->" not in system_call:
                                continue
                            call_num = get_number(system_call)
                            if call_num in this_dict:
                                this_dict[call_num] += 1
                            else:
                                this_dict[call_num] = 1
                    f.close()
                    this_file_num += 1
                    direct_file_num += 1
                except Exception as ex:
                    print('Can not Open ' + thing + ' Wrong with:' + str(ex))
        # Remove all the Log API
        # 去除所有的关于Log的API，来去除插桩或者其他因素造成的影响
        logs = ['Landroid/util/Log;->v(', 'Landroid/util/Log;->e(', 'Landroid/util/Log;->w(',
                'Landroid/util/Log;->i(', 'Landroid/util/Log;->d(']
        for log in logs:
            if get_number(log) in this_dict:
                del this_dict[get_number(log)]
        # If there is no API call in this package, just ignore it.
        if len(this_dict) == 0:
            return
        parts = path[len(apk_path)+7:].split("/")
        if parts[0] == '':
            depth = 0
        else:
            depth = len(parts)
        package = {'apk': apk_path,                         # Ahe APK file storing path
                   'path': path,                            # The Packages' path
                   'path_parts': parts,                     # Parts of Path
                   'depth': depth,                     # Directory Depth
                   'total_num': len(this_dict),             # Total API Types
                   'total_call': this_call_num,             # Total API Calls
                   'dir_num': this_dir_num,                 # The number of all the directories in this package
                   'file_num': this_file_num,               # The number of all the code files in this package
                   'direct_dir_num': direct_dir_num,        # The number of directories directly in this package
                   'direct_file_num': direct_file_num,      # The number of code files directly in this package
                   'api_dict': this_dict,                   # API Dict
                   'status': 0
                   # status (0:not_scanned, 1:is_lib_root, 2:is_not_lib, 3:is_lib_child, 4:smali_root)
                   }
        packages.insert(package)
        return this_dict, this_dir_num, this_file_num, this_call_num

    source_list = get_config('source_path', 'source').split(';')
    print 'source_list'

    def runner(source_path):
        """
        Run 8 thread to do this things.
        :param source_path:
        :return:
        """
        print source_path
        dirs = glob.glob(source_path+'/*/*')
        apk_count = 0
        for apk in dirs:
            apk_count += 1
            # 这里做一个log控制
            print("Decoding: " + str(apk_count) + ' APK: ' + apk)
            decoded_path = get_smali.get_smali(apk)
            try:
                into_db(decoded_path)
            except Exception as e:
                print('Wrong Here' + str(e))
            finally:
                # log status 设为已经结束
                subprocess.Popen("rm -rf %s" % decoded_path, shell=True)


    for source_path in source_list:
        thread.start_new_thread(runner, (source_path,))


if __name__ == '__main__':
    main_func()
