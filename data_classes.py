import random
import os
import pandas as pd

data_dir = 'intent/data/multi-classes'
label_1 = dict()  # 一级分类与id对应关系
label_2 = dict()  # 二级分类与id对应关系
label1_path = dict()  # 每个一级分类有单独的文件，用于存储其所有二级分类信息，包括二级名称和ID
parent_child_relation = dict()  # 一级分类ID与二级分类名对应
child_parent_relation = dict()  # 二级分类名与一级分类ID对应
text_label1 = dict()  # 答案与一级分类名对应
text_label2 = dict()  # 答案与二级分类名对应
text_label_relation_all = dict()


def get_text_label_relation(data):

    # [['如何修改同行人信息', '更换乘机人'], ['退票、改签', '我换航班座位'],...]
    origin_data = read_raw(os.path.join('intent/data', 'samples10000.txt'))
    wrong_label2 = list()
    with open(os.path.join(data_dir, 'wrong_data.txt'), 'w') as f:
        pass
    with open(os.path.join(data_dir, 'wrong_data.txt'), 'a') as f:
        f.write('\t'.join(['label', 'text']) + '\n')
        for i in range(len(origin_data)):
            item = origin_data[i]

            text = item[1]
            label2_name = item[0]
            if label2_name in label_2:
                label2_id = label_2[item[0]]
                label1_id = child_parent_relation[label2_name]

                text_label1[text] = label1_id
                text_label2[text] = label2_id
            else:
                wrong_label2.append(label2_name)
                f.write('\t'.join([label2_name, text]) + '\n')

    write_text_labelid_txt(text_label1,'label1')
    write_text_labelid_txt(text_label2,'label2')

    # with open(os.path.join(data_dir, 'text-label1_id.txt'), 'w') as f:
    #     pass
    # with open(os.path.join(data_dir, 'text-label1_id.txt'), 'a') as f:
    #     f.write('label1_id' + '\t' + 'text' + '\n')
    #     for text in text_label1:
    #         f.write('\t'.join([text, str(text_label1[text])]) + '\n')
    #
    # with open(os.path.join(data_dir, 'text-label2_id.txt'), 'w') as f:
    #     pass
    # with open(os.path.join(data_dir, 'text-label2_id.txt'), 'a') as f:
    #     f.write('label2_id' + '\t' + 'text' + '\n')
    #     for text in text_label2:
    #         f.write('\t'.join([text, str(text_label2[text])]) + '\n')

    wrong_label2 = set(wrong_label2)
    with open(os.path.join(data_dir, 'wrong_label2.txt'), 'w') as f:
        pass
    with open(os.path.join(data_dir, 'wrong_label2.txt'), 'a') as f:
        for i in wrong_label2:
            f.write(i + '\n')

    return text_label1, text_label2


# 写 问题与一级、二级分类id对应关系 文件
def write_text_labelid_txt(data,type):
    with open(os.path.join(data_dir, 'text-'+type+'_id.txt'), 'w') as f:
        pass
    with open(os.path.join(data_dir, 'text-'+type+'_id.txt'), 'a') as f:
        f.write(type+'_id' + '\t' + 'text' + '\n')
        for text in data:
            f.write('\t'.join([text, str(data[text])]) + '\n')


def train_dev_test(label=1):
    file = os.path.join(data_dir, 'text-label'+str(label)+'_id.txt')
    data = read_raw(file)
    random.shuffle(data)

    dev_idx = int(len(data) * 0.7)
    test_idx = int(len(data) * 0.85)

    prefix = 'label' + str(label)
    task_data_dir = data_dir+'/task_data/'+prefix
    with open(os.path.join(task_data_dir, 'train.txt'), 'w') as f:
        pass
    with open(os.path.join(task_data_dir, 'dev.txt'), 'w') as f:
        pass
    with open(os.path.join(task_data_dir, 'test.txt'), 'w') as f:
        pass

    str_header = 'text\t' + 'label' + '\n'

    train_file = open(os.path.join(task_data_dir, 'train.txt'), 'a')
    train_file.write(str_header)
    dev_file = open(os.path.join(task_data_dir, 'dev.txt'), 'a')
    dev_file.write(str_header)
    test_file = open(os.path.join(task_data_dir, 'test.txt'), 'a')
    test_file.write(str_header)

    for i in range(len(data)):
        if i <= dev_idx:
            train_file.write('\t'.join([data[i][0], data[i][1]]) + '\n')
        elif i > dev_idx and i <= test_idx:
            dev_file.write('\t'.join([data[i][0], data[i][1]]) + '\n')
        else:
            test_file.write('\t'.join([data[i][0], data[i][1]]) + '\n')


# 读输入数据
def read_raw(file_name):
    data = []
    line_num = 0
    with open(file_name) as f:
        for line_ in f:
            line_num += 1
            if line_num > 1:
                data.append(line_.strip().split('\t'))
    return data


