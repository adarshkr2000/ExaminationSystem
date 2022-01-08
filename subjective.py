import logging
from typing import Tuple

import nltk as nlp
import numpy as np


class SubjectiveTest:
	"""Class abstraction for subjective test generation module.
	"""

	def __init__(self, rawdata: str):
		"""Class constructor.

		Args:
			filepath (str): Absolute filepath to the subject corpus.
		"""
		self.question_pattern = [
			"Explain in detail ",
			"Define ",
			"Write a short note on ",
			"What do you mean by "
		]

		self.grammar = r"""
			CHUNK: {<NN>+<IN|DT>*<NN>+}
			{<NN>+<IN|DT>*<NNP>+}
			{<NNP>+<NNS>*}
		"""

		self.summary = rawdata
		self.summary=self.summary.replace(".",".\n")

	
	

	

	def generate_test(self, num_questions: int = 2) -> Tuple[list, list]:
		"""Method to generate subjective test.

		Args:
			num_questions (int, optional): Maximum number of questions
				to be generated. Defaults to 2.

		Returns:
			Tuple[list, list]: Generated `Questions` and `Answers` respectively
		"""
		try:
			sentences = nlp.sent_tokenize(self.summary)
		except Exception:
			logging.exception("Sentence tokenization failed.", exc_info=True)

		try:
			cp = nlp.RegexpParser(self.grammar)
		except Exception:
			logging.exception("Regex grammar train failed.", exc_info=True)

		question_answer_dict = dict()
		for sentence in sentences:

			try:
				tagged_words = nlp.pos_tag(nlp.word_tokenize(sentence))
			except Exception:
				logging.exception("Word tokenization failed.", exc_info=True)

			tree = cp.parse(tagged_words)
			for subtree in tree.subtrees():
				if subtree.label() == "CHUNK":
					temp = ""
					for sub in subtree:
						temp += sub[0]
						temp += " "
					temp = temp.strip()
					temp = temp.upper()
					if temp not in question_answer_dict:
						if len(nlp.word_tokenize(sentence)) > 20:
							question_answer_dict[temp] = sentence
					else:
						question_answer_dict[temp] += sentence

		keyword_list = list(question_answer_dict.keys())
		question_answer = list()

		for _ in range(3):
			rand_num = np.random.randint(0, len(keyword_list))
			selected_key = keyword_list[rand_num]
			answer = question_answer_dict[selected_key]
			rand_num %= 4
			question = self.question_pattern[rand_num] + selected_key + "."
			question_answer.append({"Question": question, "Answer": answer})

		que = list()
		ans = list()
		while len(que) < num_questions:
			rand_num = np.random.randint(0, len(question_answer))
			if question_answer[rand_num]["Question"] not in que:
				que.append(question_answer[rand_num]["Question"])
				ans.append(question_answer[rand_num]["Answer"])
			else:
				continue
		return que, ans

	
