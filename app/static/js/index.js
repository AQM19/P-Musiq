document.addEventListener('DOMContentLoaded', function () {
    const linkInp = document.getElementById('link-inp');
    const downloadBtn = document.getElementById('download-btn');
    const form = document.querySelector('form');

    function toggleControls(disabled) {
        downloadBtn.disabled = disabled;
        linkInp.readOnly = disabled;
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

    function sendLinkToServer(event) {
        event.preventDefault();

        const link = linkInp.value.trim();

        if (link) {
            toggleControls(true);

            const formData = new FormData(form);

            fetch(form.action, {
                method: 'POST',
                body: formData
            })
                .then(handleResponse)
                .then(handleBlobResponse)
                .catch(handleError)
                .finally(() => {
                    toggleControls(false);
                    linkInp.value = '';
                });
        } else {
            alert('Por favor ingresa un link de YouTube válido.');
        }
    }

    downloadBtn.addEventListener('click', sendLinkToServer);

    linkInp.addEventListener('keypress', function (event) {
        if (event.key === 'Enter') {
            sendLinkToServer(event);
        }
    });

});