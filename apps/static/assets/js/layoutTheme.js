let isDark = localStorage.getItem('dark_layout');

if (isDark === "true") {
    layout_change("dark")
} else {
    layout_change("light")
}


document.getElementById("p_dark_mode").addEventListener("change", function (event) {
    console.log(this.checked)

    if (this.checked === true) { //set dark
        layout_change("dark")
    } else {                      //set light
        layout_change("light")
    }
})


function layout_change(layout) {
    var control = document.querySelector('#p_dark_mode');
    var icon = document.querySelector('#p_mode_icon');

    document.getElementsByTagName('body')[0].setAttribute('data-pc-theme', layout);

    if (layout === 'dark') {
        dark_flag = true;
        localStorage.setItem('dark_layout', 'true');

        if (control) {
            control.checked = true;
        }
        if (icon) {
            icon.classList.replace("ti-sun-off", "ti-sun")
        }

    } else {
        dark_flag = false;
        localStorage.setItem('dark_layout', 'false');

        if (control) {
            control.checked = false;
        }
        if (icon) {
            icon.classList.replace("ti-sun", "ti-sun-off")
        }
    }
}
