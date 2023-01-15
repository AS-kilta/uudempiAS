#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import datetime

import os.path as osp
import sys
from pathlib import Path
from os import listdir, remove

# Fix this
#from filelock import FileLock

'''
Script generates new toimarit or toimarit_en.yaml file based on the given input.
By default this script generates new toimarit_en based on toimarit.yaml file.
If you want to generate toimarit from toimarit_en give "inv" as function argument
when running the script.

In short script for copying data between two YAMLs for different languages.


Note that sometimes you have to update officials_mapping dictionary.

Hope this helps updating toimarit.yaml


## Version history ##
Version 1.1 9.1.2022  - Ville Eronen
Version 0.5 12.7.2020 - Ville Eronen
Version 0.1 24.2.2019 - Jyri Kolu
'''


# Does not work with é, ä, ö, å...
PICTURE_OVERRIDE ={
    'arttu rintala' : '2019/arttu_rintala_19.jpg',
    'tiia-maria hyvonen': '2020/tiia_hyvonen.jpg',
    'jaakko majuri': '2019/jaakko_majuri_19.jpg',
    'leevi hormaluoma': '2021/leevi_hormaluoma.jpg',
    'veera ihalainen': '2021/veera_ihalainen_2.jpg'
}


## TODO: Add better pwd detection!


# NOTE: Deprecated
def generate_picture_list(path_ : str, years : list) -> list:
    lists = [ [], [], [] ]
    for idx, year in enumerate(years):
        path = osp.join('../' + path_, str(year))
        lists[idx] = [f for f in listdir(path) if osp.isfile(osp.join(path, f))]

    return lists


## NOTE: Deprecated
def get_person_picture_list(src_str_: str, person_: str, picture_list_ : list, user_args) -> str:

    file_name = '_'.join(person_.lower().rsplit()) + '.jpg'
    picture = osp.join(user_args.pic,'aebaej_placeholder.png')

    for idx, year in enumerate(user_args.years):

        pictures = [element for element in picture_list_[idx] if file_name in element]

        if pictures:
            path    = osp.join(user_args.pic, str(year))
            picture = osp.join(path, pictures[0])
            break

    pic_pos = src_str_.find('picture: ')
    picture_str = str(src_str_[0:pic_pos+len('picture: ')] + picture + '\n').replace('\\', '/')
    return picture_str


# NOTE: Deprecated
def sort_officials(mapping : dict):
    save_data = 'OFFICIAL_POSITIONS = {'

    for key, value in sorted(mapping.items()):
        save_data += "'''"+key+"''': '''" +value+"''', " if "'" in value or "'" in key else "'"+key+"': '" +value+"', "
    save_data += "}"

    handle_file('officials_sorted.temp', save_data.replace("', }", "'}\n"))


## TODO: refactor!
def handle_file(destinatio : str, data_write=''):
    data = ''
    mode = 'r' if not data_write else 'w'

    try:
        print('Locking file: ' + destinatio)

        # io.
        with open(destinatio, mode, encoding='utf8') as f:

            if mode == 'r':
                data = f.readlines()
            else:
                f.writelines(data_write)

        if osp.exists(destinatio + '.lock'):
            remove(destinatio + '.lock')
        print('Releasing file: ' + destinatio)

    except (OSError, IOError) as error:
        print(error)

    return data


## Add better key detection.
def map_officials(src_str : str, mapping : dict) -> tuple:

    src_split = src_str.split()
    pattern = ' '.join(src_split[2:len(src_split)])

    name = pattern.replace('ä','a').replace('ö','o').replace('Å', 'a').replace('é', 'e')
    mapped_str = (src_str, name) if pattern not in mapping else (src_str.replace(pattern, mapping[pattern]), '')

    return mapped_str


def update_picture_dict_from_file(picture_dict : dict, file_tuple : list) -> dict:

    for file_name, file_path in file_tuple:
        name = file_name.replace('.jpg','').split('_')

        if len(name) < 2:
            continue

        file_path = file_path.replace('\\', '/')

        if f'{name[0]} {name[1]}' not in picture_dict:
            picture_dict.update({f'{name[0]} {name[1]}':[file_path]})
        else:
            picture_dict[f'{name[0]} {name[1]}'].append(file_path)

    return picture_dict


def generate_picture_dict(path_ : str, years : list) -> dict:
    picture_dict = {}

    for idx, year, in enumerate(years):
        path = osp.join('../' + path_, str(year))
        file_tuple = [(f, osp.join(path.replace('../',''), f)) for f in listdir(path) if osp.isfile(osp.join(path, f))]
        picture_dict = update_picture_dict_from_file(picture_dict, file_tuple)

    return picture_dict


