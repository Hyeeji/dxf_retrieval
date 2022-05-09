import os
import json
import math
import pickle
import pandas as pd

base = []
none_base = 0
sticker = []
none_sticker = 0
none_data = 0
err = set()
cor = set()


def code_variational_generator(code):
    var_letters_fb = ['F','B']
    var_letters_lr = ['L','R']
    var_letter_comb = [(x,y) for x in var_letters_fb for y in var_letters_lr]
    code_var = [code]
    code_var.extend([code + '_' + x for x in var_letters_fb + var_letters_lr])
    code_var.extend([x + '_' + code for x in var_letters_fb + var_letters_lr])
    code_var.extend([x[0] + '_' + code + '_' + x[1] for x in var_letter_comb])
    code_var.extend([x[1] + '_' + code + '_' + x[0] for x in var_letter_comb])

    return code_var


def get_feature(category_name):
    c_name = category_name

    category_name = category_name.replace('+', '-')
    category_id = -1
    feat_id = -1

    for cat in category['categories']:
        cat_name = cat['name']
        cat_name = cat_name.rsplit(sep='-', maxsplit=1)[0]
        if cat_name == category_name:
            category_id = cat['id']
            break

    if category_id == -1:
        if c_name in base:
            global none_base
            none_base += 1
        elif c_name in sticker:
            global none_sticker
            none_sticker += 1
        else:
            global none_data
            none_data += 1
        err.add(c_name)
        return 0.

    for i in range(len(feat_pickle[2])):
        if feat_pickle[2][i] == category_id:
            feat_id = i
            break

    if feat_id == -1:
        return 0.

    cor.add(category_name)

    return feat_pickle[1][feat_id].tolist()


def matching_strategy(excel_code, pattern_codes_in_json):
    # code_var이 붙은 경우까지 포함해서 맵핑
    code_variation = code_variational_generator(excel_code)
    result = {k: pattern_codes_in_json[k] for k in pattern_codes_in_json if k in code_variation}
    return result


def name_mapping(filename_prefix):
    if filename_prefix.find('MH') != -1:
        return 'top_sweatshirt_hood'
    if filename_prefix.find('PL') != -1:
        return 'bottom_trousers'
    if filename_prefix.find('SH') != -1:
        return 'top_shirt'


def concat_string_with(delim, *arg):
    result = ''
    for s in arg:
        result += s
        result += delim

    return result[:-1]


def fetch_sketch_names(sketch_dict):
    svg_name = []
    for layer1 in sketch_dict.keys():
        for layer2 in sketch_dict[layer1]:
            for layer3 in sketch_dict[layer1][layer2]:
                svg_name.append(concat_string_with('+',layer1,layer2,layer3))

    return svg_name


def fetch_pattern_codes(pattern_dict):
    pattern_code = {}
    blk_codes = []

    for file in pattern_dict.keys():
        for blk_file in pattern_dict[file]:
            for blk_code in pattern_dict[file][blk_file]:
                if blk_code != '':
                    pattern_code[blk_code] = file.split('.')[0] + '/' + blk_file
                    blk_codes.append(blk_code)

    if len(blk_codes) != len(set(blk_codes)):
        print('블럭 코드 중복 있음!')

    return pattern_code


