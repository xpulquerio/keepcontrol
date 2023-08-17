// // JavaScript for scrolling the images
// const movieList = document.querySelector('.movie-list'); //#Pegando o elemento referenciado lá no HTML
// let scrollPosition = 0; //Iniciar na posição 0

// function scrollMovies() {
//     scrollPosition += 1; // Ajusta a velocidade de rolagem
//     if (scrollPosition >= movieList.scrollWidth) { //Se a posição da rolagem for maior ou igual ao tamanho total da lista, voltar para posição 0
//         scrollPosition = 0;
//     }
//     movieList.scrollTo(scrollPosition, 0); //Atualizo a nova posição para o valor que foi alterado em cima.
//     requestAnimationFrame(scrollMovies); //Deixa a animação suave na rolagem
// }

// scrollMovies(); //Chama a função para começar o loop

const movieList = document.querySelector('.movie-list');
const leftArrow = document.getElementById('left-arrow');
const rightArrow = document.getElementById('right-arrow');
let scrollPosition = 0;

function scrollMovies(direction) {
    const step = 200; // Ajuste este valor para controlar a distância de rolagem
    if (direction === 'left') {
        scrollPosition -= step;
    } else {
        scrollPosition += step;
    }
    if (scrollPosition < 0) {
        scrollPosition = 0;
    } else if (scrollPosition > movieList.scrollWidth - movieList.clientWidth) {
        scrollPosition = movieList.scrollWidth - movieList.clientWidth;
    }
    movieList.scrollTo({ left: scrollPosition, behavior: 'smooth' });
}

leftArrow.addEventListener('click', () => scrollMovies('left'));
rightArrow.addEventListener('click', () => scrollMovies('right'));
