"""Convert BIS pos tagged sentences in files into SSF format."""
from argparse import ArgumentParser
import os


def read_lines_from_file(file_path):
	"""Read lines from a file using its file path."""
	with open(file_path, 'r', encoding='utf-8') as file_read:
		return [line.strip() for line in file_read.readlines() if line.strip()]


def write_lines_to_file(lines, file_path):
	"""Write lines to a file."""
	with open(file_path, 'w', encoding='utf-8') as file_write:
		file_write.write('\n'.join(lines))


def convert_pos_tagged_sentences_into_ssf_sentences(sentences, syms, puncs, sep='_'):
	"""Convert raw sentences into sentences in SSF format."""
	ssf_sentences = []
	initial_header = "<Sentence id='"
	footer = "</Sentence>"
	# Set sentence counter
	sentence_cntr = 1
	for sentence in sentences:
		temp_sentence = []
		header = initial_header + str(sentence_cntr) + "'>"
		sentence_cntr += 1
		# Set token counter
		token_cntr = 1
		token_pos_list = [item.strip() for item in sentence.split() if item.strip()]
		for token_pos in token_pos_list:
			token, pos = token_pos.split(sep, 1)
			if token in syms:
				pos = 'RD_SYM'
			elif token in puncs:
				pos = 'RD_PUNC'
			elif pos == 'unk':
				pos = 'RD_UNK'
			temp_sentence.append('\t'.join([str(token_cntr), token, pos]))
			token_cntr += 1
		ssf_tokens = [header] + temp_sentence + [footer]
		ssf_sentence = '\n'.join(ssf_tokens) + '\n'
		ssf_sentences.append(ssf_sentence)
	return ssf_sentences


def convert_sentences_to_ssf_in_files_and_write_to_files(input_folder_path, output_folder_path, syms, puncs, sep='_'):
	"""Tokenize input files, convert into SSF and write to files."""
	for root, dirs, files in os.walk(input_folder_path):
		for fl in files:
			input_path = os.path.join(root, fl)
			input_sentences = read_lines_from_file(input_path)
			ssf_sentences = convert_pos_tagged_sentences_into_ssf_sentences(input_sentences, syms, puncs, sep)
			output_path = os.path.join(output_folder_path, fl)
			write_lines_to_file(ssf_sentences, output_path)


def main():
	"""Pass arguments and call functions here."""
	parser = ArgumentParser(description='This is a program to convert pos tagged sentences in non ssf into ssf format')
	parser.add_argument('--input', dest='inp', help='Enter the input folder path')
	parser.add_argument('--output', dest='out', help='Enter the output folder path')
	parser.add_argument('--sep', dest='sep', help='Enter the separator between token and pos tag', default='_')
	args = parser.parse_args()
	syms = read_lines_from_file('RD_SYM.txt')
	puncs = read_lines_from_file('RD_PUNC.txt')
	if not os.path.isdir(args.inp):
		input_sentences = read_lines_from_file(args.inp)
		ssf_sentences = convert_pos_tagged_sentences_into_ssf_sentences(input_sentences, syms, puncs, args.sep)
		write_lines_to_file(ssf_sentences, args.out)
	else:
		input_folder_path = args.inp
		output_folder_path = args.out
		if not os.path.isdir(output_folder_path):
			os.makedirs(output_folder_path)
		convert_sentences_to_ssf_in_files_and_write_to_files(input_folder_path, output_folder_path, syms, puncs, args.sep)


if __name__ == '__main__':
	main()

