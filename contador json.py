import os
# '#designativista_eleicoes', '#mariellepresente_eleicoes', '#elenao_eleicoes']:
for hashtag_label in ['#elenao']:
	for folder in ['F', 'TD', 'ID', 'IM']:
		counter = 0
		try:
			files = os.listdir('./' + hashtag_label + '/' + folder)
			for file in files:
				if file.endswith('.json'):
					counter += 1
		except:
			pass
		print('Hashtag: ' + str(hashtag_label) + '. Classification: ' + str(folder) + '. Number of posts = ' + str(counter))
	for folder in ['F', 'TD', 'ID', 'IM']:
		counter = 0
		try:
			files = os.listdir('./' + hashtag_label + '/29-09/' + folder)
			for file in files:
				if file.endswith('.json'):
					counter += 1
		except:
			pass
		print('Hashtag: ' + str(hashtag_label) + '. Classification: ' + str(folder) + '. Number of posts = ' + str(counter) + ' 29-09')

