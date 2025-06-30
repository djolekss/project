$(document).ready(function () {
    $(".popup-button").click(function () {
        var target = $(this).data("target");
        $(".popup").hide();
        $("#" + target).css("display", "flex").hide().fadeIn();
    });

    $(".close").click(function () {
        $(this).closest(".popup").fadeOut();
    });

    $(window).click(function (e) {
        if ($(e.target).hasClass("popup")) {
            $(e.target).fadeOut();
        }
    });
});
document.querySelectorAll('#menu a').forEach(link => {
    link.addEventListener('click', function (e) {
        e.preventDefault();

        // Ukloni 'active' sa svih linkova
        document.querySelectorAll('#menu a').forEach(a => a.classList.remove('active'));

        // Dodaj 'active' kliknutom linku
        this.classList.add('active');

        // Sakrij sve content-tab divove
        document.querySelectorAll('.content-tab').forEach(tab => tab.classList.add('d-none'));

        // Prikaži samo onaj na koji je link ciljao
        const target = this.getAttribute('data-target');
        document.getElementById(target).classList.remove('d-none');
    });
});

$(document).ready(function () {
    // Datepicker
    $('.datepicker').datepicker({
        format: 'yyyy-mm-dd',
        startDate: '0d',
        autoclose: true,
        todayHighlight: true
    });

    // Timepicker
    $('.timepicker').timepicker({
        timeFormat: 'HH:mm',
        interval: 30,
        minTime: '08:00',
        maxTime: '20:00',
        defaultTime: '08:00',
        startTime: '08:00',
        dynamic: false,
        dropdown: true,
        scrollbar: true
    });
});

(() => {
    'use strict'
    const forms = document.querySelectorAll('form')
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault()
                event.stopPropagation()
            }
            form.classList.add('was-validated')
        }, false)
    })
})()
