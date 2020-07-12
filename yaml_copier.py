#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import os
import sys

from filelock import FileLock

'''
Script generates new toimarit or toimarit_en.yaml file based on the given input.
By default this script generates new toimarit_en based on toimarit.yaml file.
If you want to generate toimarit from toimarit_en give "inv" as function argument
when running the script.

In short script for copying data between two YAMLs for different languages.


Note that sometimes you have to update officials_mapping dictionary.

Hope this helps updating toimarit.yaml
'''

src_path = '_data/toimarit.yaml'
dst_path = '_data/toimarit_en.yaml'


officials_mapping = {
    'Tosi ISOpomo': 'Uncle Tutor Boss', 'ISOpomo': 'Tutor Boss',
    '''Maisteri-informaatti''': '''Master's Informant''', 'Informaatti': 'Informant',
    'Lukkaritoimikunta': 'Sexton Committee','Lukkarimestari': 'Sexton Master', 'Lukkari': 'Sexton',
    
    'ASkimestari': 'ASkimaster', 'ASkitoimikunta': 'ASki Committee',
    'ASkivahti': 'ASki Guardian','Abisintti': 'Abisinth', 'Automaatti': 'Automaton',
    'DSDeetti': 'DSDent', 'Depressantti': 'Depressant', 'Dokumentoija': 'Documentator',
    'Excursiovastaava': 'Excursion Coordinator', 'Fuksitoimikunta': 'Freshman committee',
    'Graafikko': 'Graphics Designer', 'Hattivatti': 'Hattifattener',
    'Huvitoimikunta': 'Entertainment Committee', 'Juomanlaskija': 'Cupbearer', 'Jäykkäranne': 'Stiff Wrist',
    'Kultainen päätoimittaja': 'Golden Editor-in-Chief', 'Kultainen toimittaja': 'Golden Editor',
    'Kultainen toimitus': 'Golden Tomato', 'Kulttuuri- ja liikuntatoimikunta': 'Cultural Affairs Committee',
    'Kulttuurikisälli': 'Cultural Journeyperson', 'Laulukirjatoimikunta': 'Songbook Committee',
    'Liikkuja': 'Sports Manager', 'Mediatoimikunta': 'Media Committee', 'Oltermanni': 'Alderman',
    'Opintotoimikunta': 'Study Committee', 'Pelaaja': 'Gamer', 'Puheenjohtaja': 'Head of Committee',
    'Seniilisihteeri': 'Senile Secretary', 'Somevastaava': 'Social Media Manager', 'Stigulantti': 'Stigulant',
    'Stigutoimikunta': 'Stigu Committee', 'Stiguäbäj': 'Stiguäbäj', 'Stimulaatio-toimikunta': 'Stimulaatio Committee',
    'Stimulantti': 'Stimulant', 'SuurPhuksikapteeni': 'Great Freshman Captain', 'Säätömestari': 'Head of Technology',
    'Säätötoimikunta': 'Technology Committee', 'TEKSAS Ranger': 'TEKSAS Ranger',
    'Toimikuntien ulkopuolelta': 'Outside the Committees', 'Toiminnantarkastaja': 'Inspector',
    'Toimittaja': 'Editor', 'Varatoiminnantarkastaja': 'Vice-inspector',
    'Visuaalinen ilme': 'Visual Design', 'Yrityssuhdekisälli': 'Corporate Relations Journeyperson',
    'Yrityssuhdeneuvonantaja': 'Corporate Relations Consultant',
    'Yrityssuhdetoimikunta': 'Corporate Relations Committee', 'rrrRankkavastaava': 'rrrRankka Correspondent'
}


def sort_officials():
    print("Some officials name might be a subset of another name!")
    save_data = 'officials_mapping = {'
    for key, value in sorted(officials_mapping.items()):
        if "'" in value or "'" in key:
            save_data += "'''"+key+"''': '''" +value+"''', "
        else:
            save_data += "'"+key+"': '" +value+"', "
    save_data += "}"
    save_data = save_data.replace("', }", "'}\n")
    handle_file('officials_sorted.temp', 'w', save_data)


def variable_mapping(src_data, gen_type='gen'):
    dst_data = src_data
    mapping = officials_mapping

    if gen_type == 'inv':
        mapping = {v: k for k, v in officials_mapping.items()}

    dst_row = 0
    for src_row in src_data:
        dst_data[dst_row] = src_row
        for key, value in mapping.items():
            if key in src_row:  # TODO: improve key detection
                dst_data[dst_row] = src_row.replace(key, value)
                break
        dst_row += 1

    return dst_data


def handle_file(destinatio=src_path, mode='r', data_write=None):
    data = ''
    try:
        print('Locking file: ' + destinatio)
        with FileLock(destinatio + '.lock'):

            with io.open(destinatio, mode, encoding='utf8') as f:
                if mode == 'r':
                    data = f.readlines()
                else:
                    f.writelines(data_write)
        if os.path.exists(destinatio + '.lock'):
            os.remove(destinatio + '.lock')
        print('Releasing file: ' + destinatio)

    except (OSError, IOError) as error:
        print(error)

    return data


def main():
    if not os.path.isfile(src_path) or not os.path.isfile(dst_path):
        print("Invalid file paths or names.")
        sys.exit(1)

    #sort_officials()

    if len(sys.argv) == 2 and sys.argv[1] == 'inv':
        src_data = handle_file(dst_path)
        dst_data = variable_mapping(src_data, 'inv')
        handle_file(src_path, 'w', dst_data)

    else:
        dst_data = variable_mapping(handle_file())
        handle_file(dst_path, 'w', dst_data)

if __name__ == '__main__':
    sys.exit(main())
