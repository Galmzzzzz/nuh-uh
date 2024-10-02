let updateBtns = document.getElementsByClassName('update-cart')

for (let i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        let productId = this.dataset.product
        let action = this.dataset.action
        console.log(productId, action)
        console.log(user)

        if(user === 'AnonymousUser'){
            console.log('not logged in')
        }else{
            updateUserOrder(productId, action)  // Передаем action
        }
    })
}

function updateUserOrder(productId, action){  // Добавляем action как параметр
    console.log('sending data')

    let url = '/updateItem/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'productId': productId, 'action': action})  // Используем action здесь
    })
    .then((response) => {
        return response.json()
    })
    .then((data) => {
        console.log(data)
    })
}
