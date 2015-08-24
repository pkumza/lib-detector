# -*- coding:utf-8 -*-
# Created at 2015/5/4
# Original Code Created at 2015/4/27
# Modified at 2015/5/4
# Modified at 2015/08/19
"""
    Function:
        Compare packages
    作用：
        比较包

    Usage:
        Modify intodb.conf, then just run this code or import intodb.py then call function 'main_func()'.
    用法：
        修改intodb.conf的设置，然后运行本代码，或者import intodb.py之后调用main_func()方法即可。

    Trivial Notes：
        dep_packages 是第一次尝试，以卡机失败告终。
        dep_packages2 第二次尝试，但是有一些big
        dep_packages3 修复了一些bug，然后尝试增加新的元素，即子元素的path parts都记录下来。

"""
__author__ = 'Zachary Marv - 马子昂'

import ConfigParser
import pymongo
import sys
import time


def get_config(section, key):
    """
    Load the config File : into_database.conf
    载入设置文件 : into_database.conf
    """
    config = ConfigParser.ConfigParser()
    path = 'hash.conf'
    config.read(path)
    return config.get(section, key)


class TimeRecord:
    """
    Made for Time Recording.
    用来计时。
    """
    def __init__(self):
        self.init_time = time.time()
        self.if_start = False
        self.start_time = 0

    def start(self):
        self.start_time = time.time()
        self.if_start = True
        print('*' * 60)
        print('Task: '+sys.argv[0]+' Starts.')

    def end(self):
        end_time = time.time()
        if self.if_start:
            task_interval = end_time - self.start_time
            print('Task: '+sys.argv[0]+' Ends.')
            m = int(task_interval) / 60
            s = int(task_interval) % 60
            if m <= 1:
                mi = 'minute'
            else:
                mi = 'minutes'
            if s <= 1:
                se = 'second'
            else:
                se = 'seconds'
            print('Consuming '+str(m)+' '+mi+' and '+str(s)+' '+se+'.')
            print('*' * 60)
        self.if_start = False


