$(document).ready(function() {

	var original_chart
	var original_porter_chart
	$.ajax({
		url: 'ajax/initial_chart/',  // AJAX 請求的URL
		success: function (data) {
			var value = data[0];
			console.log(value)
			// 渲染第一个图表
			var ctx = document.getElementById('original_chart').getContext('2d');
			let labels = JSON.parse(value['labels']);
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
			let labels_porter = JSON.parse(value['labels_porter']);
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

			$('#product-checkboxes').append(
				'<label class="w-fit"><input type="checkbox" id="all" name="term" value="all" checked> all </label>'
			);
		}
	});

	$('#search').on('keydown', function (event) {
		if (event.key === 'Enter') {
			event.preventDefault();
			var query = $(this).val();  // 獲取輸入的搜尋字串
			if (query) {
				$(this).val('');
			} else {

			}
		}
	});


});

