const navUser = document.querySelector('.user-menu');
const UserToggle = document.querySelector('.user-menu__toggle');

if (navUser != null) {
  navUser.classList.remove('user-menu--nojs');
}

if (navUser != null) {
  UserToggle.addEventListener('click', function () {
    if (navUser.classList.contains('user-menu--closed')) {
      navUser.classList.remove('user-menu--closed');
      navUser.classList.add('user-menu--opened');
    } else {
      navUser.classList.add('user-menu--closed');
      navUser.classList.remove('user-menu--opened');
    }
  });
}

const navMain = document.querySelector('.nav');
const navToggle = document.querySelector('.nav__toggle');

navMain.classList.remove('nav--nojs');

navToggle.addEventListener('click', function () {
  if (navMain.classList.contains('nav--closed')) {
    navMain.classList.remove('nav--closed');
    navMain.classList.add('nav--opened');
  } else {
    navMain.classList.add('nav--closed');
    navMain.classList.remove('nav--opened');
  }
});

const activeMenu = document.querySelectorAll('.nav__item--active');

if (activeMenu[1]) {
  activeMenu[0].classList.remove('nav__item--active')
}

