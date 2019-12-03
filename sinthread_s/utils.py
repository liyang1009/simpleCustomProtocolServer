def merge_prefix(deque,loc):
	'''from the byte stream pool get specify length dataset '''
	if len(deque) > 0:
		sum_data_index = 0
		need_data = []
		item_index = 0 
		data_index = 0
		for item in deque:
			sum_data_index += len(item)
			item_index += 1
			if sum_data_index >= loc:
				break	
		for i in range(item_index):
			need_data.append(deque.popleft())
		
		remind_length = loc - sum_data_index  
		if remind_length !=0:
			last_element = need_data[item_index - 1]
			new_remind_data = last_element[:remind_length]
			new_header = last_element[remind_length:]
			deque.appendleft(new_header)
			need_data[item_index-1] = new_remind_data
			print(need_data)
		return  "".join(need_data)	


