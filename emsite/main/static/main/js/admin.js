// =========================
    // CSRF
    // =========================

    function getCookie(name) {

        let cookieValue = null;

        if (document.cookie && document.cookie !== '') {

            const cookies = document.cookie.split(';');

            for (let i = 0; i < cookies.length; i++) {

                const cookie = cookies[i].trim();

                if (cookie.substring(0, name.length + 1) === (name + '=')) {

                    cookieValue = decodeURIComponent(
                        cookie.substring(name.length + 1)
                    );

                    break;
                }
            }
        }

        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');


    // =========================
    // TABS
    // =========================

    const tabs = document.querySelectorAll('.admin-tab');

    tabs.forEach(tab => {

        tab.addEventListener('click', () => {

            tabs.forEach(t => {
                t.classList.remove('active');
            });

            tab.classList.add('active');

            resetModes();

        });

    });


    // =========================
    // VARIABLES
    // =========================

    let deleteMode = false;
    let editMode = false;

    const confirmActions = document.querySelector('.admin-confirm-actions');

    const confirmBtn = document.querySelector('.admin-confirm-btn');

    const cancelBtn = document.querySelector('.admin-cancel-btn');


    // =========================
    // HELPERS
    // =========================

    function getCurrentWrapper() {

        return document.querySelector('.admin-table-wrapper');

    }

    function getCurrentActions() {

        return document.querySelector('.admin-actions');

    }

    function resetModes() {

        deleteMode = false;
        editMode = false;

        document.querySelectorAll('.admin-delete-btn').forEach(btn => {
            btn.classList.remove('active');
        });

        document.querySelectorAll('.admin-edit-btn').forEach(btn => {
            btn.classList.remove('active');
        });

        document
            .querySelectorAll('.selected-delete')
            .forEach(row => {
                row.classList.remove('selected-delete');
            });

        confirmActions.classList.add('hidden');

    }


    // =========================
    // DELETE BUTTON
    // =========================

    document.addEventListener('click', (e) => {

        const deleteBtn = e.target.closest('.admin-delete-btn');

        if (!deleteBtn) return;

        deleteMode = true;
        editMode = false;

        document.querySelectorAll('.admin-delete-btn').forEach(btn => {
            btn.classList.remove('active');
        });

        document.querySelectorAll('.admin-edit-btn').forEach(btn => {
            btn.classList.remove('active');
        });

        deleteBtn.classList.add('active');

        confirmActions.classList.remove('hidden');

    });


    // =========================
    // EDIT BUTTON
    // =========================

    document.addEventListener('click', (e) => {

        const editBtn = e.target.closest('.admin-edit-btn');

        if (!editBtn) return;

        editMode = !editMode;
        deleteMode = false;

        document.querySelectorAll('.admin-delete-btn').forEach(btn => {
            btn.classList.remove('active');
        });

        document.querySelectorAll('.admin-edit-btn').forEach(btn => {
            btn.classList.remove('active');
        });

        document
            .querySelectorAll('.selected-delete')
            .forEach(row => {
                row.classList.remove('selected-delete');
            });

        if (editMode) {

            editBtn.classList.add('active');

        }

        confirmActions.classList.add('hidden');

    });


    // =========================
    // TABLE ROW CLICK
    // =========================

    document.addEventListener('click', (e) => {

        const row = e.target.closest('tr');

        if (!row) return;

        if (row.closest('thead')) return;

        const wrapper = row.closest('.admin-table-wrapper');

        if (!wrapper) return;

        const id = row.dataset.id;


        // =========================
        // DELETE MODE
        // =========================

        if (deleteMode) {

            row.classList.toggle('selected-delete');

        }


        // =========================
        // EDIT MODE
        // =========================

        if (editMode) {

            const editUrl = wrapper.dataset.editUrl;

            window.location.href = `${editUrl}${id}/`;

        }

    });


    // =========================
    // CANCEL
    // =========================

    cancelBtn.addEventListener('click', () => {

        resetModes();

    });


    // =========================
    // CONFIRM DELETE
    // =========================

    confirmBtn.addEventListener('click', async () => {

        const wrapper = getCurrentWrapper();

        if (!wrapper) return;

        const deleteUrl = wrapper.dataset.deleteUrl;

        const selectedRows = document.querySelectorAll('.selected-delete');

        const ids = [];

        selectedRows.forEach(row => {

            ids.push(row.dataset.id);

        });

        if (ids.length === 0) {

            alert('Выберите записи');

            return;

        }

        try {

            const response = await fetch(deleteUrl, {

                method: 'POST',

                headers: {
                    'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/x-www-form-urlencoded',
                },

                body: new URLSearchParams({
                    'ids[]': ids
                })

            });

            const data = await response.json();

            if (data.success) {

                resetModes();

            }

        }

        catch(error) {

            console.error(error);

        }

    });


    // =========================
    // HTMX SUPPORT
    // =========================

    document.body.addEventListener('htmx:afterSwap', () => {

        resetModes();

    });