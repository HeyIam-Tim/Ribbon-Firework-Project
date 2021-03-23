console.log('hello')

let cartBtns = document.querySelectorAll('.cart-btn')

for (i=0; i<cartBtns.length; i++) {
    cartBtns[i].addEventListener('click', function(){
        console.log('click click')
        let ribbonId = this.dataset.ribbonid
        console.log('ADD ITEM: ', ribbonId)
    })
}

let updateCart = (ribbonId) => {
    let url = "{% url 'index' %}"
    fetch(url, {
        method:'POST',
        headers:{
            'Context-type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'ribbonId':ribbonId})
    })
    .then(res => res.json())
    .then(data => {
        console.log('DATA: ', data)
    })
}