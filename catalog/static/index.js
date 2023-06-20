// alert("test")
// $(".logo-container").remove();

// function decrementAmountOfProduct() {
//     let xhr = new XMLHttpRequest()
//
//     xhr.open("POST", "", true)
//
//     xhr.onload = function() {
//         if (xhr.status == 200) {
//             alert(this.response)
//         }
//     }
//
//     xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
//     let body = 'name=' + encodeURIComponent(name) +
//   '&surname=' + encodeURIComponent(surname);
//     xhr.send(body)
// }\

$("form.pick-container").submit(function() {
	$.post(
		'http://127.0.0.1:5001/catalog/', // адрес обработчика
		 $("form.pick-container").serialize(), // отправляемые данные

		function(msg) { // получен ответ сервера
			// $('#my_form').hide('slow');
			// $('#my_message').html(msg);
			// alert(msg.result)
			alert(msg)
		}
	);
	return false;
});