# 获取一级分类并创建一级分类ID
def get_label_1(file):
    data_pd = pd.read_csv(file, sep='\t')
    label_1_tmp = set(data_pd['label_1'])

    label1_dict = dict()
    index = 0
    for c in label_1_tmp:
        label1_dict[c] = index
        index += 1

    with open(os.path.join(data_dir, 'label_1.txt'), 'w') as f:
        pass
    with open(os.path.join(data_dir, 'label_1.txt'), 'a') as f:
        for key in label1_dict:
            # if mkdir_label_1(key):  # 是否使用文件夹，待定

            # f.write('\t'.join([key, str(label1_dict[key])]) + '\n')
            f.write(key + '\n')

            # 创建每个label_1的txt文件，用于存储它的二级分类
            filename_label1 = data_dir + '/label_1/' + key + '.txt'
            label1_path[label1_dict[key]] = filename_label1  # key:一级id value:一级分类的子分类文件
            with open(filename_label1, 'w') as f_label1:
                f_label1.close

    return label1_dict


# 获取二级分类并创建一级分类ID
def get_label_2(file):
    data_pd = pd.read_csv(file, sep='\t')
    label2_tmp = set(data_pd['label_2'])

    # 二级分类ID创建
    label2_dict = dict()
    index = 0
    for c in label2_tmp:
        label2_dict[c] = index
        index += 1

    # 二级分类名与ID对应关系 写入文件label_2.txt
    with open(os.path.join(data_dir, 'label_2.txt'), 'w') as f:
        pass
    with open(os.path.join(data_dir, 'label_2.txt'), 'a') as f:
        for key in label2_dict:
            f.write('\t'.join([key, str(label2_dict[key])]) + '\n')

    return label2_dict


# 为一级分类创建文件夹（暂时没用）
def mkdir_label_1(label_name):
    dir_label_1 = data_dir + '/label_1'
    path = os.path.join(dir_label_1, label_name)
    # 判断一个目录是否存在
    if os.path.exists(path) == False:
        # 创建目录
        os.makedirs(path)
    return True


# 二级分类与一级分类ID对应关系
def get_label_relation():
    dir = data_dir + '/label_1'
    for i in range(len(data)):

        label1_name = data[i][1]
        label1_id = label_1[label1_name]
        label2_name = data[i][0]

        # 将二级分类分到对应的一级分类下
        if label1_id not in parent_child_relation:
            parent_child_relation[label1_id] = list()

        if label2_name not in parent_child_relation[label1_id]:
            parent_child_relation[label1_id].append(label2_name)

        # 建立二级分类的父级
        child_parent_relation[label2_name] = label1_id

    # # 将二级分类名 存到 一级分类文件下
    for id in parent_child_relation:
        # id = int(id)
        with open(label1_path[id], 'w') as f:
            pass
        with open(label1_path[id], 'a') as f:
            f.write('\t'.join(['label2_id', 'label2_name']) + '\n')
            for i in range(len(parent_child_relation[id])):
                label2_name = parent_child_relation[id][i]
                f.write('\t'.join([str(label_2[label2_name]), label2_name]) + '\n')

    # 将二级分类与一级分类ID对应关系，写入文件
    filename = 'label2-label1_id.txt'
    with open(os.path.join(data_dir, filename), 'w') as f:
        pass
    with open(os.path.join(data_dir, filename), 'a') as f:
        f.write('\t'.join(['label_2', 'label_1']) + '\n')

    for name in child_parent_relation:
        with open(os.path.join(data_dir, filename), 'a') as f:
            f.write('\t'.join([str(label_2[name]), str(child_parent_relation[name])]) + '\n')

    return parent_child_relation, child_parent_relation


if __name__ == '__main__':
    file = os.path.join(data_dir, 'label1_name-label2_name.csv')
    data = read_raw(file)  # type:list

    # 一、二级分类
    # type: dict
    # data: {'行程': 0, '机场服务': 1, '其他': 2,...}
    # 		{'机场--如何查看机场雷达、交通、大屏、地图': 0, '修改中文名': 1, '支付宝登录失败': 2,...}
    label_1 = get_label_1(file)  # 一级分类与id对应关系
    label_2 = get_label_2(file)  # 二级分类与id对应关系

    # 一二级对应关系
    # parent_child_relation
    #   含义：一级分类ID与二级分类ID对应
    #   格式：{19: ['【其他】如何删除行程', '【手添】如何手添误删行程', '【手添】手添成功的行程不显示', '【手添】提示行程已存在',...],11:[...],...}
    # child_parent_relation
    #   含义：二级分类ID与与一级分类ID对应
    # 	格式：{'【其他】如何删除行程': 19, '【手添】如何手添误删行程': 19, '【手添】手添成功的行程不显示': 19, '【手添】提示行程已存在': 19,...}
    parent_child_relation, child_parent_relation = get_label_relation()

    # 答案与一二级对应关系
    text_label1, text_label2 = get_text_label_relation(data)

    # 生成一级、二级分类的train、verify、test set
    train_dev_test(label=1)
    train_dev_test(label=2)
