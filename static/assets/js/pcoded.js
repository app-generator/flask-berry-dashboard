'use strict';

var flg = '0';
document.addEventListener('DOMContentLoaded', function () {
  // remove pre-loader start
  setTimeout(function () {
    document.querySelector('.loader-bg').remove();
  }, 400);
  // remove pre-loader end
  if (document.querySelector('body').hasAttribute("data-pc-layout")) {
    if (document.querySelector('body').getAttribute("data-pc-layout") == 'horizontal') {
      var docW = window.innerWidth;
      if (docW <= 1024) {
        add_scroller();
      }
    }
  } else {
    add_scroller();
  }

  var hamburger = document.querySelector('.hamburger:not(.is-active)');
  if (hamburger) {
    hamburger.addEventListener('click', function () {
      if (document.querySelector('.hamburger').classList.contains('is-active')) {
        document.querySelector('.hamburger').classList.remove('is-active');
      } else {
        document.querySelector('.hamburger').classList.add('is-active');
      }
    });
  }
  // Menu overlay layout start
  var overlay_menu = document.querySelector('#overlay-menu');
  if (overlay_menu) {
    overlay_menu.addEventListener('click', function () {
      menu_click();
      if (document.querySelector('.pc-sidebar').classList.contains('pc-over-menu-active')) {
        remove_overlay_menu();
      } else {
        document.querySelector('.pc-sidebar').classList.add('pc-over-menu-active');
        document.querySelector('.pc-sidebar').insertAdjacentHTML('beforeend', '<div class="pc-menu-overlay"></div>');
        document.querySelector('.pc-menu-overlay').addEventListener('click', function () {
          remove_overlay_menu();
          document.querySelector('.hamburger').classList.remove('is-active');
        });
      }
    });
  }
  // Menu overlay layout end

  // Menu collapse click start
  var mobile_collapse_vertical = document.querySelector('#mobile-collapse');
  if (mobile_collapse_vertical) {
    mobile_collapse_vertical.addEventListener('click', function () {
      if (!document.querySelector('body').classList.contains('pc-horizontal')) {
        // menu_click();
      }
      var temp_sidebar = document.querySelector('.pc-sidebar');
      if (temp_sidebar) {
        if (document.querySelector('.pc-sidebar').classList.contains('mob-sidebar-active')) {
          remove_menu();
        } else {
          document.querySelector('.pc-sidebar').classList.add('mob-sidebar-active');
          document.querySelector('.pc-sidebar').insertAdjacentHTML('beforeend', '<div class="pc-menu-overlay"></div>');
          document.querySelector('.pc-menu-overlay').addEventListener('click', function () {
            remove_menu();
            document.querySelector('.hamburger').classList.remove('is-active');
          });
        }
      }
    });
  }
  // Menu collapse click end

  // Menu collapse click start
  var mobile_collapse = document.querySelector('.pc-horizontal #mobile-collapse');
  if (mobile_collapse) {
    mobile_collapse.addEventListener('click', function () {
      if (document.querySelector('.topbar').classList.contains('mob-sidebar-active')) {
        remove_menu();
      } else {
        document.querySelector('.topbar').classList.add('mob-sidebar-active');
        document.querySelector('.topbar').insertAdjacentHTML('beforeend', '<div class="pc-menu-overlay"></div>');
        document.querySelector('.pc-menu-overlay').addEventListener('click', function () {
          remove_menu();
          document.querySelector('.hamburger').classList.remove('is-active');
        });
      }
    });
  }
  // Menu collapse click end
  // Horizontal menu click js start

  var topbar_link_list = document.querySelector('.pc-horizontal .topbar .pc-navbar>li>a');
  if (topbar_link_list) {
    topbar_link_list.addEventListener('click', function (e) {
      var targetElement = e.target;
      setTimeout(function () {
        targetElement.parentNodes.children[1].removeAttribute('style');
      }, 1000);
    });
  }
  // Horizontal menu click js end

  // header dropdown scrollbar start
  if (!!document.querySelector('.header-notification-scroll')) {
    new SimpleBar(document.querySelector('.header-notification-scroll'));
  }
  if (!!document.querySelector('.profile-notification-scroll')) {
    new SimpleBar(document.querySelector('.profile-notification-scroll'));
  }
  // header dropdown scrollbar end
  var sidebar_hide = document.querySelector('#sidebar-hide');
  if (sidebar_hide) {
    sidebar_hide.addEventListener('click', function () {
      if (document.querySelector('.pc-sidebar').classList.contains('pc-sidebar-hide')) {
        document.querySelector('.pc-sidebar').classList.remove('pc-sidebar-hide');
      } else {
        document.querySelector('.pc-sidebar').classList.add('pc-sidebar-hide');
      }
    });
  }
});

