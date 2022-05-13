let btnUp = document.querySelectorAll('.js-btn-up');
    let inputQTY = document.querySelectorAll('.js-input-qty');
    for (i=0; i < btnUp.length; i++) {
        btnUp[i].addEventListener("click", (event) => {
        event.preventDefault();
        let targetBtn = event.target;
        if (event.target.tagName == 'svg') {
            targetBtn = event.target.parentNode;
            console.log('1')
        } else if (event.target.tagName == 'path') {
            targetBtn = event.target.parentNode.parentNode;
        }
        console.log(targetBtn.nextSibling.nextSibling);
        targetBtn.nextSibling.nextSibling.value = Number(targetBtn.nextSibling.nextSibling.value) + 1;
        
    });
    }

    let btnDown = document.querySelectorAll('.js-btn-down');
    for (i=0; i < btnUp.length; i++) {
        btnDown[i].addEventListener("click", (event) => {
        event.preventDefault();
        let targetBtn = event.target;
        if (event.target.tagName == 'svg') {
            targetBtn = event.target.parentNode;
            console.log('1')
        } else if (event.target.tagName == 'path') {
            console.log('3')
            targetBtn = event.target.parentNode.parentNode;
        }
        console.log(targetBtn.nextSibling.nextSibling);
        if(Number(targetBtn.previousSibling.previousSibling.value) > 1) {
            targetBtn.previousSibling.previousSibling.value = Number(targetBtn.previousSibling.previousSibling.value) - 1;
        } else {
            targetBtn.previousSibling.previousSibling.value = 1;
        }
        
        
    });
    }

const order_form = document.getElementById("form-order");
let first_name = document.getElementById("id_first_name");
let last_name = document.getElementById("id_last_name");
let surname = document.getElementById("id_surname");
let email = document.getElementById("email");
let phone = document.getElementById("id_phone");
let region = document.getElementById("id_state");
let city = document.getElementById("id_city");
let street = document.getElementById("id_street");
let house = document.getElementById("id_house");
let flat = document.getElementById("id_flat");


function isItemExist(name) {
  return (name in localStorage)
}

first_name.value = (isItemExist('first_name')) ? localStorage.first_name : ''
last_name.value = (isItemExist('last_name')) ? localStorage.last_name : ''
surname.value = (isItemExist('surname')) ? localStorage.surname : ''
email.value = (isItemExist('email')) ? localStorage.email : email.value
phone.value = (isItemExist('phone')) ? localStorage.phone : ''
region.value = (isItemExist('region')) ? localStorage.region : ''
city.value = (isItemExist('city')) ? localStorage.city : ''
street.value = (isItemExist('street')) ? localStorage.street : ''
house.value = (isItemExist('house')) ? localStorage.house : ''
flat.value = (isItemExist('flat')) ? localStorage.flat : ''

order_form.addEventListener('submit', () => {
  localStorage.first_name = first_name.value
  localStorage.last_name = last_name.value
  localStorage.surname = surname.value
  localStorage.email = email.value
  localStorage.phone = phone.value
  localStorage.region = region.value
  localStorage.city = city.value
  localStorage.street = street.value
  localStorage.house = house.value
  localStorage.flat = flat.value
})