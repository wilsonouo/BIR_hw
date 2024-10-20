$(document).ready(function() {

	var original_chart
	var original_porter_chart
	var labels
	var labels_porter
	$.ajax({
		url: 'ajax/initial_chart/',  // AJAX 請求的URL
		success: function (data) {
			var value = data[0];
			// 渲染第一个图表
			var ctx = document.getElementById('original_chart').getContext('2d');
			labels = Array.from({ length: value['data'].length }, (_, i) => i + 1);
			original_chart = new Chart(ctx, {
				type: 'line',
				data: {
					labels: labels,
					datasets: [{
						label: 'all',
						data: value['data'],
						borderColor: 'rgba(75, 192, 192, 1)',
						borderWidth: 2
					}]
				},
				options: {
					responsive: false,
					scales: {
						y: {
							beginAtZero: true
						}
					}
				}
			});
			
			// chart porter
			var ctx_porter = document.getElementById('original_porter_chart').getContext('2d');
			labels_porter = Array.from({ length: value['data_porter'].length }, (_, i) => i + 1);
			original_porter_chart = new Chart(ctx_porter, {
				type: 'line',
				data: {
					labels: labels_porter,
					datasets: [{
						label: 'all',
						data: value['data_porter'],
						borderColor: 'rgba(75, 192, 192, 1)',
						borderWidth: 2
					}]
				},
				options: {
					responsive: false,
					scales: {
						y: {
							beginAtZero: true
						}
					}
				}
			});

			// show the table
			var table = '<h2>all</h2><div class="w-56 h-40 border-gray-300 border-2 flex flex-col overflow-y-auto overflow-x-hidden"><table class="w-64 divide-y divide-gray-200"><thead class="bg-gray-50"><tr><th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">rank</th><th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">word</th></tr>';
			var label_value = Object.values(JSON.parse(value['labels']));
			for(var i = 0; i < label_value.length; i++){
				table = table.concat(
					'<tbody class="bg-white divide-y divide-gray-200"><tr><td class="px-6 py-4 whitespace-nowrap">' + (i+1) + '</td><td class="px-6 py-4 whitespace-nowrap">' + label_value[i] + '</td></tr></tbody>'
				);
			};
			table = table.concat('</thead></table></div>');
			$('#rank').append(table);


			var porter_table = '<h2>all</h2><div class="w-56 h-40 border-gray-300 border-2 flex flex-col overflow-y-auto"><table class="min-w-full divide-y divide-gray-200"><thead class="bg-gray-50"><tr><th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">rank</th><th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">word</th></tr>';
			var label_porter_value = Object.values(JSON.parse(value['labels_porter']));
			for(var i = 0; i < label_porter_value.length; i++){
				porter_table = porter_table.concat(
					'<tbody class="bg-white divide-y divide-gray-200"><tr><td class="px-6 py-4 whitespace-nowrap">' + (i+1) + '</td><td class="px-6 py-4 whitespace-nowrap">' + label_porter_value[i] + '</td></tr></tbody>'
				);
			};
			porter_table = porter_table.concat('</thead></table></div>');
			$('#porter_rank').append(porter_table);




		}
	});

	$('#search').on('keydown', function (event) {
		if (event.key === 'Enter') {
			event.preventDefault();
			var query = $(this).val();  // 獲取輸入的搜尋字串
			if (query) {
				const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
				$.ajax({
					url: 'ajax/add_chart/',  // AJAX 請求的URL
					method: 'POST',
					data: {
						term: query,
						'csrfmiddlewaretoken': csrftoken
					},
					success: function (response) {
						var value = response[0];
						// 添加新的數據集到現有的 datasets 中
						var r = Math.floor(Math.random() * 256);
						var g = Math.floor(Math.random() * 256);
						var b = Math.floor(Math.random() * 256);
						var line_color = 'rgba(' + r + ', ' + g + ', ' + b + ', 1)';
						newDataset = {
							label: query,
							data: value['data'],
							borderColor: line_color,
							borderWidth: 2
						};
						original_chart.data.datasets.push(newDataset);
						// 重新繪製圖表
						original_chart.update();

						// show the table
						var table = '<h2 class="mt-2">' + query + '</h2><div class="w-56 h-40 border-gray-300 border-2 flex flex-col overflow-y-auto overflow-x-hidden"><table class="w-64 divide-y divide-gray-200"><thead class="bg-gray-50"><tr><th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">rank</th><th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">word</th></tr>';
						var label_value = Object.values(JSON.parse(value['labels']));
						for(var i = 0; i < label_value.length; i++){
							table = table.concat(
								'<tbody class="bg-white divide-y divide-gray-200"><tr><td class="px-6 py-4 whitespace-nowrap">' + (i+1) + '</td><td class="px-6 py-4 whitespace-nowrap">' + label_value[i] + '</td></tr></tbody>'
							);
						};
						table = table.concat('</thead></table></div>');
						$('#rank').append(table);

						var data_porter = value['data_porter'];
						newDataset_porter = {
							label: query,
							data: data_porter,
							borderColor: line_color,
							borderWidth: 2
						};
						original_porter_chart.data.datasets.push(newDataset_porter);
						original_porter_chart.update();

						// show the table
						var porter_table = '<h2 class="mt-2">' + query + '</h2><div class="w-56 h-40 border-gray-300 border-2 flex flex-col overflow-y-auto"><table class="min-w-full divide-y divide-gray-200"><thead class="bg-gray-50"><tr><th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">rank</th><th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">word</th></tr>';
						var label_porter_value = Object.values(JSON.parse(value['labels_porter']));
						for(var i = 0; i < label_porter_value.length; i++){
							porter_table = porter_table.concat(
								'<tbody class="bg-white divide-y divide-gray-200"><tr><td class="px-6 py-4 whitespace-nowrap">' + (i+1) + '</td><td class="px-6 py-4 whitespace-nowrap">' + label_porter_value[i] + '</td></tr></tbody>'
							);
						};
						porter_table = porter_table.concat('</thead></table></div>');
						$('#porter_rank').append(porter_table);
						
					}
				})

			}
			$(this).val('');

			



		}
	});

});

