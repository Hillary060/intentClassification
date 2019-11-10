import random
import os

def read_raw(file_name):
	data = []
	line_num = 0
	with open(file_name) as f:
		for line_ in f:
			line_num += 1
			if line_num>1:
				data.append(line_.strip().split('\t'))
	return data

def process(data, data_dir):
	str_header = 'label' + '\t' + 'content' + '\n'
	label_dict = dict()
	with open(os.path.join(data_dir, 'class.tsv'), 'w') as f:
		pass

	label_index = 0
	with open(os.path.join(data_dir, 'class.tsv'), 'a') as f:
		f.write(str_header)
		for item in data:
			if item[0] not in label_dict:
				label_dict[item[0]] = label_index
				f.write(str(label_index)+ '\t' + item[0] +'\n')
				label_index += 1

	random.shuffle(data)
	dev_idx = int(len(data)*0.7)
	test_idx = int(len(data)*0.85)

	with open(os.path.join(data_dir, 'train.tsv'), 'w') as f:
		pass	
	with open(os.path.join(data_dir, 'dev.tsv'), 'w') as f:
		pass		
	with open(os.path.join(data_dir, 'test.tsv'), 'w') as f:
		pass

	train_file = open(os.path.join(data_dir, 'train.tsv'), 'a')
	train_file.write(str_header)
	dev_file = open(os.path.join(data_dir, 'dev.tsv'), 'a')
	dev_file.write(str_header)
	test_file = open(os.path.join(data_dir, 'test.tsv'), 'a')
	test_file.write(str_header)

	for i in range(len(data)):
		if i<=dev_idx:
			train_file.write('\t'.join([str(label_dict[data[i][0]]),data[i][1]])+'\n')
		elif i>dev_idx and i<=test_idx:
			dev_file.write('\t'.join([str(label_dict[data[i][0]]),data[i][1]])+'\n')
		else:
			test_file.write('\t'.join([str(label_dict[data[i][0]]),data[i][1]])+'\n')

def static(data, data_dir):
	label_count = dict()

	for item in data:
		if item[0] not in label_count:
			label_count[item[0]] = 0
		label_count[item[0]] += 1
	all_count = sum([label_count[x] for x in label_count])

	label_count = sorted(label_count.items(), key=lambda x: x[1], reverse=True)

	print(label_count)
	with open(os.path.join(data_dir, 'static.tsv'), 'w') as f:
		pass
	with open(os.path.join(data_dir, 'static.tsv'), 'a') as f:
		for x in range(len(label_count)):
			f.write('\t'.join([label_count[x][0], str(label_count[x][1]), str(label_count[x][1]/float(all_count))])+'\n')
	print(len(label_count))




if __name__=='__main__':
	data_dir = 'intent/data'
	data = read_raw(os.path.join(data_dir, 'samples10000.txt'))
	static(data, data_dir)
	process(data, data_dir)