from openpyxl import load_workbook
from openpyxl import Workbook
import matplotlib.pyplot as plt
import numpy as np

def get_genome():
	file = open("/Users/anna/Desktop/bioinf/genome_e_coli.fna", 'r')
	rare_genom = file.read()
	genome = rare_genom.replace('>NC_000913.3 Escherichia coli str. K-12 substr. MG1655, complete genome', '')
	genome = genome.replace('\n', '')
	genome = genome.replace(' ', '')

	return genome

def accept_start(codone):

	start_codone = ["ATG"]
	if codone in start_codone: return True
	else: return False

def accept_stop(codone):

	stop_codones = ["TAA", "TAG", "TGA"]
	if codone in stop_codones: return True
	else: return False

def get_second_line(dna):

	complim = {'A':'T', 'G': 'C', 'T':'A', 'C':'G'}
	new_line = ''
	for i in range(1, len(dna)):
		new_line += complim.get(dna[i])
	new_line = new_line[::-1]
	return new_line

def translate(genome):

	start_codones = []
	stop_codones = []
	flag = False

	for i in range(0, len(genome), 3):
		if not flag:
			if accept_start(genome[i:i+3]):
				start_codones.append(i)
				flag = True
		else:
			if accept_stop(genome[i:i+3]):
				stop_codones.append(i)
				flag = False

	if flag: start_codones.pop(-1)
	return start_codones, stop_codones

def result_to_file(result_list_starts, result_list_stops):

	wb = Workbook()
	filename = 'prak.xlsx'
	worksheet = wb.active
	worksheet.title = 'Table 1'
	titles = [['start1'], ['start2'], ['start3'], ['start4'], ['start5'], ['start6'],
				['stop1'],['stop2'],['stop3'],['stop4'],['stop5'],['stop6']]

	for i in range(len(result_list_starts)):
		worksheet.append(titles[i]+result_list_starts[i])
		worksheet.append(titles[i+6]+result_list_stops[i])

	wb.save(filename = filename)

def bar_chart(result_list_starts, result_list_stops):
	length = {}
	dif = 0
	for i in range(len(result_list_starts)):
		for j in range(len(result_list_starts[i])):
			dif = result_list_stops[i][j] - result_list_starts[i][j]
			if dif in length.keys():
				length[dif] += 1
			else:
				length[dif] = 1
	length = dict(sorted(length.items(), key=lambda item: item[0]))

	plt.bar(range(len(length)), list(length.values()), align='center')
	plt.xticks(range(len(length)), list(length.keys()))

	plt.show()

	return length

def main():

	genome = get_genome()
	list_of_start_codones = []
	list_of_stop_codones = []
	second_line = get_second_line(genome)

	for i in range(3):
		a, b = translate(genome[i::])
		list_of_start_codones.append(a)
		list_of_stop_codones.append(b)

	for i in range(3):
		a,b = translate(second_line[i::])
		list_of_start_codones.append(a)
		list_of_stop_codones.append(b)

	print(bar_chart(list_of_start_codones, list_of_stop_codones))

	#sum_of_starts = 0
	#sum_of_stops = 0
		
	""""for i in range(len(list_of_stop_codones)):
						sum_of_starts += len(list_of_start_codones[i])
						sum_of_stops += len(list_of_stop_codones[i])
					result_to_file(list_of_start_codones, list_of_stop_codones)"""

if __name__=='__main__':
	main()
