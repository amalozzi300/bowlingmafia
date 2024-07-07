// Account Form
function update_profile_image_on_upload(input) {
    // updates the 'src' attribute of the profile_image field on the form when a new image is uploaded
    if(input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function(e) {
            $('.profile__image').attr('src', e.target.result);
        }

        reader.readAsDataURL(input.files[0]);
    }
}

$('.account__input').on('change', function() {
    // listener for new profile_image upload
    update_profile_image_on_upload(this);
});

// Sidepot Registration Form
function toggle_sidepot_field_visibility() {
    // toggles visibility of games_used and is_reverse sidepot form fields depending on the chosen sidepot type
    var sidepot_type = $('#sidepot__type')[0].val();
    var type_needs_games_used = ['Elim'];

    if(type_needs_games_used.includes(sidepot_type)) {
        $('.sidepot__conditional-toggle').show();
    }
    else {
        $('.sidepot__conditional-toggle').hide();
    }
}

$(function() {
    // checks for initial visibility toggle
    toggle_sidepot_field_visibility();
});

$('#sidepot__type').on('change', function() {
    // listener for change to sidepot's type field value
    toggle_sidepot_field_visibility()
});

$(function() {
    const form = $('form');
    const totalEntryFeeElement = $('#total-entry-fee');

    function updateTotalEntryFee() {
        let totalEntryFee = 0;
        const sidepotFields = form.find('[data-entry-fee]');

        sidepotFields.each(function() {
            const entryFee = parseFloat($(this).data('entry-fee'));
            
            if ($(this).is(':checkbox') && $(this).is(':checked')) {
                totalEntryFee += entryFee;
            }
            else if ($(this).attr('type') == 'number') {
                totalEntryFee += entryFee * $(this).val();
            }
        });

        totalEntryFeeElement.text(totalEntryFee.toFixed(2));
    }

    form.on('change', updateTotalEntryFee);
    updateTotalEntryFee();
});