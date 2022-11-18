function menuShow() {
    let menu = document.querySelector('.menu')
    console.log(menu)
    if (menu.classList.contains('open')) {
        menu.classList.remove('open');
    }else {
        menu.classList.add('open')
    }

}