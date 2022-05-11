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

const categoryToggle = document.querySelector('.js-category-toggle');
const categoryWrapper = document.querySelector('.js-category-wrapper');

categoryWrapper.classList.remove('no-js-wrapper');

categoryToggle.addEventListener('click', function (event) {
  if (categoryWrapper.classList.contains('category__wrapper--closed')) {
    categoryWrapper.classList.remove('category__wrapper--closed');
    categoryWrapper.classList.add('category__wrapper--show');
      } else {
        categoryWrapper.classList.add('category__wrapper--closed');
        categoryWrapper.classList.remove('category__wrapper--show');
      }
});

(function() {
  function getQTYup(url) {
fetch(url, {
  headers: {
    "X-Requested-With": "XMLHttpRequest",
  }
})
.then(response => response.json())
.then(data => {
  console.log('success');
});
}

function getCountGoods() {
let cart_remove_qty = document.querySelectorAll('.js-cart-remove');

for(i=0; i < cart_remove_qty.length; i++) {
    if(cart_remove_qty[i].previousSibling.previousSibling.textContent > 1) {
      cart_remove_qty[i].style.display = "block";
    } else {
      cart_remove_qty[i].style.display = "none";
    }
  }
}

getCountGoods();

  let cart_add_qty = document.querySelectorAll('.js-cart');
  for (i=0; i < cart_add_qty.length; i++) {
    cart_add_qty[i].addEventListener("click", (event) => {
      event.preventDefault();
      let targetLink = event.target.closest('a'); 
      if (event.target.tagName == 'a') {
        targetLink = event.target;
      } 
      let count_cart_block = targetLink.nextSibling.nextSibling;

      let ct_model = targetLink.getAttribute('data-ctmodel');
      let slug = targetLink.getAttribute('data-slug');
      count_cart = Number(count_cart_block.textContent) + 1;
      count_cart_block.textContent = count_cart;
      const getUrlCart = `/change_up/${ct_model}/${slug}/`;
      getQTYup(getUrlCart);
      getCountGoods()
  });
  }

  let cart_remove_qty = document.querySelectorAll('.js-cart-remove');
  for (i=0; i < cart_remove_qty.length; i++) {
    cart_remove_qty[i].addEventListener("click", (event) => {
      event.preventDefault();
      let targetLink = event.target.closest('a'); 
      if (event.target.tagName == 'a') {
        targetLink = event.target;
      } 
      let count_cart_block = targetLink.previousSibling.previousSibling;
      if (Number(count_cart_block.textContent) > 1) {
        count_cart = Number(count_cart_block.textContent) - 1;
        count_cart_block.textContent = count_cart;
      } else {
        targetLink.style.display = "none";
      }

      let ct_model = targetLink.getAttribute('data-ctmodel');
      let slug = targetLink.getAttribute('data-slug');
      
      const getUrlCart = `/change_down/${ct_model}/${slug}/`;

      getQTYup(getUrlCart);
      getCountGoods()

  });
  }

})();
