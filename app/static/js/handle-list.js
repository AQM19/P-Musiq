document.addEventListener('DOMContentLoaded', function () {
    const inputItem = document.getElementById('input-item');
    const addButton = document.getElementById('add-button');
    const itemList = document.querySelector('.item-list');
    const downloadBtn = document.querySelector('.download-btn');

    function toggleControls(disabled) {
        downloadBtn.disabled = disabled;
        addButton.disabled = disabled;
        inputItem.readOnly = disabled;
    }

    function createDeleteButton() {
        const button = document.createElement('button');
        button.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height=18" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M3 6h18M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2" />
        </svg>
        `;
        button.className = 'delete-btn';

        button.addEventListener('click', function () {
            const itemText = button.parentElement.textContent;
            deleteLinkFromList(itemText);
        });

        return button;
    }

    function addItem() {
        const itemText = inputItem.value.trim();

        if (itemText) {
            const items = Array.from(itemList.children).map(li => li.textContent.trim());
            if (items.includes(itemText)) {
                alert('Ese link ya está en el listado');
                return;
            }

            const li = document.createElement('li');
            const span = document.createElement('span');
            const deleteButton = createDeleteButton();

            span.textContent = itemText;
            li.appendChild(span);
            li.appendChild(deleteButton);

            itemList.appendChild(li);

            inputItem.value = '';
        }
    }

    function handleError(error) {
        console.error('Error al enviar el formulario:', error);
        alert('Hubo un problema al procesar tu solicitud.');
    }

    function handleResponse(response) {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const contentType = response.headers.get('Content-Type');
        if (contentType && contentType.includes('application/json')) {
            return response.json().then(data => {
                throw new Error(data.error || 'Unknown error occurred');
            });
        } else {
            return response.blob().then(blob => ({ blob, response }));
        }
    }

    function handleBlobResponse({ blob, response }) {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;

        const filename = extractFilenameFromResponse(response);

        a.download = filename;
        document.body.appendChild(a);
        a.click();
        a.remove();

        window.URL.revokeObjectURL(url);
    }

    function extractFilenameFromResponse(response) {
        const contentDisposition = response.headers.get('Content-Disposition');
        let filename = 'audio.mp3';

        if (contentDisposition) {
            const match = contentDisposition.match(/filename="?([^"]+)"?/);
            if (match && match[1]) {
                filename = match[1];
            }
        }

        return filename;
    }

    function deleteLinkFromList(link) {
        const listItem = Array.from(itemList.children).find(li => li.textContent === link);
        if (listItem) {
            listItem.classList.add('fade-out-right');
            listItem.addEventListener('animationend', () => {
                listItem.remove();
            }, { once: true });
        }
    }

    async function downloadItemsSequentially(items) {
        for (const link of items) {
            try {
                const response = await fetch('/download-list', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ item: link })
                });
                const result = await handleResponse(response);
                await handleBlobResponse(result);

                deleteLinkFromList(link);

            } catch (error) {
                handleError(error);
            }
        }
    }

    function disableDeleteButtons() {
        const deleteBtns = document.querySelectorAll('.delete-btn');
        deleteBtns.forEach(btn => {
            btn.disabled = true;
        })
    }

    async function sendListToServer() {
        const items = Array.from(itemList.children).map(li => li.textContent);

        toggleControls(true);
        disableDeleteButtons();

        await downloadItemsSequentially(items);

        toggleControls(false);
    }

    addButton.addEventListener('click', addItem);

    inputItem.addEventListener('keypress', function (event) {
        if (event.key === 'Enter') {
            addItem();
        }
    });

    downloadBtn.addEventListener('click', sendListToServer);
})