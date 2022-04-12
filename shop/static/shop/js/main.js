const navUser = document.querySelectorAll('.user-menu');
const UserToggle = document.querySelectorAll('.user-menu__toggle');

const navMain = document.querySelector('.nav');
const navToggle = document.querySelector('.nav__toggle');

navMain.classList.remove('nav--nojs');

const activeMenu = document.querySelectorAll('.nav__item--active');

if (activeMenu[1]) {
  activeMenu[0].classList.remove('nav__item--active')
}

if (navUser != null) {
  navUser.forEach(function(item) {
    item.classList.remove('user-menu--nojs');
  });
}

function toggleClass(parent, classA, classB) {
  document.addEventListener('click', function (event) {
    if (event.target.dataset.toggle != undefined) {
      let currentNav = event.target.closest(parent);
      
      if (currentNav.classList.contains(classA)) {
        currentNav.classList.remove(classA);
        currentNav.classList.add(classB);
      } else {
        currentNav.classList.add(classA);
        currentNav.classList.remove(classB);
      }
    }
  });
}

toggleClass('nav', 'user-menu--closed', 'user-menu--opened');
toggleClass('nav', 'nav--closed', 'nav--opened');

const navContainer = document.querySelector('.nav-container');
const header = document.querySelector('.header');

if(window.matchMedia('(max-width: 767px)').matches) {
  window.onscroll = function () {
    if (window.pageYOffset > 495) {
      navContainer.classList.add('nav-container--fixed');
      header.style = 'padding-top: 52px';
    } else {
      header.style = '';
      navContainer.classList.remove('nav-container--fixed');
      }
  }
}

const order_form = document.getElementById("form-order");
let first_name = document.getElementById("id_first_name");
let last_name = document.getElementById("id_last_name");
let surname = document.getElementById("id_surname");
let email = document.getElementById("email");
let phone = document.getElementById("id_phone");
let adress = document.getElementById("id_adress");

const input = order_form.querySelectorAll("input");

function isItemExist(name) {
  return (name in localStorage)
}

first_name.value = (isItemExist('first_name')) ? localStorage.first_name : ''
last_name.value = (isItemExist('last_name')) ? localStorage.last_name : ''
surname.value = (isItemExist('surname')) ? localStorage.surname : ''
email.value = (isItemExist('email')) ? localStorage.email : email.value
phone.value = (isItemExist('phone')) ? localStorage.phone : ''
adress.value = (isItemExist('adress')) ? localStorage.adress : ''

order_form.addEventListener('submit', () => {
  localStorage.first_name = first_name.value
  localStorage.last_name = last_name.value
  localStorage.surname = surname.value
  localStorage.email = email.value
  localStorage.phone = phone.value
  localStorage.adress = adress.value
})