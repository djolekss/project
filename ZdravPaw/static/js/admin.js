$(document).ready(function () {
    $('.sidebar a').click(function (e) {
        e.preventDefault();

        // Ukloni aktivnost sa svih linkova i sekcija
        $('.sidebar a').removeClass('active');
        $('.content-section').removeClass('active');

        // Dodaj aktivnost kliknutom linku
        $(this).addClass('active');

        // Dohvati ciljanu sekciju po data-target atributu
        const target = $(this).data('target');

        // Prikazi odgovarajucu sekciju
        $('#' + target).addClass('active');
    });
});