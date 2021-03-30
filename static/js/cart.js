var updateBtns = document.getElementsByClassName('update-cart');
console.log("*************** Here 1")
for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		console.log("*************** Here 3")
		var productId = this.dataset.product;
		var action = this.dataset.action;
		var quantity = 0;
		if (this.dataset.quantity == 0){
			quantity = document.getElementById('quantity').value;
			console.log("Hey, I'm Here");
			console.log(quantity);
		}
		else{
			quantity = this.dataset.quantity;
			console.log("Oh, I have quantity")
		}
		console.log('productId:', productId, 'Action:', action);
		console.log('USER:', user);

		if (user == 'AnonymousUser'){
			addCookieItem(productId, action, quantity);
			//console.log('No Log')
		}else{
			updateUserOrder(productId, action, quantity);
		}
	})
}
console.log("*************** Here 2")
function updateUserOrder(productId, action, quantity){
	console.log('User is authenticated, sending data...')

		var url = '/update_item/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'productId':productId, 'action':action, 'quantity':quantity})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    location.reload()
		});
}

function addCookieItem(productId, action, quantity){
	console.log('User is not authenticated...!')

	if (action == 'add'){
		if (cart[productId] == undefined){
		cart[productId] = {'quantity':quantity}

		}else{
			cart[productId]['quantity'] += quantity
		}
	}

	if (action == 'remove'){
		cart[productId]['quantity'] -= 1

		if (cart[productId]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[productId];
		}
	}
	console.log('CART:', cart)
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
	
	location.reload()

}