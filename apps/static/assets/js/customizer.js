'use strict';
checkCookie();

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
var layout_reset = document.querySelector('#layoutreset');
if (layout_reset) {
  layout_reset.addEventListener('click', function (e) {
    setCookie('rtl_layout', 'false', 1);
    setCookie('dark_layout', 'false', 1);
    setCookie('preset_color', 'preset-1', 1);
    setCookie('box_container', 'false', 1);
    setCookie('font_name', 'Roboto', 1);
    location.reload();
  });
}
if (box_container == 'true') {
  change_box_container('true');
} else {
  change_box_container('false');
}
if (font_name != '') {
  font_change(font_name);
}
// ============================================
if (!!document.querySelector('.pct-body')) {
  new SimpleBar(document.querySelector('.pct-body'));
}
var pc_toggle = document.querySelector('#pct-toggler');
if (pc_toggle) {
  pc_toggle.addEventListener('click', function () {
    if (!document.querySelector('.pct-customizer').classList.contains('active')) {
      document.querySelector('.pct-customizer').classList.add('active');
    } else {
      document.querySelector('.pct-customizer').classList.remove('active');
    }
  });
}

// preset color
var preset_color = document.querySelectorAll('.preset-color > a');
for (var h = 0; h < preset_color.length; h++) {
  var c = preset_color[h];

  c.addEventListener('click', function (event) {
    var targetElement = event.target;
    if (targetElement.tagName == 'SPAN') {
      targetElement = targetElement.parentNode;
    }
    var temp = targetElement.getAttribute('data-value');
    setCookie('preset_color', temp, 1);
    preset_change(temp);
  });
}

var c_box_container = document.querySelector('#layoutboxcontainer');
c_box_container.addEventListener('click', function () {
  if (c_box_container.checked) {
    change_box_container('true');
  } else {
    change_box_container('false');
  }
});

var c_rtl_layout = document.querySelector('#layoutmodertl');
c_rtl_layout.addEventListener('click', function () {
  if (c_rtl_layout.checked) {
    layout_rtl_change('true');
  } else {
    layout_rtl_change('false');
  }
});

function removeClassByPrefix(node, prefix) {
  for (let i = 0; i < node.classList.length; i++) {
    let value = node.classList[i];
    if (value.startsWith(prefix)) {
      node.classList.remove(value);
    }
  }
}
