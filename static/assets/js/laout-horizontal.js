'use strict';
document.getElementsByTagName('body')[0].setAttribute('data-pc-layout', 'horizontal');
const pc_link = document.querySelector('.pc-navbar').innerHTML;

var docW = window.innerWidth;
if (docW > 1024) {
    set_horizontal_menu();
    set_edge_menu();
}
window.addEventListener('resize', function () {
    if (docW > 1024) {
        document.querySelector('.pc-navbar').innerHTML = pc_link;
        set_horizontal_menu();
        set_edge_menu();
    }
});
function set_horizontal_menu() {
    var pc_menu_list = document.querySelectorAll('.pc-navbar > li.pc-item');
    var pc_new_list = '';
    var pc_single_link = '';
    var flag_item = '';
    var flag_item_extra = '';
    var flag_w = 0;
    var flag_hit = false;
    var flag_hit_extra = false;
    pc_menu_list.forEach(function (item, list_index) {
        if (item.classList.contains("pc-caption")) {
            if (flag_hit_extra === true) {
                if (flag_item_extra.insertAdjacentHTML) {
                    flag_item_extra.insertAdjacentHTML(
                        'afterend',
                        '<li class="pc-item pc-hasmenu">\
                        <a href="#!" class="pc-link ">\
                            <span class="pc-micon"><i class="'+ flag_item_extra.children[1].getAttribute('class') + '"></i></span>\
                            <span class="pc-mtext">'+
                        flag_item_extra.children[0].innerHTML +
                        '</span>\
                            <span class="pc-arrow"><i class="ti ti-chevron-right"></i></span>\
                        </a>\
                        <ul class="pc-submenu">' +
                        pc_new_list +
                        '\
                        </ul>\
                    </li>'
                    );
                    flag_item_extra.remove();
                }
            }
            flag_hit_extra = true;
            pc_new_list = "";
            flag_hit = false;
            flag_item_extra = item;
        } else {
            if (flag_hit === false) {
                pc_single_link = flag_item;
                flag_hit = true;
            }
            pc_new_list += item.outerHTML;
            if (list_index + 1 === pc_menu_list.length) {
                if (flag_hit_extra === true) {
                    if (flag_item_extra.insertAdjacentHTML) {
                        flag_item_extra.insertAdjacentHTML(
                            'afterend',
                            '<li class="pc-item pc-hasmenu">\
                            <a href="#!" class="pc-link ">\
                                <span class="pc-micon"><i class="'+ flag_item_extra.children[1].getAttribute('class') + '"></i></span>\
                                <span class="pc-mtext">'+
                            flag_item_extra.children[0].innerHTML +
                            '</span>\
                                <span class="pc-arrow"><i class="ti ti-chevron-right"></i></span>\
                            </a>\
                            <ul class="pc-submenu">' +
                            pc_new_list +
                            '\
                            </ul>\
                        </li>'
                        );
                        flag_item_extra.remove();
                    }
                }
                flag_hit_extra = true;
                pc_new_list = "";
                flag_hit = false;
                flag_item_extra = item;;
            }
            item.remove();
        }
    });
    var pc_menu_list_new = document.querySelectorAll('.pc-navbar > li.pc-item');
    pc_menu_list_new.forEach(function (item, list_index) {
        flag_w += get_width(item) + 49;
        if (flag_w > window.innerWidth) {
            if (flag_hit === false) {
                pc_single_link = flag_item;
                flag_hit = true;
            }
            if (flag_hit === true) {
                pc_new_list += item.outerHTML;
                item.remove();
            }
        } else {
            flag_item = item;
        }
        if (list_index + 1 === pc_menu_list_new.length) {
            if (pc_single_link.insertAdjacentHTML) {
                pc_single_link.insertAdjacentHTML(
                    'afterend',
                    '<li class="pc-item pc-hasmenu">\
                          <a href="#!" class="pc-link ">\
                              <span class="pc-micon"><i class="ti ti-archive"></i></span>\
                              <span class="pc-mtext">Other</span>\
                              <span class="pc-arrow"><i class="ti ti-chevron-right"></i></span>\
                          </a>\
                          <ul class="pc-submenu">' +
                    pc_new_list +
                    '\
                          </ul>\
                      </li>'
                );
            }
        }
    });
}
function set_edge_menu() {
    var temp_link = document.querySelectorAll('.pc-sidebar .pc-navbar .pc-hasmenu');
    for (var t = 0; t < temp_link.length; t++) {
        var c = temp_link[t];
        c.addEventListener('mouseenter',
            function (event) {
                collapse_edge(event)
            },
            function (event) {
                event.children[1].classList.remove('edge');
                event.children[1].classList.remove('edge-alt');
            }
        );
    }
}
function get_width(element) {
    var off = element.getBoundingClientRect();
    var w = off.width;
    return w;
}
function get_height(element) {
    var off = element.getBoundingClientRect();
    var h = off.height;
    return h;
}
// Collapse  edge start
function collapse_edge(event) {
    var hpx;
    var docH = window.innerHeight;
    var docW = window.innerWidth;
    if (docW > 1024) {
        var targetElement = event.target;
        var elm = targetElement.children[1];
        var off = elm.getBoundingClientRect();
        var l = off.left;
        var t = off.top;
        var w = off.width;
        var h = off.height;
        var edge_pos = l + w <= docW;
        if (!edge_pos) {
            elm.classList.add('edge');
        }

        var edge_pos_alt = t + h <= docH;
        if (!edge_pos_alt) {
            elm.classList.add('edge-alt');
            
            var edge_pos_alt_big = t >= h;
            if (!edge_pos_alt_big) {
                elm.classList.add('edge-alt-full');
                var drp_top = t - 140;
                var drp_bottom = h - t - 140;
                var temp_style = "top: -" + drp_top + "px; bottom: -" + drp_bottom + "px";
                elm.setAttribute("style", temp_style);
            }
        }
    }
}