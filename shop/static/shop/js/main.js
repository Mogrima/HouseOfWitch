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