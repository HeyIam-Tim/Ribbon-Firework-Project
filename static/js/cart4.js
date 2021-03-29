console.log('hello')

let cartBtns = document.querySelectorAll('.cart-btn')

for (i=0; i<cartBtns.length; i++) {
    cartBtns[i].addEventListener('click', function(){
        console.log('click click')
        let ribbonId = this.dataset.ribbonid
        console.log('ADD ITEM: ', ribbonId)
        updateCart(ribbonId)
    })
}

let updateCart = (ribbonId) => {
    // get csrf token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    let url = "/ribbon-api/"
    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body: JSON.stringify({'ribbonId': ribbonId})
    })
    .then(res => res.json())
    .then(data => {
        console.log('DATA: ', data)
        document.querySelector('#cart-quantity').innerHTML = data.item_quantity
    })
}