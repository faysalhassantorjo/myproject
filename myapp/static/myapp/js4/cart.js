var updateBtns=document.getElementsByClassName('update-cart')
var sizeSelect = document.getElementById("sizeSelect");

// console.log('size',selectedSize); // Output the selected size to the console

console.log(updateBtns.length)
console.log("hello1")
for( var i=0; i<updateBtns.length; i++){
    updateBtns[i].addEventListener('click',function(){
        var productId=this.dataset.product
        var action=this.dataset.action
        var selectedSize = sizeSelect.value;
        console.log("ProductId: ",productId,"Action: ",action,'size: ',selectedSize)

        console.log("user: ",user)
        if(user=="AnonymousUser"){
                window.location.href = '/login';
        }
        else{
            updateUserOrder(productId,action,selectedSize)
        }
    })
}

function updateUserOrder(productId,action,selectedSize){
    var url='/update_item/'
    console.log('URL:',url)
    fetch(url,{
        method:'POST',
        headers:{
            'Content-Type':"application/json",
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productID':productId,'action':action,'selectedSize':selectedSize})
    })
    .then((response)=>{
        return response.json();
    })
    .then((data)=>{
        console.log('data: ',data);
        location.reload();
    });
}