// Menu click start
function add_scroller() {
  menu_click();
  // Menu scrollbar start
  if (!!document.querySelector('.navbar-content')) {
    new SimpleBar(document.querySelector('.navbar-content'));
  }
  // Menu scrollbar end
}
// Menu click start
function menu_click() {
  var vw = window.innerWidth;
  var elem = document.querySelectorAll('.pc-navbar li');
  for (var j = 0; j < elem.length; j++) {
    elem[j].removeEventListener('click', function () { });
  }
  // if (!document.querySelector('body').hasAttribute("data-pc-layout", "compact")) {
  var elem = document.querySelectorAll('.pc-navbar li:not(.pc-trigger) .pc-submenu');
  for (var j = 0; j < elem.length; j++) {
    elem[j].style.display = 'none';
  }
  var pc_link_click = document.querySelectorAll('.pc-navbar > li:not(.pc-caption)');
  for (var i = 0; i < pc_link_click.length; i++) {
    pc_link_click[i].addEventListener('click', function (event) {
      event.stopPropagation();
      var targetElement = event.target;
      if (targetElement.tagName == 'SPAN') {
        targetElement = targetElement.parentNode;
      }
      if (targetElement.parentNode.classList.contains('pc-trigger')) {
        targetElement.parentNode.classList.remove('pc-trigger');
        slideUp(targetElement.parentNode.children[1], 200);
      } else {
        var tc = document.querySelectorAll('li.pc-trigger');
        for (var t = 0; t < tc.length; t++) {
          var c = tc[t];
          c.classList.remove('pc-trigger');
          slideUp(c.children[1], 200);
        }
        targetElement.parentNode.classList.add('pc-trigger');
        var tmp = targetElement.children[1];
        if (tmp) {
          slideDown(targetElement.parentNode.children[1], 200);
        }
      }
    });
  }
  var pc_sub_link_click = document.querySelectorAll('.pc-navbar > li:not(.pc-caption) li');
  for (var i = 0; i < pc_sub_link_click.length; i++) {
    pc_sub_link_click[i].addEventListener('click', function (event) {
      var targetElement = event.target;
      if (targetElement.tagName == 'SPAN') {
        targetElement = targetElement.parentNode;
      }
      event.stopPropagation();
      if (targetElement.parentNode.classList.contains('pc-trigger')) {
        targetElement.parentNode.classList.remove('pc-trigger');
        slideUp(targetElement.parentNode.children[1], 200);
      } else {
        var tc = targetElement.parentNode.parentNode.children;
        for (var t = 0; t < tc.length; t++) {
          var c = tc[t];
          c.classList.remove('pc-trigger');
          if (c.tagName == 'LI') {
            c = c.children[0];
          }
          if (c.parentNode.classList.contains('pc-hasmenu')) {
            slideUp(c.parentNode.children[1], 200);
          }
        }
        targetElement.parentNode.classList.add('pc-trigger');
        var tmp = targetElement.parentNode.children[1];
        if (tmp) {
          tmp.removeAttribute('style');
          slideDown(tmp, 200);
        }
      }
    });
  }
}


function remove_menu() {
  var temp_menu = document.querySelector('.pc-sidebar');
  if (temp_menu) {
    document.querySelector('.pc-sidebar').classList.remove('mob-sidebar-active');
  }
  if (document.querySelector('.topbar')) {
    document.querySelector('.topbar').classList.remove('mob-sidebar-active');
  }

  document.querySelector('.pc-sidebar .pc-menu-overlay').remove();
  document.querySelector('.topbar .pc-menu-overlay').remove();
}

function remove_overlay_menu() {
  document.querySelector('.pc-sidebar').classList.remove('pc-over-menu-active');
  if (document.querySelector('.topbar')) {
    document.querySelector('.topbar').classList.remove('mob-sidebar-active');
  }
  document.querySelector('.pc-sidebar .pc-menu-overlay').remove();
  document.querySelector('.topbar .pc-menu-overlay').remove();
}

