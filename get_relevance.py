import json
from collections import defaultdict


def main():
	"""计算相关性，支持大规模数据运算
	"""
	with open('./data/example.json', 'r', encoding='utf-8') as f1:
		with open('./data/new_example.json', 'w', encoding='utf-8') as f2:
			# 分别计算每个实体出现的次数，每个实体对于总体出现的概率
			num_di = defaultdict(int)
			f_li = []
			for ind, i in enumerate(f1):
				# if ind > 10000:
				# 	break
				print('\r第一轮循环： %s' % ind, end='')
				line_li = json.loads(i)
				f_li.append(line_li)
				for j in line_li:
					num_di[j] += 1
			num_di = dict(num_di)
			print()
			print(num_di)
			total_num = sum(num_di.values())
			print(total_num)
			percent_di = {a: b / total_num for a, b in num_di.items()}
			print(percent_di)

			# 计算用户集合Cx购买y的期望用户数Exy
			# 计算同时购买了x与y的用户数Nxy
			Exy_di = defaultdict(dict)
			Nxy_di = defaultdict(dict)
			for ind2, one_li in enumerate(f_li):
				print('\r第二轮循环： %s/%s' % (ind2, f_li.__len__()), end='')
				for x in one_li:
					for y in one_li:
						if x == y:
							continue
						else:
							Cxy = 1 - (1 - percent_di[y]) ** (len(one_li) - 1)
							try:
								Exy_di[x][y] += Cxy
							except:
								Exy_di[x][y] = Cxy
							try:
								Nxy_di[x][y] += 1
							except:
								Nxy_di[x][y] = 1

			# 计算两个实体之间的相关度Rxy
			sort_di = defaultdict(dict)
			l = num_di.keys().__len__()
			print()
			for ind3, x in enumerate(num_di.keys()):
				print('\r第三轮循环： %s/%s' % (ind3, l), end='')
				for y in num_di.keys():
					if x == y:
						continue
					else:
						try:
							Exy = Exy_di[x][y]
							Nxy = Nxy_di[x][y]
							if Nxy and Exy:
								# print(Exy, Nxy)

								# 计算x, y的相关度
								Rxy = (Nxy - Exy) / (Exy ** 0.5)
								sort_di[x][y] = round(Rxy, 2)
						except:
							continue
			print("\n计算完毕")

			# 归一化，可以不进行归一化，直接输出
			new_sort_di = defaultdict(dict)
			n = 0
			for e, f in sort_di.items():
				print('\r第四轮循环： %s/%s' % (n, l), end='')
				n += 1
				for g, h in f.items():
					new_sort_di[e][g] = round(h / max(f.values()), 3)
			f2.write(json.dumps(new_sort_di, ensure_ascii=False))


def get_show():
	"""展示每个商品对应旗下的相关性列表排序
	"""
	with open('./data/new_example.json', 'r', encoding='utf-8') as f:
		di = json.loads(f.read())
		print()
		for key, new_di in di.items():
			new_di = sorted(new_di.items(), key=lambda x: x[1], reverse=True)
			print(key, new_di)


if __name__ == '__main__':
	main()
	get_show()
