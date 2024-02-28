$(document).ready(function() {
    $('#registrationForm').submit(function(event) {
        event.preventDefault();

        var username = $('#username').val();
        var login = $('#login').val();
        var password = $('#password').val();
        var password1 = $('#password1').val();
        // var agree = $('TOS').val();

        if (password !== password1) {
            $('#message').text("Пароли не совпадают. Пожалуйста, введите одинаковые пароли.");
            return; // Остановка отправки запроса
        }
        // alert(agree);
        // if (!agree){
        //     $('#message').text("Увы, Вы не можете зарегистрироваться, не согласившись с нашими словиями использования!");
        //     return;
        // }

        var formData = {
            username: username,
            login: login,
            password: password,
            password1: password1
        };

        if (Object.values(formData).every(val => val.trim() !== '')) {
            $.ajax({
                type: 'POST',
                url: '/AJAX/API/register',
                data: JSON.stringify(formData), // Отправка данных в формате JSON
                contentType: 'application/json',
                success: function(response) {
                    $('#message').text(response.message); // Отображение сообщения с сервера

                    if (response.success) {
                        $('#username, #login, #password, #password1').val(''); // Очистка полей формы
                        // Дополнительные действия после успешной регистрации
                    }
                },
                error: function(xhr, status, error) {
                    $('#message').text("Ошибка при регистрации: " + error); // Отображение ошибки
                }
            });
        } else {
            $('#message').text("Пожалуйста, заполните все поля формы."); // Отображение сообщения об ошибках
        }
    });
});