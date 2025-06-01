/* ATIVA E DESATIVA MENU MOBILE */
const menu = document.querySelector('.content-main__header-menu');
const navigation = document.querySelector('.navigation');
const icon = menu.querySelector('.hamburguer');

menu.addEventListener('click', () => {
    navigation.classList.toggle('open');
    
    if (icon.classList.contains('fa-bars')) {
        icon.classList.remove('fa-bars');
        icon.classList.add('fa-xmark');
    } else {
        icon.classList.remove('fa-xmark');
        icon.classList.add('fa-bars');
    }
});