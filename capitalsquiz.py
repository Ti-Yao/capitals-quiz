#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random
import pandas as pd
from Levenshtein import distance as levenshtein_distance
import re


def print_list(printlist):
	for number, letter in enumerate(printlist):
		print(number + 1, letter)


df = pd.read_csv('capital.csv').set_index('Continent')

continents = df.index.unique().tolist()
shuffle = 'N'
print_list(continents)

continent_index = input('\n')
if ',' in continent_index:
	continent_index = continent_index.split(',')
	continent_index = list(map(int, continent_index))
	continent_index  = [x - 1 for x in continent_index ]
	continent = [continents[i] for i in continent_index]
else:
	continent = continents[int(continent_index)-1]

multi = input('Multiple Choice (Y/N)\t').upper()
print('\n')

if multi == 'Y' or multi == 'N':
	N = input('N questions\t')
	print('\n')
	shuffle = input('Shuffle (Y/N)\t').upper()
	print('\n')
else:
	N = 'all'
	start = int(input('start\t'))
	print('\n')
	end = int(input('end\t'))
	print('\n')


continent_df = df.loc[continent]

flip = input('Flip (Y/N)\t').upper()
if flip == 'Y':
	pairs = dict(zip(continent_df.Capital, continent_df.Country))
else:
	pairs = dict(zip(continent_df.Country, continent_df.Capital))

N = int(N) if N.isnumeric() else len(continent_df.Country.tolist())


if shuffle == 'Y':
	countries = random.sample(continent_df.Country.tolist(),N)
else:
	countries = continent_df.Country.tolist()

def result(score, errors,country, answer):
	if levenshtein_distance(answer.lower(), re.sub(r'[^\w\s]','',pairs[country].lower().replace('saint','st').replace("'",''))) <=3:
		score += 1
		response = 'Correct\n'
		if levenshtein_distance(answer.lower(), pairs[country].lower()) >0:
			response = response.replace('\n',  f'  ({pairs[country]})\n' )
		print(response)
	else:
		print(pairs[country],'\n')
		errors.append((country,answer))
	return score,errors

def create_choice(country, n = 10):
	current_continent = continent_df.loc[continent_df['Country'] == country].index.values[0]
	continent_countries = continent_df.loc[current_continent].Capital.tolist()
	continent_countries.remove(pairs[country])
	answers = [pairs[country]] + random.sample(continent_countries, n - 1)
	random.shuffle(answers)
	print_list(answers)
	return answers

def print_errors(errors):
	print('\n********* Mistakes ********* ')
	for error in errors:
		print(f'Country: {error[0]}\nYour Guess: {error[1]}\nCorrect Answer: {pairs[error[0]]}\n')
	print('**************************** ')

def run_quiz_multi(countries):
	score = 0
	errors = []
	for i, country in enumerate(countries):
		answers = create_choice(country)
		choice = int(input(f'\n{country}\t'))
		answer = answers[choice-1]
		score,errors = result(score,errors, country, answer)
		print(f'{score}/{i+ 1} ({N})\n')

	print_errors(errors)
	print("you got", score, "out of", len(countries))


def run_quiz(countries):
	errors = []
	score = 0
	for i, country in enumerate(countries):
		answer = input(f'\n{country}\t')
		score,errors = result(score,errors, country, answer)
		print(f'{score}/{i+1} ({N})\n')
	print_errors(errors)
	print("you got", score, "out of", len(countries))

def learn(countries):
	countries = countries[start:end]
	for i, country in enumerate(countries):
		answer = input(f'\n{country}\t')
		result(0,[], country, answer)
		# print(f'{i + 1}/{N}\n')

if multi == 'Y':
	run_quiz_multi(countries)
elif multi == 'N':
	run_quiz(countries)
else:
	learn(countries)
