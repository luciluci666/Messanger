

let url = 'http://127.0.0.1:8000/user/contact/message/'

function loadCart(){
    fetch('http://127.0.0.1:8000/user/contact/message?contact_id=1&token=6fc8fc2e-93c6-486f-a86d-b7addf3f4d3f').then(
       response => {
          return response.text();
       }
    ).then(
       text => {
        console.log(text);
       }
    );
 }
loadCart()