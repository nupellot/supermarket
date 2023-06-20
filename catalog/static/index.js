// alert("test")

// $("form.pick-container").submit(function() {
// 	$.post(
// 		'http://127.0.0.1:5001/catalog/', // адрес обработчика
// 		this.serialize(), // отправляемые данные
// 		function (response) {
// 			// $('#my_form').hide('slow');
// 			// $('#my_message').html(msg);
// 			// alert(msg.result)
// 			alert(response)
// 		}
// 	);
// 	return false;
// });


// $('form.pick-container').submit(function(e) {
// 	let $form = $(this);
// 	let form = this
// 	// console.log($form.elements)
// 	// console.log(form.elements)
// 	// console.log(this)
// 	// let amountElement = this.elements.amount
// 	// console.log(amountElement)
// 	// let idElement = this.elements.prod_id
// 	// console.log(idElement)
// 	console.log($form)
// 	console.log(form)
// 	// console.log($form.elements)
// 	// console.log($form.serialize())
// 	$.ajax({
// 		type: "POST",
// 		url: "http://127.0.0.1:5001/catalog/",
// 		data: $form.serialize()
// 	}).done(function(response) {
// 		let amountElement = form.elements.amount
// 		let idElement = form.elements.prod_id
// 		console.log($form.serialize())
// 		console.log(form.serialize())
// 		response.forEach(function callback(currentProduct) {
// 			// form.elements.amount.value = currentProduct[]
// 			// console.log("currentProduct" + currentProduct)
// 			console.log(currentProduct["prod_id"] + " " + idElement.value)
// 			// console.log(this.elements)
//
// 			if (currentProduct["prod_id"] == idElement.value) {
// 				console.log("im inside!")
// 				console.log(amountElement.value + " " + currentProduct["amount"])
// 				amountElement.value = currentProduct["amount"]
// 				return
// 			}
// 		});
// 		// amountElement.value = response[]
// 		// console.log(response)
// 		// console.log($form)
// 		// console.log(this.elements)
// 		// console.log(JSON.parse(response))
// 	}).fail(function() {
// 		alert('fail');
// 	});
// 	//отмена действия по умолчанию для кнопки submit
// 	e.preventDefault();
// });


// $("form.pick-container").submit(function() {
// 	$.ajax({
// 	  type: "POST",
// 	  url: 'http://127.0.0.1:5001/catalog/',
// 	  data: this.serialize(),
// 	  success: function(msg) { // получен ответ сервера
// 			// $('#my_form').hide('slow');
// 			// $('#my_message').html(msg);
// 			// alert(msg.result)
// 			alert(msg)
// 		},
// 	  dataType: dataType
// 	});
// }


function changeAmountOfProduct(endpoint) {
	// alert("test")
	console.log(endpoint)
	let id = endpoint.form.elements.prod_id.value
	$.ajax({
		type: "POST",
		url: "http://127.0.0.1:5001/catalog/api/changeAmountOfProduct",
		data: {"prod_id": id, "action": endpoint.name}
	}).done(function(response) {
		console.log(response)
		endpoint.form.elements.amount.value = response["amount"]
	}).fail(function() {
		alert('fail');
	});
}

// $('form.pick-container').submit(function(e) {
// 	let $form = $(this);
// 	let form = this
// 	console.log($form)
// 	console.log(form)
// 	$.ajax({
// 		type: "POST",
// 		url: "http://127.0.0.1:5001/catalog/+",
// 		data: $form.serialize()
// 	}).done(function(response) {
// 		let amountElement = form.elements.amount
// 		let idElement = form.elements.prod_id
// 		console.log($form.serialize())
// 		console.log(form.serialize())
// 		response.forEach(function callback(currentProduct) {
// 			console.log(currentProduct["prod_id"] + " " + idElement.value)
// 			// console.log(this.elements)
//
// 			if (currentProduct["prod_id"] == idElement.value) {
// 				console.log("im inside!")
// 				console.log(amountElement.value + " " + currentProduct["amount"])
// 				amountElement.value = currentProduct["amount"]
// 				return
// 			}
// 		});
// 	}).fail(function() {
// 		alert('fail');
// 	});
// 	//отмена действия по умолчанию для кнопки submit
// 	e.preventDefault();
// });
