
document.addEventListener('DOMContentLoaded', function () {

    const slots = document.querySelectorAll('.time-slot');
    const hiddenInput = document.getElementById('selected_slots');
    const cancelBtn = document.getElementById('cancelSelection');

    let selected = [];
    slots.forEach(slot => {

        if (slot.classList.contains('booked')) {
            return;
        }

        slot.addEventListener('click', function () {

            const slotId = this.dataset.id;

            if (this.classList.contains('selected')) {

                this.classList.remove('selected');

                selected = selected.filter(id => id !== slotId);

            } else {

                this.classList.add('selected');

                selected.push(slotId);
            }

            hiddenInput.value = selected.join(',');
        });
    });

    cancelBtn.addEventListener('click', function () {

        selected = [];

        hiddenInput.value = '';

        slots.forEach(slot => {
            slot.classList.remove('selected');
        });
    });

    document.querySelector('.record-form')
        .addEventListener('submit', function(e) {

        if (selected.length === 0) {
            e.preventDefault();
            alert('Выберите хотя бы один временной слот');
        }
    });
});