def main_func():
    """
    Main Function
    主方法
    Run this function to compare every package.
    Input is get_config('database', 'db_pack')
    Output is get_config('database', 'db_dep_pack')
    """

    """
    Connect to the Database and get input and output collection.
    """
    conn = pymongo.MongoClient(get_config('database', 'db_host'), int(get_config('database', 'db_port')))
    db = conn[get_config('database', 'db_name')]
    packages = db[get_config('database', 'db_brief')].find().sort([
        ("depth", pymongo.ASCENDING), ("b_total_call", pymongo.ASCENDING),
        ('b_total_num', pymongo.ASCENDING), ("b_hash", pymongo.ASCENDING)])
    # package = packages.next()
    dep_packages = db[get_config('database', 'db_dep')]
    dep_packages_st_6 = db[get_config('database', 'db_dep_6')]
    dep_packages_st_4 = db[get_config('database', 'db_dep_4')]

    """
        Search the packages among the database.
        We ignore packages which depth is 0, because that means it's a library contains the whole APP. We believe root
    directory is not a library.
        Firstly, we put the packages with the same b_total_call and b_total_num into a list named 'common',when there's no
    more packages having the same b_total_call and b_total_num. Secondly, we compare every package in 'common' list so we
    get every package's parent. At last, calculate the Repetitions as 'dep_num' and insert the packages into a new db
    collection.
        在数据库中对包进行寻找。
        在运行的过程中，会忽略那些深度为0的包。因为那意味着，整个应用都是一个库。
        首先，把相同b_total_call和b_total_num的包放到一个list（列表）中，这个list的名字叫做common，当再也没有package有同样的
    参数的时候，计算这个common列表。common中的内容要进行两两比较，找到每个包的parent（也有可能是它自己），计算每一个包的
    重复次数。最后，把新得到的信息，包括status、parent、重复次数，插入数据库的新的数据集合里。
    """
    common = []
    total_call_plat = 0
    total_num_plat = 0
    total_dep_num = {}

    # Status 0 means have not scanned yet. '0' is packages' initial status.
    status_1_cnt = 0                # Status 1 means lib_root
    status_2_cnt = 0                # Status 2 means non-lib
    status_3_cnt = 0                # Status 3 means lib_child
    status_4_cnt = 0                # Status 4 means directory_root
    status_5_cnt = 0                # Status 5 形如一个文件夹，com，只有一个子文件夹com/admob
    status_6_cnt = 0                # Status 6 means 有重复，且不是代表元素
    dir_parent_dict = {}            # scanned packages' statuses.
    package_count = 0               # count
    packages_num = packages.count()
    cur_p = None
    cur_b = False

    for package in packages.find({"b_total_call": {"$gt": 5}},
                                 {"b_total_call": 1, "b_total_num": 1, "b_hash": 1, "depth": 1, "status": 1,
                                  "path": 1, "s_path": 1}):
        package_count += 1

        # !!!!!!! Important !!!!
        # This is a patch. Delete it when you run this function.
        # Step over Status 4.

        # if package_count < 362982:
        #    continue
        # delete this.

        # We believe root directory is not a library unless the whole App is a library.
        if package['depth'] == 0:
            package['status'] = 4
            dir_parent_dict[package['path']] = 4
            del package['_id']
            dep_packages_st_4.insert(package)
            status_4_cnt += 1
            cur_b = False
            continue

        # If a package has only one directory, and
        '''
        if package['direct_dir_num'] == 1 and package['direct_file_num'] == 0:
            if cur_b:
                if cur_p['dep_num'] > 50:
                    cur_p['status'] = 1
                    status_1_cnt += 1
                else:
                    cur_p['status'] = 2
                    status_2_cnt += 1
                del cur_p['_id']
                dep_packages.insert(cur_p)
            package['status'] = 5
            dir_parent_dict[package['path']] = 5
            del package['_id']
            dep_packages.insert(package)
            status_5_cnt += 1
            cur_b = False
            continue
            '''

        # (if this package's dir_parent is lib, there's no need to compare this package any more.
        # 1 means lib_root; 3 means lib_child, so I use Modulo operation here.)

        # 2015/08/20 We decide to compare package no matter what its parent is.
        '''
        dir_split = package['path'].split('\\')
        dir_parent_split = dir_split[:len(dir_split)-1]
        dir_parent = '\\'.join(dir_parent_split)
        if dir_parent in dir_parent_dict and dir_parent_dict[dir_parent] in [1, 3]:
            # Mark this package as lib_child and insert it into a new Database Collection.
            package['status'] = 3
            dir_parent_dict[package['path']] = 3
            status_3_cnt += 1
            del package['_id']
            dep_packages.insert(package)
            continue
        '''

        if not cur_b:       # if cur_package is not available
            cur_p = package
            cur_p['dep_num'] = 1
            cur_p['pp'] = []
            cur_b = True
            continue

        if package_count != packages_num:
            if package['depth'] == cur_p['depth']:
                if package['b_total_call'] == cur_p['b_total_call']:
                    if package['b_total_num'] == cur_p['b_total_num']:
                        if package['b_hash'] == cur_p['b_hash']:
                            cur_p['dep_num'] += 1
                            # this code made the Database extremely large.
                            # cur_p['pp'].append(package['path'])
                            # Modified 2015/08/21 ->
                            # only mark the unique one.
                            s_path = package['s_path']
                            if s_path not in cur_p['pp']:
                                cur_p['pp'].append(s_path)
                            package['parent'] = cur_p['path']
                            package['status'] = 6
                            status_6_cnt += 1
                            del package['_id']
                            dep_packages_st_6.insert(package)
                            continue

        if cur_p['dep_num'] > 50:
            cur_p['status'] = 1
            status_1_cnt += 1
        else:
            cur_p['status'] = 2
            status_2_cnt += 1

        del cur_p['_id']
        dep_packages.insert(cur_p)
        cur_p = package
        cur_p['dep_num'] = 1
        cur_p['pp'] = []

        """   *************************************************************
        # len(common) == 0 is used just for the first package comes here.
        # the code in the if-statement will only runs once.
        if len(common) == 0:
            total_call_plat = package['b_total_call']
            total_num_plat = package['b_total_num']
            common.append({"package": package, "dep_num": 1, "parent": 0})
        else:
            # if this package is the last package in the database,
            # There's no need to append it into a common list.
            if total_call_plat == package['b_total_call'] and total_num_plat == package['b_total_num']\
                    and package_count != packages_num:
                common.append({"package": package, "dep_num": 1, "parent": 0})
            else:
                print 'Common List Size: '+str(len(common))
                for i in common:
                    if i['parent'] != 0:
                        continue
                    for j in common:
                        if j['parent'] != 0:
                            continue
                        if i['package']['b_hash'] == j['package']['b_hash']:
                            i['dep_num'] += 1
                            j['parent'] = i['package']['path']   # set his parent as i
                        i['parent'] = i['package']['path']       # the parent is himself
                for i in common:
                    if i['parent'] == i['package']['path']:
                        if i['dep_num'] in total_dep_num:
                            total_dep_num[i['dep_num']] += 1
                        else:
                            total_dep_num[i['dep_num']] = 1
                        for j in common:
                            if j['parent'] == i['package']['path']:
                                j['dep_num'] = i['dep_num']
                    package_featured = i['package']
                    del package_featured['_id']
                    # Threshold is set here
                    if i['dep_num'] >= 50:
                        package_featured['status'] = 1          # lib_root
                        status_1_cnt += 1
                    else:
                        package_featured['status'] = 2          # is not lib
                        status_2_cnt += 1
                    dir_parent_dict[package_featured['path']] = package_featured['status']
                    package_featured['dep_parent'] = i['parent']
                    package_featured['dep_num'] = i['dep_num']
                    print package_featured
                    dep_packages.insert(package_featured)
                del common[:]
                # Add three statements here. Actually fixed the Bug in package_compare.py
                total_call_plat = package['b_total_call']
                total_num_plat = package['b_total_num']
                common.append({"package": package, "dep_num": 1, "parent": 0})

                ****************************************************************************"""
    """
    This is a copy of code. I put the code here to deal with the last package.
    放在这里用来处理最后一个common list，因为上面的for循环的话，最后一个common list就没办法处理了。
    这就是为什么之前的代码，会发现rep-packages4比packages总量上少一个。
    理论上这些代码只运行一次。
    """
    """
    for i in common:
        if i['parent'] != 0:
            continue
        for j in common:
            if j['parent'] != 0:
                continue
            if i['package']['b_hash'] == j['package']['b_hash']:
                i['dep_num'] += 1
                j['parent'] = i['package']['path']   # set his parent as i
            i['parent'] = i['package']['path']       # the parent is himself
    for i in common:
        if i['parent'] == i['package']['path']:
            if i['dep_num'] in total_dep_num:
                total_dep_num[i['dep_num']] += 1
            else:
                total_dep_num[i['dep_num']] = 1
            for j in common:
                if j['parent'] == i['package']['path']:
                    j['dep_num'] = i['dep_num']
        package_featured = i['package']
        del package_featured['_id']
        # Threshold is set here
        if i['dep_num'] >= get_config('threshold', 'dep_threshold'):
            package_featured['status'] = 1          # lib_root
            status_1_cnt += 1
        else:
            package_featured['status'] = 2          # is not lib
            status_2_cnt += 1
        dir_parent_dict[package_featured['path']] = package_featured['status']
        package_featured['dep_parent'] = i['parent']
        package_featured['dep_num'] = i['dep_num']
        dep_packages.insert(package_featured)
    del common[:]
    """


    """
    At last, output some statistics into txt file.
    dep_statistics represents the repetitions status.
    status_statistics represents every package's status.
    """
    dep_writer = open('dep_status.txt', 'w')
    for a, b in [(k, total_dep_num[k]) for k in sorted(total_dep_num.keys())]:
        dep_writer.write(str(a)+'\t'+str(b)+'\n')
    dep_writer.close()
    status_writer = open(get_config('dep_statistics', 'status_statistics'), 'w')
    status_writer.write('Status 1 : '+str(status_1_cnt)+'\n')
    status_writer.write('Status 2 : '+str(status_2_cnt)+'\n')
    status_writer.write('Status 3 : '+str(status_3_cnt)+'\n')
    status_writer.write('Status 4 : '+str(status_4_cnt)+'\n')
    status_writer.write('Status 5 : '+str(status_5_cnt)+'\n')
    for a, b in [(k, dir_parent_dict[k]) for k in sorted(dir_parent_dict.keys())]:
        status_writer.write(str(a)+'\t'+str(b)+'\n')
    status_writer.close()
    print 'Status_1 : '+str(status_1_cnt)
    print 'Status_2 : '+str(status_2_cnt)
    print 'Status_3 : '+str(status_3_cnt)
    print 'Status_4 : '+str(status_4_cnt)
    print 'Status_5 : '+str(status_5_cnt)

if __name__ == '__main__':
    print("This code is written by " + __author__ + '\n')
    time_recorder = TimeRecord()
    time_recorder.start()
    main_func()
    time_recorder.end()
