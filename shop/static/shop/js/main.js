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