def make_figure_str(src_str : str, suggested_picture : str) -> str:
    pic_pos = src_str.find('picture: ')
    return str(src_str[0:pic_pos+len('picture: ')] + suggested_picture + '\n').replace('\\', '/')

    
# TF KE
def get_person_picture_dict(picture_dict : dict, person : str, src_str : str, pic_path : str) -> dict:

    person = person.lower()

    if picture_dict.get(person,'') and person not in PICTURE_OVERRIDE:
        return make_figure_str(src_str, picture_dict[person][0])

    if picture_dict.get(person,'') and person in PICTURE_OVERRIDE:
        picture_path = osp.join(pic_path, PICTURE_OVERRIDE.get(person)).replace('\\', '/')
        if picture_path in picture_dict[person]:
            return make_figure_str(src_str, picture_path)

    picture_path = osp.join(pic_path, PICTURE_OVERRIDE.get(person)).replace('\\', '/') if PICTURE_OVERRIDE.get(person, '') else ''

    if picture_dict.get(person,''):
        suggested_picture = picture_dict[person][0]

        if osp.exists('../'+picture_path) and picture_path not in picture_dict[person]:
            picture_dict[person].append(picture_path)
            suggested_picture = picture_path

    else:
        suggested_picture = osp.join(pic_path, 'aebaej_placeholder.png').replace('\\', '/')

        if osp.exists('../'+picture_path) and picture_path:
            suggested_picture = picture_path

        picture_dict.update({person: [suggested_picture]})
    
    return make_figure_str(src_str, suggested_picture)


def data_tinkering(src_data: str, user_args) -> str:
    # deep copy?
    dst_data = src_data
    mapping = user_args.mapping

    # Move to dictionary
    pictute_dict = generate_picture_dict(user_args.pic, user_args.years)

    person = ''
    for dst_idx, src_str in enumerate(src_data):
        row_str = src_str

        if '- name:' in src_str:
            row_str, person = map_officials(src_str, mapping)

        if 'picture:' in src_str:
            row_str = get_person_picture_dict(picture_dict=pictute_dict, person = person, src_str = src_str, pic_path = user_args.pic)

        dst_data[dst_idx] = row_str

    return dst_data


def check_path(str_ : str) -> str:
    if not Path(str_).exists():
        msg = str(str_ + ' directory not found!')
        raise argparse.ArgumentTypeError(msg)
    return str_


def get_user_arguments(arg_parser):
    arg_parser.add_argument('-src', '--src_path', default = '../_data/toimarit.yaml',
                            nargs = 1, type = check_path, metavar = (''),
                            dest='src', help = 'Path for toimarti.yaml. Default: _data/toimarit.yaml')

    arg_parser.add_argument('-dst', '--dst_path', default = '../_data/toimarit_en.yaml',
                            nargs = 1, type = check_path, metavar = (''),
                            dest='dst', help = 'Path for toimarti.yaml. Default: _data/toimarit_en.yaml')

    arg_parser.add_argument('-pic', '--pic_path', default = 'static/toimijat',
                            nargs = 1, type = str, metavar = (''),
                            dest='pic', help = 'Path for official pictures. Default: static/toimijat')

    # Add better pwd detection!
    arg_parser.add_argument('-off', '--officials', default = 'officials_translations.txt',
                            nargs = 1, type = str, metavar = (''),
                            dest='off', help = 'Path for translation table. Default: officials_translations')

    arg_parser.add_argument('-inv', '--inverse', action = 'store_true', default = False,
                            dest='inv', help = 'TODO')


def get_positions(path : str) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    official_mapping = {}
    for line in lines:
        temp = line.split('=')
        official_mapping.update({temp[0]: temp[1].rstrip()})

    return official_mapping


def determine_mapping(user_args) -> dict:
    return get_positions(user_args.off) if not user_args.inv else {value: key for key, value in get_positions(user_args.off).items()} 


def main():
    arg_parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=('')
    )

    get_user_arguments(arg_parser)
    user_args = arg_parser.parse_args()

    setattr(user_args, 'year', datetime.datetime.now().year)
    setattr(user_args, 'years', [user_args.year - i for i in range(0, 3)])
    setattr(user_args, 'mapping', determine_mapping(user_args))

    #sort_officials()

    src_data = handle_file(user_args.src) if not user_args.inv else handle_file(user_args.dst)
    dst_data = data_tinkering(src_data, user_args)

    handle_file(user_args.dst, dst_data) if not user_args.inv else handle_file(user_args.src, dst_data)


if __name__ == '__main__':
    sys.exit(main())