window.addEventListener('load', function () {
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });
  var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
  var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl);
  });
  var toastElList = [].slice.call(document.querySelectorAll('.toast'));
  var toastList = toastElList.map(function (toastEl) {
    return new bootstrap.Toast(toastEl);
  });
});
// active menu item list start
var elem = document.querySelectorAll('.pc-sidebar .pc-navbar a');
for (var l = 0; l < elem.length; l++) {
  var pageUrl = window.location.href.split(/[?#]/)[0];
  if (elem[l].href == pageUrl && elem[l].getAttribute('href') != '') {
    elem[l].parentNode.classList.add('active');
    elem[l].parentNode.parentNode.parentNode.classList.add('active');
    elem[l].parentNode.parentNode.parentNode.classList.add('pc-trigger');
    elem[l].parentNode.parentNode.style.display = 'block';

    elem[l].parentNode.parentNode.parentNode.parentNode.parentNode.classList.add('active');
    elem[l].parentNode.parentNode.parentNode.parentNode.parentNode.classList.add('pc-trigger');
    elem[l].parentNode.parentNode.parentNode.parentNode.style.display = 'block';

    if (document.body.classList.contains('tab-layout')) {
      var temp = document.querySelector('.pc-tabcontent.active').getAttribute('data-value');
      document.querySelector('.tab-sidemenu > ul > li').classList.remove('active');
      document.querySelector('.tab-sidemenu > ul > li > a[data-cont="' + temp + '"]').parentNode.classList.add('active');
    }
  }
}

// horizontal submenu edge start
if (document.querySelector('body').classList.contains('pc-horizontal')) {
  var hpx;
  var docH = window.innerHeight;
  var docW = window.innerWidth;

  if (docW > 1024) {
    var topbar_has_menu = document.querySelector('.pc-horizontal .topbar .pc-submenu .pc-hasmenu');
    if (topbar_has_menu) {
      topbar_has_menu.addEventListener(
        'mouseenter',
        function () {
          var elm = targetElement.children[1];
          var off = elm.getBoundingClientRect();
          var l = off.left;
          var t = off.top;
          var w = off.width;
          var h = off.height;
          var screen_width = document.documentElement.scrollTop;

          var edge_pos = l + w <= docW;
          if (!edge_pos) {
            elm.classList.add('edge');
          }
          var isEntirelyVisible = t + h <= docH;
          if (!isEntirelyVisible) {
            var th = t - screen_width;
            elm.classList.add('scroll-menu');
            elm.css('max-height', 'calc(100vh - ' + th + 'px)');
            // new SimpleBar(document.querySelector('.scroll-menu'));
          }
        },
        function () {
          hpx.destroy();
          document.querySelector('.scroll-menu').removeAttribute('style');
          document.querySelector('.scroll-menu').classList.remove('scroll-menu');
        }
      );
    }
  }
}
// horizontal submenu edge end

var tc = document.querySelectorAll('.prod-likes .form-check-input');
for (var t = 0; t < tc.length; t++) {
  var prod_like = tc[t];
  prod_like.addEventListener('change', function (event) {
    if (event.currentTarget.checked) {
      prod_like = event.target;
      prod_like.parentNode.insertAdjacentHTML(
        'beforeend',
        '<div class="pc-like"><div class="like-wrapper"><span><span class="pc-group"><span class="pc-dots"></span><span class="pc-dots"></span><span class="pc-dots"></span><span class="pc-dots"></span></span></span></div></div>'
      );
      prod_like.parentNode.querySelector('.pc-like').classList.add('pc-like-animate');
      setTimeout(function () {
        prod_like.parentNode.querySelector('.pc-like').remove();
      }, 3000);
    } else {
      prod_like = event.target;
      prod_like.parentNode.querySelector('.pc-like').remove();
    }
  });
}

// =======================================================
// =======================================================
var rtl_flag = false;
var dark_flag = false;
function setCookie(cname, c_value, ext_days) {
  var d = new Date();
  d.setTime(d.getTime() + ext_days * 24 * 60 * 60 * 1000);
  var expires = 'expires=' + d.toGMTString();
  document.cookie = cname + '=' + c_value + ';' + expires + ';path=/';
}

function getCookie(cname) {
  var name = cname + '=';
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for (var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return '';
}





function checkCookie() {
  var temp = getCookie('dark_layout');
  if (temp != '') {
    dark_layout = temp;
  }
  var temp = getCookie('rtl_layout');
  if (temp != '') {
    rtl_layout = temp;
  }
  var temp = getCookie('preset_color');
  if (temp != '') {
    preset_color = temp;
  }
  var temp = getCookie('box_container');
  if (temp != '') {
    box_container = temp;
  }
  var temp = getCookie('font_name');
  if (temp != '') {
    font_name = temp;
  }
}
if (dark_layout == 'true') {
  layout_change('dark');
} else {
  layout_change('light');
}
if (rtl_layout == 'true') {
  layout_rtl_change('true');
} else {
  layout_rtl_change('false');
}
if (preset_color != '') {
  preset_change(preset_color);
}
if (box_container == 'true') {
  change_box_container('true');
} else {
  change_box_container('false');
}
if (font_name != '') {
  font_change(font_name);
}

function layout_rtl_change(value) {
  var control = document.querySelector('#layoutmodertl');
  if (value == 'true') {
    rtl_flag = true;
    document.getElementsByTagName('body')[0].setAttribute('data-pc-direction', 'rtl');
    document.getElementsByTagName('html')[0].setAttribute('dir', 'rtl');
    document.getElementsByTagName('html')[0].setAttribute('lang', 'ar');
    setCookie('rtl_layout', 'true', 1);
    if (control) {
      document.querySelector('#layoutmodertl').checked = true;
    }
  } else {
    rtl_flag = false;
    document.getElementsByTagName('body')[0].setAttribute('data-pc-direction', 'ltr');
    document.getElementsByTagName('html')[0].removeAttribute('dir');
    document.getElementsByTagName('html')[0].removeAttribute('lang');
    setCookie('rtl_layout', 'false', 1);
    if (control) {
      document.querySelector('#layoutmodertl').checked = false;
    }
  }
}

function font_change(name) {
  var srcs = '';
  if (name == 'Roboto') {
    srcs = 'https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap';
  }
  if (name == 'Poppins') {
    srcs = 'https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;700&display=swap';
  }
  if (name == 'Inter') {
    srcs = 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap';
  }
  document.querySelector('#main-font-link').setAttribute('href', srcs);
  document.querySelector('body').setAttribute('style', 'font-family:"' + name + '", sans-serif');
  setCookie('font_name', name, 1);
  var control = document.querySelector('.pct-offcanvas');
  if (control) {
    document.querySelector('#layoutfont' + name).checked = true;
  }
}
function layout_change(layout) {
  var control = document.querySelector('#layoutmodelight');
  document.getElementsByTagName('body')[0].setAttribute('data-pc-theme', layout);
  if (layout == 'dark') {
    dark_flag = true;
    setCookie('dark_layout', 'true', 1);
    if (control) {
      document.querySelector('#layoutmodedark').checked = true;
    }
  } else {
    dark_flag = false;
    setCookie('dark_layout', 'false', 1);

    if (control) {
      document.querySelector('#layoutmodelight').checked = true;
    }
  }
}
function change_box_container(value) {
  if (document.querySelector('.pc-content')) {
    var control = document.querySelector('#layoutbox_container');
    if (value == 'true') {
      document.querySelector('.pc-content').classList.add('container');
      document.querySelector('.footer-wrapper').classList.add('container');
      document.querySelector('.footer-wrapper').classList.remove('container-fluid');
      setCookie('box_container', 'true', 1);
      if (control) {
        document.querySelector('#layoutbox_container').checked = true;
      }
    } else {
      document.querySelector('.pc-content').classList.remove('container');
      document.querySelector('.footer-wrapper').classList.remove('container');
      document.querySelector('.footer-wrapper').classList.add('container-fluid');
      setCookie('box_container', 'false', 1);
      if (control) {
        document.querySelector('#layoutbox_container').checked = false;
      }
    }
  }
}

function preset_change(value) {
  var control = document.querySelector('.pct-offcanvas');
  document.getElementsByTagName('body')[0].setAttribute('data-pc-preset', value);
  if (control) {
    document.querySelector('.preset-color > a.active').classList.remove('active');
    document.querySelector(".preset-color > a[data-value='" + value + "']").classList.add('active');
  }
}

// =======================================================
// =======================================================
let slideUp = (target, duration = 0) => {
  target.style.transitionProperty = 'height, margin, padding';
  target.style.transitionDuration = duration + 'ms';
  target.style.boxSizing = 'border-box';
  target.style.height = target.offsetHeight + 'px';
  target.offsetHeight;
  target.style.overflow = 'hidden';
  target.style.height = 0;
  target.style.paddingTop = 0;
  target.style.paddingBottom = 0;
  target.style.marginTop = 0;
  target.style.marginBottom = 0;
};
let slideDown = (target, duration = 0) => {
  target.style.removeProperty('display');
  let display = window.getComputedStyle(target).display;

  if (display === 'none') display = 'block';

  target.style.display = display;
  let height = target.offsetHeight;
  target.style.overflow = 'hidden';
  target.style.height = 0;
  target.style.paddingTop = 0;
  target.style.paddingBottom = 0;
  target.style.marginTop = 0;
  target.style.marginBottom = 0;
  target.offsetHeight;
  target.style.boxSizing = 'border-box';
  target.style.transitionProperty = 'height, margin, padding';
  target.style.transitionDuration = duration + 'ms';
  target.style.height = height + 'px';
  target.style.removeProperty('padding-top');
  target.style.removeProperty('padding-bottom');
  target.style.removeProperty('margin-top');
  target.style.removeProperty('margin-bottom');
  window.setTimeout(() => {
    target.style.removeProperty('height');
    target.style.removeProperty('overflow');
    target.style.removeProperty('transition-duration');
    target.style.removeProperty('transition-property');
  }, duration);
};
var slideToggle = (target, duration = 0) => {
  if (window.getComputedStyle(target).display === 'none') {
    return slideDown(target, duration);
  } else {
    return slideUp(target, duration);
  }
};

// ========================== =============================
// ========================== =============================
