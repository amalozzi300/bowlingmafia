function readURL(input) {

    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $(".profile__image").attr('src', e.target.result);
        }

        reader.readAsDataURL(input.files[0]);
    }
}

$(".account__input").on('change', function() {
    readURL(this);
});
