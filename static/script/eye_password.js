var icon = document.getElementById('icone')

icon.addEventListener('click', () => {

    let input = document.querySelector('.senha')

    if (input.getAttribute('type') == 'password') {
        input.setAttribute('type', 'text')
        icon.setAttribute('src', '/static/images/view.png')
    } else {
        input.setAttribute('type', 'password')
        icon.setAttribute('src', '/static/images/view (1).png')
    }

});