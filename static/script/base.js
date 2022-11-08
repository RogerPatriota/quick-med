function menuShow() {
    let menu = document.querySelector('.menu-drop')
    console.log(menu)
    if (menu.classList.contains('open')) {
        menu.classList.remove('open');
    }else {
        menu.classList.add('open')
    }

}