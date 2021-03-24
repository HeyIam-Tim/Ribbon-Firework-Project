console.log('hello')
// let user = '{{request.user}}'
// console.log('hello', user)

let getRibbons = () => {

    let url = "/api/" 
    // let url = "http://127.0.0.1:8000/api/"
    fetch(url, {
        // method:'GET',
        headers:{
            'Context-type':'application/json',
        },
    })
    .then(Response => Response.json())
    .then(data => {
        console.log('DATA: ', data)
        let grid = document.querySelector('.grid')
        let grid_area = '';
        for (i=0; i<data.length; i++) {
            let cart = `
                <div class="card">
                    <a href="/ribbon-create/${data[i].id}/"><img src="/static/${data[i].image}/" alt="ribbonimg"></a>
                    <div class="options flex fd-col">
                        <p>${data[i].ribbon_name}</p>
                        <div class="flex jc-sb actions">
                            <div class="cta">
                                <a href="/ribbon-create/${data[i].id}/"><button>Купить</button></a>
                                ${user.is_authenticated ?
                                    `<button data-ribbonid="${data[i].id}" class="cart cart-btn">Корзина</button>`:'<button data-ribbonid="${data[i].id}" class="cart cart-btn">Корзина</button>'
                                }
                            </div>
                            <h3>${data[i].price} p</h3>
                        </div>
                    </div>
                </div>
            `
            grid_area += cart
        }
        grid.innerHTML = grid_area
        // grid.innerHTML = `
        // {% for ribbon in ${data} %}
        //     <div class="card">
        //         <a href="/ribbon-create/"><img src="{{ribbon.image.url}}" alt=""></a>
        //         <div class="options flex fd-col">
        //             <p>{{ribbon.ribbon_name}}</p>
        //             <div class="flex jc-sb actions">
        //                 <div class="cta">
        //                     <a href="{% url 'ribbon-create' ribbon.id %}"><button>Купить</button></a>
        //                     {% if request.user.is_authenticated %}
        //                     <button data-ribbonid="{{ribbon.id}}" class="cart cart-btn">Корзина</button>
        //                     {% endif %}
        //                 </div>
        //                 <h3>{{ribbon.price}} p</h3>
        //             </div>
        //         </div>
        //     </div>
        // {% endfor %}
        // `
    });
}

getRibbons()

// let cartBtns = document.querySelectorAll('.cart-btn')

// for (i=0; i<cartBtns.length; i++) {
//     cartBtns[i].addEventListener('click', function(){
//         console.log('click click')
//         let ribbonId = this.dataset.ribbonid
//         console.log('ADD ITEM: ', ribbonId)
//         updateCart(ribbonId)
//     })
// }

// let updateCart = (ribbonId) => {
//     // get csrf token
//     function getCookie(name) {
//         let cookieValue = null;
//         if (document.cookie && document.cookie !== '') {
//             const cookies = document.cookie.split(';');
//             for (let i = 0; i < cookies.length; i++) {
//                 const cookie = cookies[i].trim();
//                 // Does this cookie string begin with the name we want?
//                 if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                     cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                     break;
//                 }
//             }
//         }
//         return cookieValue;
//     }
//     const csrftoken = getCookie('csrftoken');

//     let url = "{% url 'index' %}"
//     fetch(url, {
//         method:'POST',
//         headers:{
//             'Context-type':'application/json',
//             'X-CSRFToken':csrftoken,
//         },
//         body:JSON.stringify({'ribbonId':ribbonId})
//     })
//     .then(res => res.json())
//     .then(data => {
//         console.log('DATA: ', data)
//     })
// }