def read_excel(path):
    base_sheet = pd.read_excel(path, sheet_name=0, header=0)
    base_mapping = {}
    num_record = len(base_sheet['svg_name'])

    for i in range(num_record):
        full_name = concat_string_with('+', base_sheet['garment_type'][i], base_sheet['layer1'][i],
                                       base_sheet['layer2'][i], base_sheet['layer3'][i])
        base.append(full_name)
        mapping = base_sheet['구성 패턴 조각'][i]
        if type(mapping) != str and math.isnan(mapping):
            mapping = None

        ob_dict = {'own': mapping, 'belong': None}
        base_mapping[full_name] = ob_dict

    sticker_sheet = pd.read_excel(path,sheet_name=1,header=0)
    sticker_mapping = {}
    num_record = len(sticker_sheet['svg_name'])
    for i in range(num_record):
        full_name = concat_string_with('+',  sticker_sheet['garment_type'][i], sticker_sheet['layer1'][i],
                                       sticker_sheet['layer2'][i], sticker_sheet['layer3'][i])
        sticker.append(full_name)
        mapping1 = sticker_sheet['구성 패턴 코드'][i]
        if type(mapping1) != str and math.isnan(mapping1):
            mapping1 = None
        mapping2 = sticker_sheet['종속 몸판 패턴(BD or SL)'][i]
        if type(mapping2) != str and math.isnan(mapping2):
            mapping2 = None
        ob_dict = {'own': mapping1, 'belong': mapping2}
        sticker_mapping[full_name] = ob_dict


    base_mapping.update(sticker_mapping)

    blk_set = set()
    for map in base_mapping:
        if base_mapping[map]['own']:
            base_mapping[map]['own'] = [x.strip() for x in base_mapping[map]['own'].split(',')]
            blk_set.update(base_mapping[map]['own'])
        if base_mapping[map]['belong']:
            base_mapping[map]['belong'] = [x.strip() for x in base_mapping[map]['belong'].split(',')]
            blk_set.update(base_mapping[map]['belong'])

    return base_mapping, blk_set


def generate_database_file(outpath, database, mapping):
    mappingdata = {}
    mappingdata['cloth'] = []
    for filename in database:
        cloth = {}
        cloth['svgFile'] = filename + '.svg'
        cloth['pattern'] = []
        for svg_name in database[filename]['svg_names']:
            patterns = {}
            patterns['category'] = svg_name
            patterns['feature'] = get_feature(svg_name)
            if svg_name in mapping: # mapping data 존재
                mapping_blocks = mapping[svg_name]['own']
                # matching_strategy(excel_code, mapping_blocks)
                blocks = {}
                if mapping_blocks != None:
                    for mapping_block in mapping_blocks:
                        block_info = matching_strategy(mapping_block, database[filename]['pattern_codes'])
                        blocks.update(block_info)

                patterns['blocks'] = blocks
            else:
                patterns['blocks'] = None

            cloth['pattern'].append(patterns)

        mappingdata['cloth'].append(cloth)

    with open(outpath, "w") as json_file:
        json.dump(mappingdata, json_file, indent=4)


if __name__ == '__main__':
    main_json_dir = 'D:/Pattern_dataset/sketch-pattern_dataset'
    mapping_xls_path = 'D:/Pattern_dataset/svg_database+pattern_code_ver4.xlsx'
    database_out_path = 'database.json'
    category_path = '../../files/categories.json'
    feature_path = '../../files/features_thr_0.3.pkl'

    # 엑셀 파일의 모든 필요한 맵핑 정보 불러오기
    mapping, blk_set = read_excel(mapping_xls_path)

    json_list = os.listdir(main_json_dir)
    json_list.sort()
    database = {}

    with open(category_path) as category_json:
        category = json.load(category_json)

    with open(feature_path, 'rb') as f:
        feat_pickle = pickle.load(f)

    for item in json_list:
        print('Processing {}...'.format(item))
        item_path = os.path.join(main_json_dir,item)
        if os.path.isfile(item_path):
            with open(item_path,'r') as main_json:
                data = json.load(main_json)

                svg_names = fetch_sketch_names(data['sketch'])
                name_prefix = name_mapping(item)
                svg_names = [concat_string_with('+',name_prefix,x) for x in svg_names]

                pattern_codes = fetch_pattern_codes(data['pattern'])
                sp_dict = {'svg_names': svg_names, 'pattern_codes': pattern_codes}
                database[item.split('.')[0]] = sp_dict

    generate_database_file(database_out_path, database, mapping)
    print(none_base, none_sticker, none_data)
    print(len(base), len(sticker))
    print(len(err), len(cor))
    print(err)
    print(cor)
